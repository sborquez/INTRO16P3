import socket
from botdummy import *
import numpy
from control import *
import random

IP = "localhost"
PORT = 0000
NJ = 2   #Numero de jugadores


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
        x, y = spawn( battlefield )
        stats[ id ] =(jugador,3,3,(x,y)) #nombre,vidas, y turnos restantes
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
battlefield = numpy.tile(0,(20,20))
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
    for id in conexiones_entrantes:
        jugador = conexiones_entrantes[id][2]
        socket_o = conexiones_entrantes[id][0]
        log.append("alertar:",str(id))
        print "Alertando a ", jugador
        posicion = stats[id][3]
        socket_o.send( estimar_amenaza(posicion, battlefield) )
        print "Esperando accion de ", jugador
        mensaje_recibido = socket_o.recv(1024)
        
        disparo = (mensaje_recibido.split("-")[0]).split(",")
        evaluar_disparo( battlefield, disparo)
        posicion = (mensaje_recibido.split("-")[1]).split(",")
        posicion[0] = int(posicion[0])
        posicion[1] = int(posicion[1])
        disparo[0] = int(disparo[0])
        disparo[1] = int(disparo[1])
        log.append("") #disparo

        estado = evaluar_movimiento(battlefield, posicion)
        if ( estado = "D"):
            stats[battlefield[disparo[x]][disparo[y]]][1]-=1

        estado = evaluar_movimiento(battlefield, posicion)
        if ( estado == "M"):
            battlefield[stats[id][3][0]][stats[id][3][1]] = 0
            battlefield[posicion[x]][posicion[y]] = id
            log.append("") #se movio
        elif ( estado = "C"):
            log.append("") #se murio1
            log.append("") #se murio2
            del conexiones_entrantes[id]
            del conexiones_entrantes[battlefield[posicion[x]][posicion[y]]]
            battlefield[stats[id][3][0]][stats[id][3][1]] = 0
            battlefield[posicion[x]][posicion[y]] = 0
            stats[battlefield[disparo[x]][disparo[y]]][2]-=1
        
       stats, conexiones_entrantes, log =  fin_turno(stats, conexiones, log)

servidor.close()
log.append("juego:terminar")
