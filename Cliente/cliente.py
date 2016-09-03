import socket
import numpy
import random
from botplayer import *
battlefield = numpy.tile(0,(20,20))

#LOGIN
cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IP = raw_input("ingrese la ip ")
PORT = input("ingrese el puerto ")
cliente.connect( (IP ,PORT ) )
usuario = raw_input( "Ingrese nombre de usuario:" )
cliente.send( usuario )

#SPAWN
mensaje = cliente.recv(1024)
posicion = mensaje.split(",")
print posicion
posicion_x = int(posicion[0])
posicion_y = int(posicion[1])
battlefield[posicion_x][posicion_y] = 1

juego = 1
while (juego):
    mensaje = cliente.recv(1024)
    if ( mensaje[0] == "a"):
        amenazas = mensaje
    #EN BASE A LA LISTA AMENAZAS, TOMAR UNA DECISION
    disparo_x, disparo_y = disparar( random.randint(1,len( amenazas.split("-") ) ) )
    #ESCOGER UN MOVIMIENTO
    posicion_x, posicion_y = mover( (posicion_x,posicion_y) )
    #ENVIAR MOVIMIENTO
    cliente.send(str(disparo_x)+","+str(disparo_y)+"-"+str(posicion_x)+","+str(posicion_y) )
    
cliente.close()
