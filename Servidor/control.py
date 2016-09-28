import random

def validar_movimiento( movimiento ):
    posibles_movimientos = {(1,0),(-1,0),(0,1),(0,-1)}
    movimiento = movimiento[0], movimiento[1]
    return movimiento in posibles_movimientos

def validar_disparo( disparo ):
    posibles_disparos = {( -5 ,0),( -4 ,0),( -3 ,0),( -2 ,0),( -1 ,0),( 1 ,0),( 2 ,0),( 3 ,0),( 4 ,0),( 5 ,0),(0, -5 ),(0, -4 ),(0, -3 ),(0, -2 ),(0, -1 ),(0, 1 ),(0, 2 ),(0, 3 ),(0, 4 ),(0, 5 )}
    disparo =  disparo[0], disparo[1]
    return disparo in posibles_disparos


def limites( coordenada , limite):
    coordenada = [coordenada[0], coordenada[1]]
    for i in range(0,2):
        if (coordenada[i] >= limite):
            coordenada[i] = coordenada[i] - limite
    return coordenada

def evaluar_disparo(  battlefield, coordenada ):
    x, y = coordenada[0], coordenada[1]
    if ( battlefield[x][y] != 0 ):
        return True
    else: 
        return False

def evaluar_movimiento(battlefield, coordenada):
    x, y = coordenada[0], coordenada[1]
    if (battlefield[x][y] == 0):
        return True
    else:
        return False

def periodico ( r ,SIZE):
    if ( r >= SIZE ): return (SIZE-r)
    return r

def amenaza ( valor ):
    l = [3,3,2,2,1]
    return l [ abs ( valor ) -1 ]

def estimar_amenaza ( posicion,battlefield ,SIZE):
    amenazas = "a"
    for i in xrange(2):
        for j in [-5,-4,-3,-2,-1,1,2,3,4,5]:
            if (i == 0):
                if ( battlefield [ periodico ( posicion[i]+j,SIZE)][1] == 1 ):
                    amenazas+="-"+str(amenaza (j)) 
            else:
                if ( battlefield [0][ periodico ( posicion[i]+j, SIZE ) ] == 1 ):
                    amenazas+="-"+str( amenaza (j) )
        return amenazas

def spawn( battlefield , SIZE):
    while (1):
        x , y = random.randint(0,SIZE-1), random.randint(0,SIZE-1)
        if ( battlefield[x][y] == 0 ):
            return x,y
