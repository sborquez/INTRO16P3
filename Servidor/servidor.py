import socket
import dummy_bot
import threading

def conectar():
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
        conexiones_entrantes[jugador].send(str(x)+","+str(y))
    return stats

battlefield = numpy.tile(0,(20,20))
servidor = socket.socket()
servidor.bind( (' ',0 ) )
print servidor.getsockname()
servidor.listen(2)
print "Esperando Conexiones"
conexiones_entrantes = conectar()
stats = spawn_all( battlefield, conexiones_entrantes )
juego = 1

while ( juego ):
    for jugador in conexiones_entrantes:
        conexiones_entrantes[jugador].send("amenazas: \n")
        for amenaza in  estimar_amenaza (stats[jugador[2], battlefield):
            conexiones_entrantes[jugador].send( str(amenaza)+"\n" )
        conexiones_entrantes[jugador].send("fin\n")

servidor.close()

