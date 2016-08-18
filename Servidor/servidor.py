import socket
import dummy_bot

servidor = socket.socket()
servidor.bind( ( "10.10.9.13",6969 ) )
servidor.listen(1)
socket_cliente, datos_cliente = servidor.accept()
servidor.close()

# iniciar juego
tamanno_battlefield = 10
battlefield = numpy.tile( 0, (n,n) )
