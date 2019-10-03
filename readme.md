# 说明

## 1、安装

1、安装 runtime

```
pip install grpcio
```

2、安装 python 下的 protoc 编译器

```
pip install grpcio-tools
```

3、写 proto 文件（见 proto/hellworld.proto）

4、编译 proto 文件

proto/helloworld.proto 是文件路径

```
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
```

* python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
* --python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
* --grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
* -I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录

此时生成 helloworld_pb2.py 和 helloworld_pb2_grpc.py 两个文件

* helloworld_pb2.py: 用来和 protobuf 数据进行交互
* helloworld_pb2_grpc.py: 用来和 grpc 进行交互

5、分别编写 server 端的服务和 client 的服务

* server：需要常驻开启
* client：请求时连接 server 端

## 2、使用

已封装 client 和 server 的代码。

先运行 server 的 py 文件，再运行 client 的 py 文件即可。