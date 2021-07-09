import grpc
import time
import threading
import pubsub_pb2
import pubsub_pb2_grpc

clientId = input("Please input Id: ")
channel = grpc.insecure_channel('localhost:50051')
stub = pubsub_pb2_grpc.PubsubStub(channel)
def publish(topic, context):
    print("Publish message in {}:{}".format(topic, context))
    response = stub.publish(pubsub_pb2.publishRequest(topic=topic, context=context))
    print(response.message)
def browse(topic):
    print("Browse topic :{}".format(topic))
    response = stub.browse(pubsub_pb2.browseRequest(topic=topic))
    for i in response:
        print(i.message)
def receive(topic, TTL):
    for j in stub.subcribe(pubsub_pb2.subRequest(topic=topic, clientId=clientId, TTL=TTL)):
        print("Receive message from {}:{}".format(topic, j.message))

def subcribe(topic, TTL=10):
    print("Successfully subscribed {}!".format(topic))
    xc = threading.Thread(target=receive, args=(topic,TTL))
    xc.start()
        
publish('testtopic1', 'message1')
browse('testtopic1')
time.sleep(5)
publish('testtopic2', 'message2')
subcribe('testtopic2', 10)
publish('testtopic3', 'message3')
time.sleep(5)
browse('testtopic3')