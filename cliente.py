import socket
import base64
import threading
import time
from hashlib import md5

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('127.0.0.1', 19876))

helloiam_txt = "helloiam usuario_1"
tcp_socket.send(helloiam_txt.encode("ascii"))

helloiam_response = tcp_socket.recv(1024)
helloiam_response_txt = helloiam_response.decode("ascii")

print(helloiam_response_txt)
if helloiam_response_txt == 'ok\n':
    print('si mano')
    msglen_txt = "msglen"
    tcp_socket.send(msglen_txt.encode("ascii"))

    msglen_response = tcp_socket.recv(1024)
    msglen_response_txt = msglen_response.decode("ascii")
    print(msglen_response_txt)
    msglen_confirmation = msglen_response_txt.split(' ')
    if msglen_confirmation[0] == 'ok':
        msglen_size = int(msglen_confirmation[1])
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.connect(('127.0.0.1', 15601))
        givememsg_txt = 'givememsg 15601'
        print('h1')
        tcp_socket.send(givememsg_txt.encode("ascii"))
        print('h2')
        givememsg_response = udp_socket.recv(msglen_size)
        print('h3')
        server_msg = base64.b64decode(givememsg_response)
        print(server_msg)
        udp_socket.close()


tcp_socket.close()


# print('hola')
