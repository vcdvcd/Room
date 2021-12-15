import os
import sys
from socket import *
from select import select
def main():
    client = socket(AF_INET, SOCK_STREAM)
    if login(client):
        connect(client)
def connect(client):
    rlist = [client, sys.stdin]
    wlist = []
    xlist = []
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is client:
                data = client.recv(1024)
                if data.decode() == 'e\n':
                    client.close()
                    print('管理员关闭了聊天室')
                    os._exit(0)
                else:
                    print(data.decode(), end='')
            elif r is sys.stdin:
                data = sys.stdin.readline()
                if data == 'e\n':
                    data = user + ': ' + '用户离开了聊天室' + '\n'
                    client.send(data.encode())
                    client.close()
                    os._exit(0)
                else:
                    if data.split(' ')[0] == 'sendto':
                        data1 = user+': '+data
                        client.send(data1.encode())
                    else:
                        data = user + ': ' + data
                        client.send(data.encode())
def login(client):
    global user
    user = input('用户名称:')
    # 再连接到服务器，传送用户名以检验
    client.connect(('127.0.0.1', 8000))
    print('连接到', ('127.0.0.1', 8000))
    client.send(user.encode())
    data = client.recv(1024)
    if data.decode() == 'user already existed':
        print('该用户已经存在')
        return False
    else:
        data = user + ': ' + '用户进入聊天室' + '\n'
        client.send(data.encode())
        return True


if __name__ == '__main__':
    main()