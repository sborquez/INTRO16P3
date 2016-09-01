import socket

cliente = socket.socket()
IP = raw_input("ingrese la ip ")
PORT = input("ingrese el puerto ")
cliente.connect( (IP ,PORT ) )
usuario = raw_input( "Ingrese nombre de usuario:" )
cliente.send( usuario )
posicion = cliente.recv(1024)
print posicion
cliente.close()
