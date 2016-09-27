def validar_movimiento( movimiento ):
    posibles_movimientos = {(1,0),(-1,0),(0,1),(0,-1)}
    movimiento = movimiento[0], movimiento[1]
    return movimiento in posibles_movimientos

def validar_disparo( disparo ):
    posibles_disparos = {( -5 ,0),( -4 ,0),( -3 ,0),( -2 ,0),( -1 ,0),( 1 ,0),( 2 ,0),( 3 ,0),( 4 ,0),( 5 ,0),(0, -5 ),(0, -4 ),(0, -3 ),(0, -2 ),(0, -1 ),(0, 1 ),(0, 2 ),(0, 3 ),(0, 4 ),(0, 5 )}
    disparo =  disparo[0], disparo[1]
    return disparo in posibles_disparos


def limites( coordenada , limite):
    for i in coordenada:
        if (i >= limite):
            coordenada[i] = coordenada[i] - limite
    return coordenada

def evaluar_disparo(  battlefield, coordenada ):
    if ( battlefield[x][y] != 0 ):
        return True
    else: 
        return False

def evaluar_movimiento(battlefield, coordenada):
    if (battlefield[x][y] == 0):
        return True
    else:
        return False

