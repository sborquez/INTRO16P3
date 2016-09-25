import socket
import numpy
import random
from botplayer import *
battlefield = numpy.tile(0,(20,20))

def spawn(cliente):
    mensaje = cliente.recv(1024)
    posicion = mensaje.split(",")
    return int(posicion[0]), int(posicion[1])

#LOGIN
cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IP = raw_input("ingrese la ip ")
PORT = input("ingrese el puerto ")
cliente.connect( (IP ,PORT ) )
usuario = raw_input( "Ingrese nombre de usuario:" )
cliente.send( usuario )

#SPAWN INICIAL
posicion = spawn(cliente) 

juego = 1
while (juego):
    #RECIBIR ORDEN DEL SERVIDOR, Y EN BASE A ESO ACTUALIZAR NUESTRO ESTADO Y RESPONDER

    mensaje = cliente.recv(1024)

    #SI RECIBE UNA AMENAZA ESTAMOS OK, SE PROSIGUE CON ATACAR Y LUEGO MOVERSE

    if ( mensaje[0] == "a"):
        amenazas = mensaje
    #EN BASE A LA LISTA AMENAZAS, TOMAR UNA DECISION
    disparo_x, disparo_y = disparar( random.randint(1,len( amenazas.split("-") ) ) )
    #ESCOGER UN MOVIMIENTO
    posicion_x, posicion_y = mover( (posicion[0],posicion[1]) )
    #ENVIAR MOVIMIENTO
    cliente.send(str(disparo_x)+","+str(disparo_y)+"-"+str(posicion_x)+","+str(posicion_y) )
    #IF MUERTO --> RE-SPAWN
    #IF GAME OVER --> BREAK    
cliente.close()
