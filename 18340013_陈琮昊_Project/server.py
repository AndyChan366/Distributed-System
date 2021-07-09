import re
import grpc
import logging
import time
import argparse
import socket
import threading
import src
from src import tcp_protobuf_pb2
import hashlib
import numpy as np
import bisect
from concurrent.futures import ThreadPoolExecutor

# 当某个slave超过WAITTIME没发送心跳，说明挂了
WAITTIME = 5


# server调用slave服务器的grpc服务，实现slave上的数据库操作
class DATA():
    def __init__(self, slave_ip, slave_port):
        self.ip = slave_ip
        self.port = slave_port
        self.channel = grpc.insecure_channel('{}:{}'.format(slave_ip, slave_port))
        self.stub = src.DatastoreStub(self.channel)

    def __del__(self):
        self.channel.close()

    def put(self, key, value):
        try:
            response = self.stub.put(src.Request(key=key, value=value))
            return response
        except grpc._channel._Rendezvous:
            # 当消息处理失败时，在try的except处返回处理失败的消息给用户
            return src.Response(message='Failed!')

    def get(self, key):
        try:
            response = self.stub.get(src.Request(key=key))
            return response
        except grpc._channel._Rendezvous:
            return src.Response(message='Failed!')

    def delete(self, key):
        try:
            response = self.stub.delete(src.Request(key=key))
            return response
        except grpc._channel._Rendezvous:
            return src.Response(message='Failed!')

    def transform(self, start, end, ip, port):
        try:
            response = self.stub.transform(src.TransFrom(start=start, end=end, aim_ip=ip, aim_port=port))
            return response
        except grpc._channel._Rendezvous:
            print('Data transform error! From {}:{} to {}:{}, range {}-{}'.format(self.ip, self.port, ip, port, start, end))
        return src.Response(message='Failed!')


# 一致性哈希算法的简单实现
class HashRing():
    # 虚拟节点的数目（默认为0，即每个节点只在一致性哈希环上有一个节点）
    def __init__(self, virtual_number=0):
        # 一致性哈希环使用一个有序数组来表示
        self.node_number = virtual_number + 1
        # 存储每个slave节点的哈希值（可能有虚拟节点）
        self.circle_hash = np.array([])
        # 存储每个slave节点的DATA结构体
        self.circle_data = np.array([])
        # 存储每个slave节点最近一次的访问时间，字典的key为(ip, port)的字符串对，value为time.time()的值
        self.slave_last_access_time = dict()

    # 字符串哈希
    def hash(self, slavename):
        digest = hashlib.md5(slavename.encode('utf-8')).digest()
        res = ((digest[3] & 0xFF) << 24) | ((digest[2] & 0xFF) << 16) | ((digest[1] & 0xFF) << 8) | (digest[0] & 0xFF)
        return res & 0xFFFFFFFF

    # 根据key的哈希决定它的数据存在哪个slave中
    def get(self, key):
        key_hashvalue = self.hash(key)
        # 二分查找，返回大于等于改哈希值的第一个节点
        index = bisect.bisect_left(self.circle_hash, key_hashvalue)
        # 如果当前的哈希值已经比最大哈希值还大，则取模，故为0
        if index >= self.circle_hash.shape[0]:
            index = 0
        return self.circle_data[index]

    # 根据slave的ip和port将它加入到一致性哈希环中
    def add_node(self, ip, port):
        # 如果是本来就存在的节点则不执行任何操作
        if (ip, port) in self.slave_last_access_time:
            return
        data = DATA(ip, port)
        tmp_hash = []
        tmp_data = []
        count = 0
        for i in range(self.node_number):
            slavename = '{}:{}#{}'.format(ip, port, str(i))
            slavehash = self.hash(slavename)
            tmp_hash.append(slavehash)
            tmp_data.append(data)
            # 只有当前一致性哈希环上有节点的时候才需要数据迁移
            if self.circle_hash.shape[0] == 0:
                continue
            # 新节点加入时需要把原来处理这个区间的节点的数据进行迁移
            index = bisect.bisect_left(self.circle_hash, slavehash)
            if index >= self.circle_hash.shape[0]:
                index = 0
            last_index = index - 1
            if last_index < 0:
                last_index = self.circle_hash.shape[0] - 1
            # transform是目标节点的操作，将这个新节点的ip和port还有它覆盖的哈希范围发给目标节点，目标节点再调用新节点的receive服务将对应的key和value发送给它
            try:
                response = self.circle_data[index].transform(
                    self.circle_hash[last_index] + 1, slavehash, ip, port)
            except:
                response = src.Response(message='Failed!')
            if response.message != 'Done!':
                # 如果迁移失败就不入网
                tmp_hash.pop()
                tmp_data.pop()
                count += 1
                print('Failed to add new slave {}:{} #{}'.format(ip, port, i))
        if count == self.node_number:
            return
        self.slave_last_access_time[(ip, port)] = time.time()
        # 将结果补充到环上
        self.circle_hash = np.append(self.circle_hash, tmp_hash).astype(np.int64)
        self.circle_data = np.append(self.circle_data, tmp_data)
        # 保证这个哈希环是有序的，保证能够使用二分查找
        sorted_index = self.circle_hash.argsort()
        self.circle_hash = self.circle_hash[sorted_index]
        self.circle_data = self.circle_data[sorted_index]

    # 根据slave的ip和port将它移除一致性哈希环
    def remove_node(self, ip, port):
        remove_indices = []
        for i in range(self.node_number):
            slavename = '{}:{}#{}'.format(ip, port, str(i))
            slavehash = self.hash(slavename)
            remove_index = bisect.bisect_left(self.circle_hash, slavehash)
            # 防止一些不必要的bug（比如刚好有2个slave的哈希值相同）
            while remove_index < self.circle_hash.shape[0] and self.circle_hash[remove_index] == slavehash:
                if self.circle_data[remove_index].ip != ip or self.circle_data[
                    remove_index].port != port:
                    remove_index += 1
                else:
                    break
            # 如果出bug，这个节点本来就不在哈希环上，那就什么都不操作
            if remove_index >= self.circle_hash.shape[0] or self.circle_hash[remove_index] != slavehash:
                continue
            remove_indices.append(remove_index)
        # 节点删除
        if (ip, port) in self.slave_last_access_time:
            self.slave_last_access_time.pop((ip, port))
        self.circle_hash = np.delete(self.circle_hash, remove_indices)
        self.circle_data = np.delete(self.circle_data, remove_indices)


# server提供建立slave连接的服务，用于识别新加入的slave
class RPCServer(src.SlaveServicer):
    def __init__(self, hashring):
        self.hashring = hashring

    # 如果这个slave没出现过，加入一致性哈希环；更新它的访问时间
    def add_slave_setting(self, request, context):
        print('Slave({}, {}), welcome!'.format(request.ip, request.port))
        if not (request.ip, request.port) in self.hashring.slave_last_access_time:
            self.hashring.add_node(request.ip, request.port)
        else:
            self.hashring.slave_last_access_time[(request.ip, request.port)] = time.time()
        return src.SlaveCode(message='Success!')


# 处理用户请求的线程函数
def _processing_request(hashring, con, addr):
    # 下面的操作用线程池处理
    message = b''
    # 先接受message的长度
    data = con.recv(1024)
    data_decode = data.decode('utf-8')
    message_length = re.findall('([0-9]*)\n\n', data_decode)
    # 如果没找到就断开连接
    if len(message_length) != 1:
        con.close()
        return
    data = data_decode[len(message_length[0]) + 2:].encode('utf-8')
    message_length = int(message_length[0])
    while True:
        message += data
        if (len(message) >= message_length):
            break
        data = con.recv(1024)
        if not data:
            break
    # result是从client发来的信息
    result = tcp_protobuf_pb2.Request()
    result.ParseFromString(message)
    print('Message from {}: operation({}), key({}), value({})'.format(addr, result.operation, result.key, result.value))
    while True:
        try:
            data = None
            if result.operation == 'put':
                data = hashring.get(result.key)
                # response是从slave发来的处理结果
                response = data.put(result.key, result.value)
            elif result.operation == 'get':
                data = hashring.get(result.key)
                response = data.get(result.key)
            elif result.operation == 'delete':
                data = hashring.get(result.key)
                response = data.delete(result.key)
            else:
                response = src.Response(message='Failed!')
        # 不管这里发生了什么错误，都给客户端返回操作失败
        except:
            print('Transation failed! {} at {}'.format(addr, result))
            response = src.Response(message='Failed!')
        print(data.ip, data.port)
        if response.message != 'Done!' and data is not None:
            # 不管什么原因导致这次服务Failed了，我们都检查一下这个data对应的slave有没有过期，如果过期了就把它删了重新来过
            if not (data.ip, data.port) in hashring.slave_last_access_time or time.time() - \
                    hashring.slave_last_access_time[(data.ip, data.port)] > WAITTIME:
                hashring.remove_node(data.ip, data.port)
                continue
        # 正常访问，则直接退出
        break
    if response.message != 'Done!':
        # backres是发送回client的信息
        backres = tcp_protobuf_pb2.Response(message='Failed!')
    else:
        backres = tcp_protobuf_pb2.Response(message='Done!')
        if result.operation == 'get':
            backres.value = response.value
    con.sendall(backres.SerializeToString())
    con.close()


# server通过TCP监听获取client的请求
class TCPServer():
    # server_tcp_port负责监听client通信，server_rpc_port负责监听是否有新的slave加入
    def __init__(self, server_ip='localhost', server_tcp_port=8000, server_rpc_port=8001):
        self.server_ip = server_ip
        self.server_tcp_port = server_tcp_port
        self.server_rpc_port = server_rpc_port
        # 建立slave节点数据分发的一致性哈希环
        self.hashring = HashRing(virtual_number=3)
        # 建立新slave服务器入分布式系统的监听服务
        self.rpcserver = grpc.server(ThreadPoolExecutor(max_workers=1))
        src.add_SlaveServicer_to_server(RPCServer(self.hashring), self.rpcserver)
        self.rpcserver.add_insecure_port('{}:{}'.format(server_ip, server_rpc_port))
        self.rpcserver.start()
        print('Slave rpc service start!')
        # 建立处理TCP连接的线程池
        self.executor = ThreadPoolExecutor(max_workers=30)
        # 建立监听client请求的TCP服务
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.server_ip, self.server_tcp_port))

    def __del__(self):
        self.rpcserver.stop(0)
        self.sock.close()

    def _listen(self):
        print('Start listening!')
        # 无限循环，监听客户端的TCP请求
        while True:
            con, addr = self.sock.accept()
            # _processing_request(self.hashring, con, addr)
            # 从线程池请求一个线程来处理当前请求
            t = self.executor.submit(_processing_request, self.hashring, con, addr)

    def listen(self):
        print('Waiting for connection...')
        self.sock.listen(20)
        # 等待连接，并且把连接信息丢给线程处理
        t = threading.Thread(target=self._listen)
        t.setDaemon(True)
        t.start()
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            print('Close server!')

    def start():
        pass


def server_start(args):
    tcpserver = TCPServer(args.server_ip, args.server_tcp_port, args.server_rpc_port)
    tcpserver.listen()


if __name__ == '__main__':
    # 参数设置
    parser = argparse.ArgumentParser(description='Dictionary server.')
    parser.add_argument('--server-ip', type=str, default='localhost', metavar='N', help='The ip of dictionary server.')
    parser.add_argument('--server-tcp-port', type=int, default=8000, metavar='N',
                        help='The tcp port of dictionary server.')
    parser.add_argument('--server-rpc-port', type=int, default=8001, metavar='N',
                        help='The rpc port of dictionary server.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    server_start(args)