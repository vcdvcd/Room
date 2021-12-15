# server.py

# 导入系统模块
import os, sys
# 导入网络编程（传输层）模块
from socket import *
# IO多路复用模块
from select import select
import json

def main():
    'main 主函数'
    server = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口可立即重用
    server.bind(('127.0.0.1', 8000))  # 绑定地址
    server.listen()  # 监听

    # 接收函数
    accept(server)

def accept(server):
    'accept 服务器接受函数'

    # 使用select模块的select方法实现IO多路复用监听传输
    rlist = [server, sys.stdin]
    wlist = []
    xlist = []

    while True:
        rs, ws, xs = select(rlist, wlist, xlist)

        for r in rs:
            if r is server:
                # 服务器接受客户端连接
                conn, addr = server.accept()
                # 调用validate函数检查用户名
                if validate(conn):
                    # 将客户端套接字添加到rlist中以监听
                    rlist.append(conn)
                    # 如果用户名注册成功
                    print('来自', addr)
                    userAdds[users[-1]] = conn
                else:
                    conn.close()
            elif r is sys.stdin:
                # 服务器向所有客户端发送系统（管理员）消息
                data = sys.stdin.readline()
                if data == 'e\n':
                    # 如果服务器输入回车，则退出
                    for c in rlist[2:]:
                        c.send(b'e\n')
                        c.close()
                    server.close()
                    print('管理员关闭了聊天室!')
                    os._exit(0)
                if data == 'cluster\n':
                    print(users)
                else:
                    # 如果服务器输入正常语句，通知所有客户端
                    data = '管理员' + ': ' + data
                    f1 = open('message.txt', 'a')
                    f1.write(data)
                    f1.close()
                    for c in rlist[2:]:
                        c.send(data.encode())
            else:
                # 服务器接受客户端的消息并转发给所有客户端
                data = r.recv(1024)
                if data.decode().split(' ')[1] == '用户离开了聊天室\n':
                    username = data.decode().split(':')[0]
                    users.remove(username)
                    r.close()
                    rlist.remove(r)
                if len(data.decode().split(" ")) > 2:
                    if data.decode().split(" ")[1] == 'sendto':
                        data1 = data.decode().split(" ")
                        userAdds[data1[2]].send((data.decode().split(" ")[0]+data1[3]).encode())
                        break
                if not data:
                    # 关闭客户端
                    r.close()
                    rlist.remove(r)
                else:
                    # 转发信息给其他客户端
                    print(data.decode(), end='')
                    f1 = open('message.txt', 'a')
                    f1.write(data.decode())
                    f1.close()
                    for c in rlist[2:]:
                        if c is not r:
                            c.send(data)

def validate(client):
    name = client.recv(1024).decode()
    if name in users:
        client.send(b'user already existed')
        return False
    else:
        users.append(name)
        client.send(b'Welcome!')
        return True


if __name__ == '__main__':
    # 全局变量，管理用户信息
    users = []
    userAdds = {}
    # 主函数
    main()