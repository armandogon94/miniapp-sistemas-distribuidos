# Alumnos:
# Armando Gonzalez V-20.977.787
# Michael Amariscua V-26.745.371
# Ricardo Perez V-26.040.729

import socket
import base64
import threading
import time
import hashlib
import sys


class myThread (threading.Thread):
    def __init__(self, threadID, name, size, ipaddr, port):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.size = size
        self.port = port
        self.ipaddr = ipaddr
        self.md5 = ""

    def run(self):
        print("Starting " + self.name)
        self.udp_message_reception(
            self.name, self.size, self.ipaddr, self.port)
        print("Exiting " + self.name)

    def set_md5(self, md5):
        self.md5 = md5

    def get_md5(self):
        return self.md5

    def udp_message_reception(self, threadName, size, ipaddr, port):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((ipaddr, port))
        udp_socket.settimeout(10)
        try:
            print("entro udp")
            if size % 3 != 0:
                newsize = size + 3 - (size % 3)
            else:
                newsize = size
            print(newsize)
            newsize = int((newsize/3)*4)
            print(newsize)
            givememsg_response = udp_socket.recv(newsize)
            print(givememsg_response)
            server_msg = base64.b64decode(givememsg_response.decode('utf-8'))
            server_msg_txt = server_msg.decode("utf-8")
            md5_chksum = hashlib.md5(server_msg).hexdigest()
            print(md5_chksum)
            self.set_md5(md5_chksum)
            print("recibio udp")
            print(givememsg_response)
            print(server_msg_txt)
            print(self.md5)
        except socket.timeout:
            print("error udp")
        udp_socket.close()


try:
    ip_address = sys.argv[1]
    tcp_port_connection = sys.argv[2]
    username = sys.argv[3]
    local_ip = sys.argv[4]
    udp_port_connection = sys.argv[5]
except:
    sys.exit(
        "ERROR. Por favor ingrese los datos como se muestra --> cliente.py ipDestino puertoTCP usuario ipLocal puertoUDP")

print("Bienvenido al sistema!")
print("Recibiendo datos... Espere un momento")
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((ip_address, int(tcp_port_connection)))

helloiam_txt = "helloiam " + username
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
        udp_thread = myThread(1, "UDP-1", msglen_size,
                              local_ip, int(udp_port_connection))
        udp_thread.start()
        givememsg_txt = "givememsg " + udp_port_connection  # 15601
        counter = 3
        while counter:
            tcp_socket.send(givememsg_txt.encode("ascii"))
            givememsg_response = tcp_socket.recv(1024)
            givememsg_response_txt = givememsg_response.decode("ascii")
            print("givememsg response ->"+givememsg_response_txt)
            counter -= 1
        chkmd5_txt = "chkmsg " + udp_thread.get_md5()
        print(chkmd5_txt)
        tcp_socket.send(chkmd5_txt.encode('ascii'))
        chkmd5_response = tcp_socket.recv(1024).decode('ascii')
        print("ckmd5 response -> " + chkmd5_response)
        udp_thread.join()

bye_txt = "bye"
tcp_socket.send(bye_txt.encode("ascii"))

bye_response = tcp_socket.recv(1024)
bye_response_txt = bye_response.decode("ascii")
print("bye response -> " + bye_response_txt)
tcp_socket.close()
