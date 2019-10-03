#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import grpc
import proto.helloworld_pb2 as helloworld_pb2
import proto.helloworld_pb2_grpc as helloworld_pb2_grpc
import time, sys

HOST = 'localhost'
PORT = 50051


def error_log(msg):
    with open('./rpc_err.log', 'a')as f:
        f.write('%s||%s||%s\n' % (
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            sys._getframe(1).f_code.co_name,  # 执行errlog这个函数的函数名字，即上一级函数
            msg
        ))


# RPC专用类（客户端）
class GRPCClient(object):
    def __init__(self):
        server = '%s:%s' % (HOST, PORT)
        # 连接 rpc 服务器
        channel = grpc.insecure_channel(server)
        # 调用 rpc 服务，GreeterStub 这个类名是固定生成的，参照 helloworld_pb2_grpc.py
        self.stub = helloworld_pb2_grpc.GreeterStub(channel)

    def send_hello(self, name):
        is_error = False
        error_msg = ''
        try:
            # s 是一个基于 dict 的实例
            s = helloworld_pb2.HelloRequest(name=name)
            # 调用 SayHello 向 Server 发送信息
            # 这个函数是在 __init__ 时被定义的，定义时，添加了3个参数，分别定义了唯一标识、指定压缩格式（str to 二进制）、解压缩格式。
            # 所以这里调用时，会被自动压缩成对应的参数，然后发送到 server 去。
            # 如果只看转成二进制字符串这一步，相当于
            # import grpc._common as common
            # common.serialize(s, helloworld_pb2.HelloRequest.SerializeToString)
            # 然后你也可以拿去，用自己的通信方式去发送数据
            response = self.stub.SayHello(s)
        except BaseException as e:
            # 这个错误信息可能是服务器连接失败
            is_error = True
            error_msg = e
            error_log(e.details())
            return {
                'code': 0,
                'msg': 'send error',
                'data': e
            }
        finally:
            # 组织返回信息
            if is_error:
                return {
                    'code': 0,
                    'msg': error_msg,
                    'data': {}
                }
            else:
                return {
                    'code': 200,
                    'msg': 'success',
                    'data': response
                }

    def send_people(self, name, age):
        is_error = False
        error_msg = ''
        try:
            s = helloworld_pb2.PeopleRequest(name=name, age=age)
            # 向Server发送信息
            response = self.stub.SendPeople(s)
        except BaseException as e:
            # 这个错误信息可能是服务器连接失败
            is_error = True
            error_msg = e
            error_log(e.details())
            return {
                'code': 0,
                'msg': 'send error',
                'data': e
            }
        finally:
            # 组织返回信息
            if is_error:
                return {
                    'code': 0,
                    'msg': error_msg,
                    'data': {}
                }
            else:
                return {
                    'code': 200,
                    'msg': 'success',
                    'data': response
                }


# 测试和示例代码
if __name__ == '__main__':
    client = GRPCClient()
    # response = client.send_hello('这是一个消息')
    # if response['code'] is 200:
    #     print(response['msg'])
    #     print(response['data'].message)
    # else:
    #     print('error')

    res2 = client.send_people('张三', 20)
    if res2['code'] is 200:
        print(res2['msg'])
        print(res2['data'].isRight)
    else:
        print('error')
