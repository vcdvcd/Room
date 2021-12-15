import os
import sys
from socket import *
from select import select
def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen()
    accept(server)
def accept(server):

    rlist = [server, sys.stdin]
    wlist = []
    xlist = []
    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is server:
                conn, addr = server.accept()
                if validate(conn):
                    rlist.append(conn)
                    print('来自', addr)
                    userAdds[users[-1]] = conn
                else:
                    conn.close()
            elif r is sys.stdin:
                data = sys.stdin.readline()
                if data == 'e\n':
                    for c in rlist[2:]:
                        c.send(b'e\n')
                        c.close()
                    server.close()
                    print('管理员关闭了聊天室!')
                    os._exit(0)
                if data == 'cluster\n':
                    print(users)
                else:
                    data = '管理员' + ': ' + data
                    f1 = open('message.txt', 'a')
                    f1.write(data)
                    f1.close()
                    for c in rlist[2:]:
                        c.send(data.encode())
            else:
                data = r.recv(1024)
                if data.decode().split(' ')[1] == '用户离开了聊天室\n':
                    username = data.decode().split(':')[0]
                    users.remove(username)
                    r.close()
                    rlist.remove(r)
                if len(data.decode().split(" ")) > 2:
                    if data.decode().split(" ")[1] == 'sendto':
                        msg = data.decode().split(":")
                        data1 = data.decode().split(" ")
                        f1 = open('message.txt', 'a')
                        f1.write(msg[0]+" 发送给 "+data1[2]+": "+data1[3])
                        f1.close()
                        userAdds[data1[2]].send((data1[0]+data1[3]).encode())
                        break
                    else:
                        print(data.decode(), end='')
                        f1 = open('message.txt', 'a')
                        f1.write(data.decode())
                        f1.close()
                        for c in rlist[2:]:
                            if c is not r:
                                c.send(data)
                else:
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
    users = []
    userAdds = {}
    main()