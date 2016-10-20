#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Escrito por GasparCorrea
# gasparcorreavergara@gmail.com

import socket, numpy, random, time, sys
from control import *

"""
    Aqui deben asignar valores para configurar la partida a su gusto
    IP: localhost para ejecutar en el mismo computador. Colocar IP del computador para jugar en LAN.
    PORT: 0 buscara cualquier puerto disponible
    NJ: Cantidad de bots que participaran en la partida
"""
IP = "localhost" 
PORT = 0 
NJ = 2

if (NJ <= 5):
    SIZE = 11
elif (NJ <= 10):
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
    a cada jugadori

    matar
    Elimina la conexion con un jugador de la partida

    generar_id
    Asigna a cada usuario un id numérico, se usa para identificar al jugador internamente

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

def conectar(server, log):
    log.append("juego:cargar")
    conexiones_entrantes = dict()
    i = 1
    while( len (conexiones_entrantes) < NJ ):
        socket_o, socket_info = server.accept()
        nombre_usuario = socket_o.recv(1024)
        id = generar_id( conexiones_entrantes )
        conexiones_entrantes[ id ] = (socket_o,socket_info,nombre_usuario)
        log.append("conectado:"+nombre_usuario)
        print str(i) + '/' + str(NJ), " - Conexion exitosa de", nombre_usuario ,"!", 
        print "(IP: ", socket_info[0] + ')'
        i += 1
    print "Todos se han conectado"
    return conexiones_entrantes


def spawn_all( battlefield , conexiones_entrantes, log):
    stats = dict()
    for id in conexiones_entrantes:
        socket_o = conexiones_entrantes[id][0]
        jugador = conexiones_entrantes[id][2]
        x, y = spawn( battlefield, SIZE)
        posicion = [x, y]
        stats[ id ] =[jugador,3,3,posicion]
        battlefield[x][y] = id
        log.append("aparecer:"+jugador+","+str(x)+","+str(y))
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
#Muy importante revisar el log una vez terminada la partida, el log entrega un resumen de lo que resulto la partida
log = list()
title = time.strftime("%c").replace(" ","_")
log.append("#TITLE;"+str(title)+"/"+str(SIZE))
title = title.replace(":","_").replace("/","-")
battlefield = numpy.tile(0,(SIZE,SIZE))
servidor = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

servidor.bind( (IP, PORT) ) 
# Indica a que IP y PORT deben conectarse los clientes
print servidor.getsockname()
servidor.listen(NJ)
print "Esperando Conexiones"
conexiones_entrantes = conectar(servidor, log)
log.append("juego:comenzar")
stats = spawn_all( battlefield, conexiones_entrantes, log)
print stats, "\n-------\n", conexiones_entrantes,"\n--------\n",battlefield
juego = 1

try:
    while ( juego ):
        if ( len(conexiones_entrantes) == 0):
            break 
        for id in conexiones_entrantes.keys():
            # por si un id fue ya eliminado por ataque de otro jugador
            if id not in conexiones_entrantes:
                continue
            jugador = conexiones_entrantes[id][2]
            socket_o = conexiones_entrantes[id][0]
            #log.append("alertar:"+str(id))
            posicion = stats[id][3]
            x0, y0 = posicion[0], posicion[1]
            #print "Alertando a ", jugador
            amenaza = estimar_amenaza(posicion, battlefield, SIZE)
            socket_o.send( amenaza )
            print "Turno de", jugador
            mensaje_recibido = socket_o.recv(1024)
            # si el mensaje es vacio, el usuario se desconecto
            if not len(mensaje_recibido):
                log.append("desconectar:{ID}".format(ID=jugador))
                matar(conexiones_entrantes,stats, id, jugador)
                continue
            
            disparo = map(int,(mensaje_recibido.split("/")[0]).split(","))
            if not validar_disparo( disparo ):
                battlefield[x0][y0] = 0
                log.append("desconectar:{ID}".format(ID=jugador))
                matar(conexiones_entrantes,stats, id, jugador)
                print jugador, "ha cometido disparo fuera de rango"

            movimiento = map(int,(mensaje_recibido.split("/")[1]).split(","))
            if not validar_movimiento( movimiento ):
                matar(conexiones_entrantes, stats, id , jugador)
                log.append("desconectar:{ID}".format(ID=jugador))
                battlefield[x0][y0] = 0
                print jugador, "ha cometido un movimiento fuera de rango"

            disparo = posicion[0] + disparo[0], posicion[1] + disparo[1]
            posicion = posicion[0] + movimiento[0], posicion[1] + movimiento[1]
            print disparo, posicion
            disparo = limites( disparo, SIZE)
            posicion = limites( posicion, SIZE)
            
            estado = evaluar_disparo(battlefield, disparo)
            x, y = disparo[0], disparo[1]
            if ( estado ):
                id_golpeado = battlefield[x][y]
                stats[id_golpeado][1] -= 1
                stats[id][2] += 1
                stats[id][1] += 1
                jugador2 = stats[id_golpeado][0]
                log.append("disparar:{ID},{X},{Y},{ID2}".format(ID=jugador, X=x,Y=y,ID2=jugador2))
                log.append("muerte:{ID}".format(ID=jugador2))
                if ( stats[id_golpeado][1] == 0 ):
                    battlefield[x][y] = 0
                    log.append("desconectar:{ID}".format(ID=jugador2))
                    matar( conexiones_entrantes, stats, id_golpeado ,jugador2)
                else:
                    log.append("aparecer:"+jugador2+","+str(x)+","+str(y))
            else:
                stats[id][2] = stats[id][2] - 1
                log.append("disparar:{ID},{X},{Y},{OBJ}".format(ID=jugador, X=x,Y=y,OBJ="None"))
                # pierde vida al llegar a turno 0, los turnos se reinician
                if ( stats[id][2] == 0 ):
                    stats[id][1] -= 1
                    stats[id][2] = 3
                    # si las vidas llegan a 0, se desconecta
                    if ( stats[id][1] == 0 ):
                        x, y = stats[id][3]
                        battlefield[x][y] = 0
                        log.append("desconectar:{ID}".format(ID=jugador))
                        matar( conexiones_entrantes, stats, id ,jugador)
                        continue          

            estado = evaluar_movimiento(battlefield, posicion)
            if ( estado ):
                x1, y1  = posicion[0], posicion[1]
                battlefield[x0][y0] = 0
                stats[id][3] = x1, y1
                battlefield[x1][y1] = id
                log.append("moverse:{ID},{X},{Y}".format(ID=jugador, X=x1,Y=y1))
            else:
                x1, y1  = posicion[0], posicion[1]
                id_golpeado = battlefield[x1][y1]
                print jugador, "ha chocado a", stats[id_golpeado][0]
                battlefield[x0][y0] = 0
                stats[id_golpeado][1] -= 1
                jugador2 = stats[id_golpeado][0]
                log.append("colision:{ID}".format(ID = jugador))
                log.append("colision:{ID}".format(ID = jugador2))
                matar( conexiones_entrantes, stats, id,jugador)
                log.append("desconectar:{ID}".format(ID=jugador))
                # para que vuelva a mostrar imagen de jugador colisionado
                log.append("moverse:{ID},{X},{Y}".format(ID=jugador2, X=x1,Y=y1))
                if ( stats[id_golpeado][1] == 0 ):
                    battlefield[x1][y1] = 0
                    log.append("desconectar:{ID}".format(ID=jugador2))
                    matar( conexiones_entrantes, stats, id_golpeado, jugador2)     

except KeyboardInterrupt:
    print "STOP IT!"

except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print "Line", exc_tb.tb_lineno,
    print "Unexpected error:", type(e), "Argumentos",e.args

servidor.close()
log.append("juego:terminar")
with open("../Visualizacion/logs/"+title+".log","w") as log_file:
    for linea in log:
        log_file.write(linea+"\n")


