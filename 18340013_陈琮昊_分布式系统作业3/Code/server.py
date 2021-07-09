from threading import Event
from concurrent import futures
import time
import grpc


import pubsub_pb2
import pubsub_pb2_grpc

class Pubsub(object):
    def __init__(self):
        self.storage = {}
        self.event = {}
        
    def publish(self, topic, message):
        # 发布
        newmessage = ""
        if topic not in self.storage:
            self.storage[topic] = [{'create time': time.time(), 'message': message}]
            newmessage += "create topic: {}\n".format(topic)
        else:
            self.storage[topic].append({'create time': time.time(), 'message': message})
        if topic in self.event:
            for client in self.event[topic]:
                self.event[topic][client].set()
        newmessage += "Successfully publish!"
        return newmessage
    
    def generatemessage(self, newmessage):
        # 转化
        return str(newmessage['create time']) + ": " + newmessage['message']
    
    def refresh(self, TTL=5):
        # 控制消息在服务器的存储时间，超时则删除
        ttl = time.time() - 5
        for topic in self.storage:
            while len(self.storage[topic]) and self.storage[topic][0]['create time'] <= ttl:
                del self.storage[topic][0]
                
    def browse(self, topic):
        # 浏览
        if topic not in self.storage:
            return ["topic not created!"]
        for newmessage in self.storage[topic]:
            yield self.generatemessage(newmessage)
    
    def subcribe(self, topic, clientId, TTL=10):
        # 订阅
        if topic not in self.event:
            self.event[topic] = {}
        self.event[topic][clientId] = Event()
        createtime = time.time()
        remaintime = TTL
        while True:
            self.event[topic][clientId].wait(remaintime)
            remaintime = TTL - (time.time() - createtime)
            if remaintime <= 0:
                break
            yield self.generatemessage(self.storage[topic][-1])
            self.event[topic][clientId].clear()

class PubsubService(pubsub_pb2_grpc.Pubsub):
    def __init__(self):
        self.pubsub = Pubsub() 
        
    def publish(self, request, context): 
        newmessage = self.pubsub.publish(request.topic, request.context)
        return pubsub_pb2.reply(message = newmessage)
    
    def browse(self, request, context):
        for newmessage in self.pubsub.browse(request.topic):
            yield pubsub_pb2.reply(message=newmessage)  #
    
    def subcribe(self, request, context):  
        for newmessage in self.pubsub.subcribe(request.topic, request.clientId, request.TTL):   
            yield pubsub_pb2.reply(message=newmessage)

if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20)) 
    pubsub_server = PubsubService() 
    pubsub_pb2_grpc.add_PubsubServicer_to_server(pubsub_server, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Hello from server!')
    try:
        while True:
            time.sleep(1)
            pubsub_server.pubsub.refresh() 
    except KeyboardInterrupt:
        server.stop(0)