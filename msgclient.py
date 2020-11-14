# Alumnos:
# Armando Gonzalez V-20.977.787
# Michael Amariscua V-26.745.371
# Ricardo Perez V-26.040.729

import sys
import os
import threading
import time
import socket
import base64
from hashlib import md5

try:
    ipAddress = sys.argv[1]
    portConnection = sys.argv[2]
    username = sys.argv[3]
except:
    sys.exit(
        "ERROR. Por favor ingrese los datos como se muestra --> msgcliente.py ip puerto usuario")

print("Bienvenido al sistema!")
print("Cargando datos... Espere un momento")

print("ip: ", ipAddress)
print("port: ", portConnection)
print("user: ", username)
"""with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ipAddress, portConnection))
    s.sendall(b'Hello, world')
    data = s.recv(1024)"""
