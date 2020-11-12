# Alumnos:
# Armando Gonzalez V-20.977.787
# Michael Amariscua V-2-.---.---
# Ricardo Perez V-2-.---.---

import sys
import os
import threading
import time

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
sock = createConnection
