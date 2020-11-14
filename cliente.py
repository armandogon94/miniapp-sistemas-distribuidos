import socket 

msocket= socket.socket()
msocket.connect (('localhost', 8000))

txt_client = "Hola desde el cliente"
msocket.send(txt_client.encode("ascii"))

respuesta= msocket.recv(1024)
txt_recibido = respuesta.decode("ascii")

print (respuesta)
msocket.close()


#print('hola')