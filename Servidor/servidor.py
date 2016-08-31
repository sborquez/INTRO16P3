import socket
import dummy_bot
import threading

def conectar():
    conexiones_entrantes = list()
    while( len (conexiones_entrantes) < 3 ):
        conexiones_entrantes.append( server.accept() )
        print "Conexion exitosa!"
    print "Todos se han conectado"
    return conexiones_entrantes


servidor = socket.socket()
servidor.bind( (' ',0 ) )
print servidor.getsockname()
servidor.listen(2)
print "Esperando Conexiones"
conexiones_entrantes = conectar()
servidor.close()

# iniciar juego
tamanno_battlefield = 10
battlefield = numpy.tile( 0, (n,n) )
