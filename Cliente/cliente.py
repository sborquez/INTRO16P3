import socket
import numpy

#ESTA ES TU MATRIZ DE COORDENADAS, ES TU RESPONSABILIDAD ADMINISTRARLA
battlefield = numpy.tile(0,(20,20))

#LOGIN
cliente = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IP = raw_input("ingrese la ip ")
PORT = input("ingrese el puerto ")
cliente.connect( (IP ,PORT ) )
usuario = raw_input( "Ingrese nombre de usuario:" )
cliente.send( usuario )

#POSICION SPAWN ENTREGADA POR EL SERVIDOR
mensaje = cliente.recv(1024)
juego = 1
while (juego):
    mensaje = cliente.recv(1024)
    if ( mensaje[0] == "a"):
        amenazas = mensaje
    print amenazas
    x = input()
     #EN BASE A LA LISTA AMENAZAS, TOMAR UNA DECISION
    
    #ESCOGER UN MOVIMIENTO
    #ENVIAR MOVIMIENTO

    
cliente.close()
