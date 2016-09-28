import socket
import numpy
from control import *
import random

IP = "localhost"
PORT = 0000
NJ = 1   #Numero de jugadores

if (NJ < 5):
    SIZE = 10
elif (NJ < 10):
    SIZE = 15
else:
    SIZE = 20

"""
    Funciones utilizadas:
    
    conectar
    Recibe todas las conexiones entrantes, y relaciona cada conexion con un nombre
    jugador

    spawn_all
    Situa a todos los jugadores en la matriz battlefield, y envia respectivas posiciones
    a cada jugador

"""

def matar( conexiones_entrantes, stats, id,jugador):
    del conexiones_entrantes[id]
    del stats[id]
    print "Se ha eliminado a ", jugador

def generar_id(conexiones_entrantes):
    while (1):
        id = random.randint(0,100)
        if not ( id in conexiones_entrantes) :
            return id

def conectar(server):
    log.append("juego:cargar")
    conexiones_entrantes = dict()
    while( len (conexiones_entrantes) < NJ ):
        socket_o, socket_info = server.accept()
        nombre_usuario = socket_o.recv(1024)
        id = generar_id( conexiones_entrantes )
        conexiones_entrantes[ id ] = (socket_o,socket_info,nombre_usuario)
        log.append("conectado:"+str(id))
        print "Conexion exitosa!"
    print "Todos se han conectado"
    return conexiones_entrantes


def spawn_all( battlefield , conexiones_entrantes ):
    stats = dict()
    for id in conexiones_entrantes:
        socket_o = conexiones_entrantes[id][0]
        jugador = conexiones_entrantes[id][2]
        x, y = spawn( battlefield, SIZE)
        posicion = [x, y]
        stats[ id ] =[jugador,3,3,posicion]
        battlefield[x][y] = id
        log.append("aparecer:"+str(id)+","+str(x)+","+str(y))
        print jugador," ha sido situado en "+str(x)+","+str(y)
        socket_o.send(str(x)+","+str(y))
    return stats

"""
    Estructuras utilizadas:
    conexiones entrantes es un diccionario cuyas llaves son el id del jugador, 
    y el valor es una tupla con un objeto socket,una tupla de ip, puerto, y el nombre del jugador.
    >>> conexiones_entrantes
    {'id':( socket_jugador, ( ip,puerto ),nombre_jugador)}
    
    stats es un diccionario cuyas llaves son el nombre del jugador, 
    y el valor es una tupla con las vidas, los turnos restantes, 
    y una tupla coordenadas.
    >>> stats
    {'id':(nombre_jugador,vidas, turnos restantes,(x,y))}

    battlefield es un np.array con valores 0 indicando espacios vacios, 
    y en los espacios en que estan situados los jugadores estan marcados 
    por sus respectivos id de jugador.
    >>> battlefield
    [[0,0,0],
     ['id_jugador_1',0,0],
     [0,id_jugador_2,0]]

"""

log = list()
battlefield = numpy.tile(0,(SIZE,SIZE))
servidor = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
servidor.bind( (IP,PORT ) )
print servidor.getsockname()
servidor.listen(NJ)
print "Esperando Conexiones"
conexiones_entrantes = conectar(servidor)
stats = spawn_all( battlefield, conexiones_entrantes )
print stats, "\n-------\n", conexiones_entrantes,"\n--------\n",battlefield
juego = 1
log.append("juego:comenzar")
while ( juego ):
    if ( len(conexiones_entrantes) == 0):
        break 
    for id in conexiones_entrantes.keys():
        jugador = conexiones_entrantes[id][2]
        socket_o = conexiones_entrantes[id][0]
        log.append("alertar:"+str(id))
        posicion = stats[id][3]
        x0, y0 = posicion[0], posicion[1]
        print "Alertando a ", jugador
        amenaza = estimar_amenaza(posicion, battlefield, SIZE)
        socket_o.send( amenaza )
        print "Esperando accion de ", jugador
        mensaje_recibido = socket_o.recv(1024)
        
        disparo = map(int,(mensaje_recibido.split("/")[0]).split(","))
        if not validar_disparo( disparo ):
            battefield[x0][y0] = 0
            matar(conexiones_entrantes,stats, id, jugador)
            print jugador," ha cometido disparo fuera de rango"

        #evaluar_disparo( battlefield, disparo)
        movimiento = map(int,(mensaje_recibido.split("/")[1]).split(","))
        if not validar_movimiento( movimiento ):
            matar(conexiones_entrante, stats, id , jugador)
            battefield[x0][y0] = 0
            print jugador," ha cometido un movimiento fuera de rango"

        disparo = posicion[0] + disparo[0], posicion[1] + disparo[1]
        posicion = posicion[0] + movimiento[0], posicion[1] + movimiento[1]
        print disparo, posicion
        disparo = limites( disparo, SIZE)
        posicion = limites( posicion, SIZE)
        log.append("") #disparo
        
        estado = evaluar_disparo(battlefield, posicion)
        if ( estado ):
            x, y = disparo[0], disparo[1]
            id_golpeado = battlefield[x][y]
            stats[id_golpeado][1] = stats[id_golpeado][1] -1
            stats[id][2] = stats[id][2] +1
        else:
            stats[id][2] = stats[id][2] -1

        estado = evaluar_movimiento(battlefield, posicion)
        if ( estado ):
            x1, y1  = posicion[0], posicion[1]
            battlefield[x0][y0] = 0
            stats[id][3] = x1, y1
            battlefield[x1][y1] = id
            log.append("") #se movio
        else:
            x1, y1  = posicion[0], posicion[1]
            id_golpeado = battlefield[x1][y1]
            print jugador, " ha chocado a ", stats[id_golpeado][0]," ", jugador," sera destruido"
            log.append("") #se murio1
            matar( conexiones_entrantes, stats, id,jugador)
            battlefield[x0][y0] = 0
            stats[id_golpeado][1]-=1
        for id in stats.keys():
            if ( stats[id][2] == 0 ):
                stats[id][1] = stats[id][1]-1;
                stats[id][2] = 3;
            if ( stats[id][1] == 0 ):
                matar( conexiones_entrantes, stats, id,jugador)

servidor.close()
log.append("juego:terminar")
