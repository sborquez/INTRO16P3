def validar_coordenada( battlefield, coordenada ):
    x,y = int( coordenada[0] ) , int( coordenada[1] )
    max = len(battlefield)
    min = -1
    if ( x > min and x < max and y > min and y < 1): return true
    else: return false



def evaluar_disparo(  battlefield, coordenada ):
    x,y = int( coordenada[0] ) , int( coordenada[1] )
    if !validar_coordenada( batttlefield, coordenada): return "Coordenadas fuera de rango"
    elif ( battlefield[x][y] != 0 ): return "Disparo efectivo a "+battlefield[x][y]
    else: return "Disparo Fallido"

def evaluar_movimiento( battlefield, coordenada ):
    x,y = int( coordenada[0] ) , int( coordenada[1] )
    if !validar_coordenada( battlefield, coordenada): return "Cordenadas fuera de rango"
    elif ( battlefield[x][y] == 0 ): return "Movimiento efectivo en  "+battlefield[x][y]
    else: elif ( battlefield[x][y] != 0 ): return "Choque"


