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

def mover ( posicion ):
    
    delta = escoger(3)
    if ( random.randint(0,1) ):
        posicion = posicion[0],periodico(posicion[1]+delta)
        return posicion
        
    posicion = periodico( posicion[0]+1 ), posicion[1]
    return posicion

def disparar ( amenaza ):
    delta = escoger( amenaza )
    if( random.randint(0,1) ):
        return delta,0 
    return 0,delta

def estimar_amenaza ( posicion,battlefield ):
    amenazas = "a"
    for i in xrange(2):
        for j in [-5,-4,-3,-2,-1,1,2,3,4,5]:
            if (i == 0):
                if ( battlefield [ periodico ( posicion[i]+j)][1] == 1 ):
                    amenazas+="-"+str(amenaza (j)) 
            else:
                if ( battlefield [0][ periodico ( posicion[i]+j ) ] == 1 ):
                    amenazas+="-"+str( amenaza (j) )
        return amenazas
