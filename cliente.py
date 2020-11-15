import socket
import base64
import threading
import time
from hashlib import md5


class myThread (threading.Thread):
    def __init__(self, threadID, name, size):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.size = size
        self.rcvmsg = False

    def run(self):
        print("Starting " + self.name)
        udp_message_reception(self.name, self.size)
        print("Exiting " + self.name)

    def received(self):
        return self.rcvmsg


def udp_message_reception(threadName, size):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('127.0.0.1', 15601))
    udp_socket.settimeout(5)
    try:
        print("entro udp")
        newsize = size + 4 - (size % 4)
        givememsg_response = udp_socket.recv(newsize).decode('utf-8')

        server_msg = base64.b64decode(givememsg_response).decode("utf-8")
        print("recibio udp")
        print(givememsg_response)
        print(server_msg)
    except socket.timeout:
        print("error udp")
    udp_socket.close()


tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('127.0.0.1', 19876))

helloiam_txt = "helloiam usuario_1"
tcp_socket.send(helloiam_txt.encode("ascii"))

helloiam_response = tcp_socket.recv(1024)
helloiam_response_txt = helloiam_response.decode("ascii")

print("helloiam response -> " + helloiam_response_txt)
if helloiam_response_txt == 'ok\n':
    msglen_txt = "msglen"
    tcp_socket.send(msglen_txt.encode("ascii"))

    msglen_response = tcp_socket.recv(1024)
    msglen_response_txt = msglen_response.decode("ascii")
    print("msglen_response -> " + msglen_response_txt)
    msglen_confirmation = msglen_response_txt.split(' ')
    if msglen_confirmation[0] == 'ok':
        msglen_size = int(msglen_confirmation[1])
        udp_thread = myThread(1, "UDP-1", msglen_size)
        udp_thread.start()
        givememsg_txt = "givememsg 15601"
        counter = 5
        while counter:
            tcp_socket.send(givememsg_txt.encode("ascii"))
            givememsg_response = tcp_socket.recv(1024)
            givememsg_response_txt = givememsg_response.decode("ascii")
            print("givememsg response ->"+givememsg_response_txt)
            counter -= 1
        udp_thread.join()

bye_txt = "bye"
tcp_socket.send(bye_txt.encode("ascii"))

bye_response = tcp_socket.recv(1024)
bye_response_txt = bye_response.decode("ascii")
print("bye response -> " + bye_response_txt)
tcp_socket.close()
