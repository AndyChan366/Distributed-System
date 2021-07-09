import grpc
import lmdb
import logging
import time
import hashlib
import argparse
from queue import Queue
from threading import Condition, Thread
from concurrent.futures import ThreadPoolExecutor
from src import add_DatastoreServicer_to_server, DatastoreServicer, Response, SlaveStub, SlaveInformation, BackUp, DatastoreStub

ENCODING = 'utf-8'
# 如果超过WAITTIME没返回结果，说明挂掉了
WAITTIME = 2
# 向server发送heartbeat确认的间隔
HEARTBEAT = 1

#字符串哈希
def hash(key):
    dig = hashlib.md5(key.encode('utf-8')).digest()
    res = ((dig[3] & 0xFF) << 24) | ((dig[2] & 0xFF) << 16) | ((dig[1] & 0xFF) <<8) | (dig[0] & 0xFF)
    return res & 0xFFFFFFFF

# 用队列+condition函数的方式实现单调写
def dandiaowrite(db_name, queue):
    while True:
        # queue.get在队列是空的时候会自动阻塞当前线程
        cond, operation, key, value, response = queue.get()
        with cond:
            if operation == 'put':
                with lmdb.open(db_name) as env:
                    beginning = env.begin(write=True)
                    result = beginning.put(key.encode(ENCODING), value.encode(ENCODING))
                    beginning.commit()
                if result:
                    response.message = 'Done!'
                else:
                    response.message = 'Failed!'
            elif operation == 'delete':
                with lmdb.open(db_name) as env:
                    beginning = env.begin(write=True)
                    result = beginning.delete(key.encode(ENCODING))
                    beginning.commit()
                if result:
                    response.message = 'Done!'
                else:
                    response.message = 'Failed!'
            elif operation == 'recieve':
                result = 0
                if len(key) == 0:
                    response.message = 'Done!'
                else:
                    with lmdb.open(db_name) as env:
                        beginning = env.begin(write=True)
                        for k, v in zip(key, value):
                            result += beginning.put(k.encode(ENCODING), v.encode(ENCODING))
                        beginning.commit()
                    if result > 0:
                        response.message = 'Done!'
                    else:
                        response.message = 'Failed!'
            # 通知对应的线程，服务已经commit了
            cond.notify()


# slave提供的关于数据库操作的grpc服务
class Slave(DatastoreServicer):
    def __init__(self, db_name, queue):
        self.db_name = db_name
        self.queue = queue

    # 对于put和delete必须按顺序执行
    def put(self, request, context):
        print('Put request from {}: key({}), value({})'.format(context.peer(), request.key, request.value))
        # 使用Condition阻塞当前任务，直到单调写把这个写任务完成
        c = Condition()
        response = Response(message='Failed!')
        with c:
            # 放入队列中
            self.queue.put((c, 'put', request.key, request.value, response))
            # 等待单调写进程完成数据库操作
            result = c.wait(WAITTIME)
        if not result:
            response.message = 'Failed!'
        return response

    # 不用写数据库的get操作就自由发挥
    def get(self, request, context):
        print('Get request from {}: key({}), value({})'.format(context.peer(), request.key, request.value))
        with lmdb.open(self.db_name) as env:
            beginning = env.begin(write=False)
            result = beginning.get(request.key.encode(ENCODING))
        if result is None:
            return Response(message='Failed!')
        return Response(message='Done!', value=result.decode(ENCODING))

    # 对于put和delete必须按顺序执行
    def delete(self, request, context):
        print('Delete request from {}: key({}), value({})'.format(context.peer(), request.key, request.value))
        # 使用Condition阻塞当前任务，直到单调写把这个写任务完成
        c = Condition()
        response = Response(message='Failed!')
        with c:
            self.queue.put((c, 'delete', request.key, request.value, response))
            result = c.wait(WAITTIME)
        if not result:
            response.message = 'Failed!'
        return response

    # 接受一系列key和value，用于数据迁移
    def receive(self, request, context):
        print('Receive request from {}: keys_number({}), values_number({})'.format(context.peer(), len(request.keys), len(request.values)))
        # 使用Condition阻塞当前任务，直到单调写把这个写任务完成
        c = Condition()
        response = Response(message='Failed!')
        with c:
            self.queue.put((c, 'recieve', request.keys, request.values, response))
            # 数据迁移等的时间久一点
            result = c.wait(WAITTIME * 10)
        if not result:
            response.message = 'Failed!'
        return response

    # 判断当前key的哈希值在不在指定的区间里
    def check(self, keyhash, start, end):
        if end >= start:
            return keyhash >= start and keyhash <= end
        else:
            return keyhash >= start or keyhash <= end

    # 接受key的哈希范围，将这个范围对应的key发送给目标
    def transform(self, request, context):
        print('Transform request from {}: start({}), end({}), aim_ip({}), aim_port({})'.format(context.peer(), request.start, request.end, request.aim_ip, request.aim_port))
        backup = BackUp()
        with lmdb.open(self.db_name) as env:
            beginning = env.begin(write=False)
            for key, value in beginning.cursor():
                key = key.decode(ENCODING)
                if self.check(hash(key), request.start, request.end):
                    backup.keys.append(key)
                    backup.values.append(value.decode(ENCODING))
        channel = grpc.insecure_channel('{}:{}'.format(request.aim_ip, request.aim_port))
        stub = DatastoreStub(channel)
        response = stub.receive(backup)
        return response

def slave_start(args):
    # 数据库名
    db_name = 'db_{}_{}'.format(args.ip, args.port)
    # 单调写队列
    write_queue = Queue()
    # 监听来自server关于服务器操作的rpc服务
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_DatastoreServicer_to_server(Slave(db_name, write_queue), server)
    server.add_insecure_port('{}:{}'.format(args.ip, args.port))
    server.start()
    # 单独建立一个线程处理单调写队列里面的任务
    t = Thread(target=dandiaowrite, args=(db_name, write_queue))
    t.setDaemon(True)
    t.start()
    print('Datastore service start!')
    # slave建立后，调用dictionary_server的grpc服务器，进行这个slave服务器识别
    print('Slave start!')
    # 每隔一段时间向server发一个信号表示存在感
    try:
        while True:
            try:
                channel = grpc.insecure_channel('{}:{}'.format(args.server_ip, args.server_rpc_port))
                stub = SlaveStub(channel)
                errcode = stub.add_slave_setting(SlaveInformation(ip=args.ip, port=args.port))
                channel.close()
            except grpc._channel._Rendezvous:
                print('Link to dictionary server failed, try again.')
            time.sleep(HEARTBEAT)
    except KeyboardInterrupt:
        server.stop(0)
        print('Close slave!')

if __name__ == '__main__':
    # 参数设置
    parser = argparse.ArgumentParser(description='Slave server.')
    parser.add_argument('--server-ip', type=str, default='localhost', metavar='N', help='The ip of dictionary server.')
    parser.add_argument('--server-rpc-port', type=str, default='8001', metavar='N', help='The port of dictionary server.')
    parser.add_argument('--ip', type=str, default='localhost', metavar='N', help='The ip of this slave server.')
    parser.add_argument('--port', type=str, default='8002', metavar='N', help='The port of this slave server.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    slave_start(args)