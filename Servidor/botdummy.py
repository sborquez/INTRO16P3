import numpy
import random

def escoger ( accion ):
    if ( accion == 3 ):
        l = [-1,1]
        return random.choice(list(l))
    elif( accion == 1 ):
        l = [-5,-4,4,5]
        return random.choice(list(l))
    elif( accion == 2 ):
        l = [-3,-2,2,3]
        return random.choice(list(l))

def periodico ( r ):
    if ( r >= 20 ): return (20-r)
    return r

def amenaza ( valor ):
    l = [3,3,2,2,1]
    return l [ abs ( valor ) -1 ]

def mover ( posicion, battlefield ):
    
    delta = escoger(3)
    battlefield[ posicion[0], posicion[1] ] = 0
    
    if ( random.randint(0,1) ):
        posicion = posicion[0],periodico(posicion[1]+delta)
        battlefield[ posicion[0], posicion[1] ] = 1
        return posicion,battlefield
        
    posicion = periodico( posicion[0]+1 ), posicion[1]
    battlefield[ posicion[0], posicion[1] ] = 1
    return posicion,battlefield

def disparar ( amenaza, posicion ):
    delta = escoger( amenaza )
    if( random.randint(0,1) ):
        return posicion[0]+delta
    return posicion[1]+delta

def estimar_amenaza ( posicion,battlefield ):
    amenazas = list()
    for i in xrange(2):
        for j in [-5,-4,-3,-2,-1,1,2,3,4,5]:
            if (i == 0):
                if ( battlefield [ periodico ( posicion[i]+j)][1] == 1 ):
                    amenazas.append( amenaza (j) )
            else:
                if ( battlefield [0][ periodico ( posicion[i]+j ) ] == 1 ):
                    amenazas.append( amenaza (j) )
    return [1,2,3]
    return amenazas

def spawn( battlefield ):
    while (1):
        x , y = random.randint(0,19), random.randint(0,19)
        if ( battlefield[x][y] == 0 ):
            return x,y

