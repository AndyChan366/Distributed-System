import logging
import argparse
import socket
from src.tcp_protobuf_pb2 import Request, Response
import threading


class Client():
    def __init__(self, server_ip, server_tcp_port):
        self.server_ip = server_ip
        self.server_tcp_port = server_tcp_port

    def recv(self, sock):
        message = b''
        while True:
            data = sock.recv(1024)
            if not data:
                break
            message += data
        # result是从client发来的信息
        result = Response()
        result.ParseFromString(message)
        return result

    def send(self, sock, strbits):
        # 先发送一个数据长度过去，来确定结束位置
        sock.sendall((str(len(strbits)) + '\n\n').encode('utf-8'))
        # 再发送消息的具体内容
        sock.sendall(strbits)

    # 每个操作都单独建立一次TCP连接
    def get(self, key):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_ip, self.server_tcp_port))
        # 通信格式使用proto文件内的定义，里面有3个成员变量：operation，key，value
        message_bit = Request(operation='get', key=key).SerializeToString()
        self.send(sock, message_bit)
        result = self.recv(sock)
        print(result)
        sock.close()

    def put(self, key, value):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_ip, self.server_tcp_port))
        message_bit = Request(operation='put', key=key, value=value).SerializeToString()
        self.send(sock, message_bit)
        result = self.recv(sock)
        print(result)
        sock.close()

    def delete(self, key):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_ip, self.server_tcp_port))
        message_bit = Request(operation='delete', key=key).SerializeToString()
        self.send(sock, message_bit)
        result = self.recv(sock)
        print(result)
        sock.close()


def client_start(args):
    print('Please press Ctrl+C to exit the client.')
    client = Client(args.server_ip, args.server_tcp_port)
    try:
        while True:
            # 输入一个操作
            operation = input('input operation: ')
            if operation == 'put':
                key = input('input key: ')
                value = input('input value: ')
                client.put(key, value)
            elif operation == 'get':
                key = input('input key: ')
                client.get(key)
            elif operation == 'delete':
                key = input('input key: ')
                client.delete(key)
            else:
                print('operation error!')
    except KeyboardInterrupt:
        print('Close client!')


if __name__ == '__main__':
    # 参数设置
    parser = argparse.ArgumentParser(description='Client.')
    parser.add_argument('--server-ip', type=str, default='localhost', metavar='N', help='The ip of dictionary server.')
    parser.add_argument('--server-tcp-port', type=int, default=8000, metavar='N', help='The ip of dictionary server.')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    client_start(args)