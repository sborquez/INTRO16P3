import socket
from botdummy import *
import numpy
import random

IP = "localhost"
PORT = 0000
NJ = 1     #Numero de jugadores


"""
    Funciones utilizadas:
    
    conectar
    Recibe todas las conexiones entrantes, y relaciona cada conexion con un nombre
    jugador

    spawn_all
    Situa a todos los jugadores en la matriz battlefield, y envia respectivas posiciones
    a cada jugador

"""
def generar_id(conexiones_entrantes):
    while (1):
        id = random.randint(0,100)
        if not ( id in conexiones_entrantes) :
            return id

def conectar(server):
    conexiones_entrantes = dict()
    while( len (conexiones_entrantes) < NJ ):
        socket_o, socket_info = server.accept()
        nombre_usuario = socket_o.recv(1024)
        id = generar_id( conexiones_entrantes )
        conexiones_entrantes[ id ] = (socket_o,socket_info,nombre_usuario)
        print "Conexion exitosa!"
    print "Todos se han conectado"
    return conexiones_entrantes


def spawn_all( battlefield , conexiones_entrantes ):
    stats = dict()
    for id in conexiones_entrantes:
        socket_o = conexiones_entrantes[id][0]
        jugador = conexiones_entrantes[id][2]
        x, y = spawn( battlefield )
        stats[ id ] =(jugador,3,3,(x,y)) #nombre,vidas, y turnos restantes
        battlefield[x][y] = id
        print jugador," ha sido situado en "+str(x)+","+str(y)
        socket_o.send(str(x)+","+str(y))
    return stats

"""
    Estructuras utilizadas:
    conexiones entrantes es un diccionario cuyas llaves son el nombre del jugador, 
    y el valor es una tupla con un objeto socket y una tupla de ip, puerto.
    >>> conexiones_entrantes
    {'nombre jugador':( socket_jugador, ( ip,puerto ))}
    
    stats es un diccionario cuyas llaves son el nombre del jugador, 
    y el valor es una tupla con las vidas, los turnos restantes, 
    y una tupla coordenadas.
    >>> stats
    {'id':(nombre_jugador,vidas, turnos restantes,(x,y))}

    battlefield es un np.array con valores 0 indicando espacios vacios, 
    y en los espacios en que estan situados los jugadores estan marcados 
    por sus respectivos nombres de jugador.
    >>> battlefield
    [[0,0,0],
     ['nombre_jugador_1',0,0],
     [0,nombre_jugador_2,0]]

"""


battlefield = numpy.tile(0,(20,20))
servidor = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
servidor.bind( (IP,PORT ) )
print servidor.getsockname()
servidor.listen(NJ)
print "Esperando Conexiones"
conexiones_entrantes = conectar(servidor)
stats = spawn_all( battlefield, conexiones_entrantes )
print stats, "\n-------\n", conexiones_entrantes
juego = 1

while ( juego ):
    for id in conexiones_entrantes:
        jugador = conexiones_entrantes[id][2]
        socket_o = conexiones_entrantes[id][0]
        print "Alertando a ", jugador
        posicion = stats[id][3]
        socket_o.send( estimar_amenaza(posicion, battlefield) )
        print "Esperando accion de ", jugador
        mensaje_recibido = socket_o.recv(1024)
servidor.close()

