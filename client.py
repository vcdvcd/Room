# client.py

# 导入系统模块
import os, sys
# 导入网络编程（传输层）模块
from socket import *
# IO多路复用模块
from select import select
def main():
    'main 主函数'
    client = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字
    # 登录函数
    if login(client):
        # 连接函数
        connect(client)

def connect(client):
    'connect 客户端连接函数'

    # 使用select模块的select方法实现IO多路复用监听传输
    rlist = [client, sys.stdin]
    wlist = []
    xlist = []

    while True:
        rs, ws, xs = select(rlist, wlist, xlist)

        for r in rs:
            if r is client:
                # 接受服务器发来的消息
                data = client.recv(1024)
                if data.decode() == 'e\n':
                    # 如果消息为回车，聊天室关闭
                    client.close()
                    print('管理员关闭了聊天室')
                    os._exit(0)
                else:
                    # 打印接收到的信息
                    print(data.decode(), end='')
            elif r is sys.stdin:
                # 发送消息给服务器
                data = sys.stdin.readline()
                if data == 'e\n':
                    # 如果回车，发送退出消息，关闭客户端，退出聊天室
                    data = user + ': ' + '用户离开了聊天室' + '\n'
                    client.send(data.encode())
                    client.close()
                    os._exit(0)
                else:
                    if data.split(' ')[0] == 'sendto':
                        data1 = user+': '+data
                        client.send(data1.encode())
                    else:
                        # 发信息给服务器
                        data = user + ': ' + data
                        client.send(data.encode())

def login(client):
    '登录函数 login'
    # 使用全局变量管理用户
    # 先让客户端输入姓名
    global user
    user = input('用户名称:')
    # 再连接到服务器，传送用户名以检验
    client.connect(('127.0.0.1', 8000))  # 连接到服务器地址
    print('连接到', ('127.0.0.1', 8000))
    client.send(user.encode())
    data = client.recv(1024)
    if data.decode() == 'user already existed':
        # 如果用户名已经存在，要求重新输入
        print('该用户已经存在')
        return False
    else:
        data = user + ': ' + '用户进入聊天室' + '\n'
        client.send(data.encode())
        return True


if __name__ == '__main__':
    main()