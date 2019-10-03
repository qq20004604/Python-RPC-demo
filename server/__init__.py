#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from concurrent import futures
import time
import grpc
import proto.helloworld_pb2 as helloworld_pb2
import proto.helloworld_pb2_grpc as helloworld_pb2_grpc

PORT = 50051
MAX_WORKERS = 10


# 实现 proto 文件中定义的 GreeterServicer
class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # 当 proto 文件中定义的 rpc 被触发时（指 rpc SayHello 这个方法），执行本函数
    def SayHello(self, request, context):
        # request 实质上是 proto 定义的 message HelloRequest 这个类的实例，可以通过 request.name 拿到 name 的值
        print('client send: %s' % request.name)
        return helloworld_pb2.HelloReply(message='hello {msg}'.format(msg=request.name))

    # 这里相对上面，就复杂一些，添加一些处理逻辑，返回不同的信息
    def SendPeople(self, request, context):
        print('client send: name(%s), age(%s)' % (request.name, request.age))
        name = request.name
        age = request.age
        # 名字长度大于3，并且age大于20，则返回 True，否则 False
        if age > 20 and len(name) > 3:
            return helloworld_pb2.IsCorrect(isRight=True)
        else:
            return helloworld_pb2.IsCorrect(isRight=False)


class GRPCServer(object):
    def __init__(self):
        pass

    def run(self):
        # 启动 rpc 服务，设置连接池，最大为10个用户
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
        # 设置 Server，并启用响应函数
        helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
        # 监听本机的 50051 端口
        server.add_insecure_port('[::]:%s' % PORT)
        # 启动服务
        server.start()
        print('server start!')
        # 这个是为了维持 Server 一直在启动。从这里可以推断，上面应该是起了一个新的线程或者进程。
        try:
            while True:
                time.sleep(60 * 60 * 24)  # one day in seconds
        except KeyboardInterrupt:
            # 如果用户手动中断（比如 ctrl + c？）
            server.stop(0)


# 测试和示例代码
if __name__ == '__main__':
    server = GRPCServer()
    server.run()
