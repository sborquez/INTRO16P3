import socket
from random import randint
from botdummy import *

def spawn(cliente):
    mensaje = cliente.recv(1024)
    posicion = mensaje.split(",")
    return int(posicion[0]), int(posicion[1])
print "Conectado"
cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
#IP = raw_input("ingrese la ip ")
#PORT = input("ingrese el puerto ")
IP,PORT = "localhost",8888
cliente.connect( (IP ,PORT ) )
name  = randint(0,991)
cliente.send( "dummy{0}".format(name) )
posicion = spawn(cliente) 

juego = 1
print "Start"
try:
    while (juego):

        mensaje = cliente.recv(1024)
        disparo = escoger_disparo( mensaje )
        movimiento = escoger_movimiento()
        mensaje = disparo + "/" + movimiento
        cliente.send( mensaje )
except socket.error:
    cliente.close()
    print "GAME OVER"

