import socket
from botdummy import *

def spawn(cliente):
    mensaje = cliente.recv(1024)
    posicion = mensaje.split(",")
    return int(posicion[0]), int(posicion[1])

cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IP = raw_input("ingrese la ip ")
PORT = input("ingrese el puerto ")
cliente.connect( (IP ,PORT ) )
cliente.send( "dummy" )
posicion = spawn(cliente) 

juego = 1
while (juego):

    mensaje = cliente.recv(1024)
    disparo = escoger_disparo( mensaje )
    movimiento = escoger_movimiento()
    mensaje = disparo + "/" + movimiento
    cliente.send( mensaje )

cliente.close()
