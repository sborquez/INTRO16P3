import socket
import botdummy
import numpy
import threading

"""
    Funciones utilizadas:
    
    conectar
    Recibe todas las conexiones entrantes, y relaciona cada conexion con un nombre
    jugador

    spawn_all
    Situa a todos los jugadores en la matriz battlefield, y envia respectivas posiciones
    a cada jugador

"""

def conectar(server):
    conexiones_entrantes = dict()
    while( len (conexiones_entrantes) < 3 ):
        socket_o, socket_info = server.accept()
        socket_o.send("Ingrese nombre usuario\n")
        nombre_usuario = socket_o.recv(1024)
        conexiones_entrantes[ nombre_usuario ] = (socket_o,socket_info)
        print "Conexion exitosa!"
    print "Todos se han conectado"
    return conexiones_entrantes


def spawn_all( battlefield , conexiones_entrantes ):
    stats = dict()
    for jugador in conexiones_entrantes:
        x, y = spawn(battlefield)
        stats[ jugador ] =(3,3,(x,y)) #vidas, y turnos restantes
        battlefield[x][y] = jugador
        print jugador," ha sido situado en "+str(x)+","+str(y)
        conexiones_entrantes[jugador][0].send(str(x)+","+str(y))
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
    {'nombre_jugador':(vidas, turnos restantes,(x,y))}

    battlefield es un np.array con valores 0 indicando espacios vacios, 
    y en los espacios en que estan situados los jugadores estan marcados 
    por sus respectivos nombres de jugador.
    >>> battlefield
    [[0,0,0],
     ['nombre_jugador_1',0,0],
     [0,nombre_jugador_2,0]]
"""


battlefield = numpy.tile(0,(20,20))
servidor = socket.socket()
servidor.bind( ('',0 ) )
print servidor.getsockname()
servidor.listen(2)
print "Esperando Conexiones"
conexiones_entrantes = conectar(servidor)
stats = spawn_all( battlefield, conexiones_entrantes )

juego = 1

while ( juego ):
    for jugador in conexiones_entrantes:
        print "Alertando a ", jugador
        conexiones_entrantes[jugador].send("amenazas: \n")
        for amenaza in  estimar_amenaza(stats[jugador[2]], battlefield):
            conexiones_entrantes[jugador][0].send( str(amenaza)+"\n" )
        conexiones_entrantes[jugador][0].send("fin\n")
        print "Esperando movimiento de ", jugador
        mensaje_recibido = conexiones_entrantes[jugador][0].recv(1024)
        #Validar movimiento y actualizar matriz
        mensaje_recibido = conexiones_entrantes[jugador][0].recv(1024)
        #Validar disparo y actualizar matriz
        

servidor.close()

