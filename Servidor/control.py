def validar_coordenada(battlefield, coordenada):
    x,y = int(coordenada[0]), int(coordenada[1])
    max = len(battlefield)
    min = -1
    if ( x > min and x < max and y > min and y < 1): return true
    else: return false

def evaluar_disparo(  battlefield, coordenada):
    if (validar_coordenada(batttlefield, coordenada) == false): return "Coordenadas fuera de rango"
    elif (battlefield[x][y] != 0): return "D"
    else: return "W"

def evaluar_movimiento(battlefield, coordenada):
    if (validar_coordenada(batttlefield, coordenada) == false): return "Coordenadas fuera de rango"
    elif (battlefield[x][y] == 0):
        return "M"
    elif (battlefield[x][y] != 0): return "C"

def actualizar_matriz(battlefield, coordenada, user):
    x,y = int(coordenada[0]), int(coordenada[1])
    if (validar_coordenada(battlefield, coordenada) and battlefield[x][y] == 0):
        battlefield[x][y]=user
    else:
        return "Error de actualizacion"

def fin_turno( stats, conexiones, log ):
    for id in stats:
        if (stats[id][1] == 0):
            del conexiones[id]
            log.append("")
        elif (stats[id][2] == 0):
            stats[id][1]-=1
    return stats, conexiones, log
