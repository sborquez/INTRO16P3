import os
import pygame
from random import randint, choice
from pygame.locals import *
from escenas import *
from time import sleep

TITULO = "Speis Guars"

#  Constantes de tamanhos para dibujar.
SPACESHIPS = 45
BATTLEFIELDSIZE = 460.0
BATTLEFIELDDIVISIONS = 20
BATTLEFIELDINICIO = (351, 10)
ESCALA = 4.0/BATTLEFIELDDIVISIONS

# Constantes de giro de las naves.
MOV = {"up": (0,  -1),
       "down": (0, 1),
       "left": (-1,  0),
       "rigth": (1,  0)}

SETH = {"up": 0,
        "down": 180,
        "left": 90,
        "rigth": -90}

# Constantes del juego
Q_turnos = 5
MAX_vidas = 5

# --------------------
# DEFINICION DE CLASES
# --------------------

# Clases de escenas.


class Inicio(Scene):

    """ Ventana de inicio del juego.
        Campos:
           background:      (image) Imagen de fondo.
           start_replay:    (bool) Comenzar a reproducir el replay.
           replay:          (list(string)) Lineas del archivo log.
           players:         (dict((ID:Jugador)) Contiene objetos Jugadores.
           colortxt:        (list(int,int, int))Color del texto en RGB."""

    def __init__(self, director, path_log):
        """Parametros.
            - director: Objeto MainFrame, manipulador del juego.
            - path_log: Directorio del fichero log que posee la partida."""

        Scene.__init__(self, director)

        # Informacion de escena
        # background: Imagen de fondo.
        background_path = os.path.join("data", "background", "portada.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        # start_replay: Comenzar a reproducir el replay.
        self.start_replay = False

        # Informacion del replay
        # replay: Lista de strings, lineas del archivo log.
        # players: Diccionario de clases Jugador (ID:Jugador).
        with open(path_log) as log:
            self.replay = log.readlines()
        self.players = cargar_jugadores(self.replay)

        # Musica
        musica_path = os.path.join("data", "music", "xeon6(intro).ogg")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(0, 0.0)

        # Texto
        # colortxt: Color del texto en RGB.
        self.colortxt = [0, 0, 0]

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """

        # Si se apreta space, se cambia de escena a la principal.
        if self.start_replay:
            pygame.mixer.music.stop()
            sfx_path = os.path.join("data", "sfx", "game_showmenu.wav")
            pygame.mixer.Sound(sfx_path).play()
            sleep(1)

            self.director.change_scene(Principal(self.director,
                                                 self.players,
                                                 self.replay))
        # Hacer parpadear el texto.
        self.colortxt = map(lambda x: x+4, self.colortxt)
        if self.colortxt[0] >= 255:
            self.colortxt = map(lambda x: 0, self.colortxt)
        self.textinscreen = fuenteL.render(
            "PRESIONE ESPACIO", 0, self.colortxt)

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. 
            Parametros:
                - event: Indica si se ha apretado 'espacio'."""

        if event:
            self.start_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla.
            Parametros:
                - screen: Ventana donde se dibuja."""
        screen.blit(self.background, (0, 0))
        screen.blit(self.textinscreen, (WIDTH/3, 5*HEIGHT/6))

        salir = fuenteS.render("ESC - Salir",
                               0, (255, 255, 255))
        fullscreen = fuenteS.render("F - fullscreen",
                                    0, (255, 255, 255))

        screen.blit(salir, (20, 10))
        screen.blit(fullscreen, (20, 20))


class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc.
        Campos:
            director:        (MainFrame), manipulador del juego.
            background:      (image) Imagen de fondo.
            replay:          (list(string)) Lineas del archivo log.
            linea:           (string) Linea leida actual de replay.
            next_turn:       (bool) Indica si se va ha leer una nueva linea.
            players:         (dict((ID:Jugador)) Contiene objetos Jugadores.
            colortxt:        (list(int,int, int))Color del texto en RGB.
            end_replay:      (bool) Indica si ha terminado el replay.
            acciones:        (list(strings) Pila de informacion ya leida.
            turnos_restantes:(int)turnos restantes para que termine el juego.
    """

    def __init__(self, director, dict_players, replay):
        """ Parametros:
                - director: Objeto MainFrame, manipulador del juego.
                - dict_players: Diccionario de clases Jugador (ID:Jugador).
                - replay: Lista de strings, lineas del archivo log."""

        Scene.__init__(self, director)
        # Informacion de escena
        # background: Imagen de fondo.
        background_path = os.path.join("data", "background", "tablero.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        # next_turn: Indica si se va ha leer una nueva linea del replay.
        # end_replay: Indica si ha terminado el replay.
        # linea: Linea leida de replay, es la accion actual.
        self.next_turn = True
        self.end_replay = False
        self.linea = ""

        # Informacion del replay
        # replay: Lista de strings, lineas del archivo log.
        # players: Diccionario de clases Jugador (ID:Jugador).
        self.replay = replay
        self.players = dict_players

        # HUD
        # sin uso aun
        self.sprites_UI = list()

        # Musica
        musica_path = os.path.join(
            "data", "music", "Arabesque(Main theme).ogg")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(100, 0.0)

        # Datos dibujo
        # acciones: Pila de informacion ya leida de replay.
        # turnos_restantes: turnos restantes para que termine el juego.
        self.acciones = ["", "", "", "", "", "", "", "", ""]
        self.turnos_restantes = Q_turnos

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """

        # Si se termino de leer la partida, pasar a los resultados.
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))

        # Si se termino de actualizar los datos de un turno, leer el siguiente.
        if self.next_turn:
            sleep(0.5)
            del self.acciones[-1]
            self.acciones.insert(0, "")
            self.next_turn = False
            linea = self.replay.pop(0)
            self.linea = linea.strip().split(":")
        accion, argumentos = self.linea
        discriminar_accion(self, accion, argumentos)

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal.
            Parametros:
                - event: Indica si se ha apretado 'espacio'."""

        # TEST
        if event:
            pygame.mixer.music.stop()
            self.end_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla.
            Parametros:
                - screen: Ventana donde se dibuja."""

        # Fondo
        screen.blit(self.background, (0, 0))

        # Cuadrilla
        dibujar_cuadricula(screen)

        # Mostrar la pila, historial de replay.
        for i, texto in enumerate(self.acciones):
            if i == 0:
                textinscreen = fuenteM.render(texto, 1, (255, 255, 255))
                screen.blit(textinscreen, (15, 90))
            else:
                textinscreen = fuenteS.render(texto, 1, (255, 255, 255))
                screen.blit(textinscreen, (15, 85-i*10))

        # Jugadores
        coor_y = 150
        coor_x = 20
        for ide, jugador in self.players.items():
            jugador.mostrar_tablero(screen)
            jugador.mostrar_marcador(screen, coor_x, coor_y)
            coor_y += 18
            if coor_y + 30 >= HEIGHT:
                coor_y = 150
                coor_x = 180


class Estadisticas(Scene):
    # TODO

    """ Ventana final del juego, muestra los resultados, tablas, etc.
        Campos:
            director:        (MainFrame), manipulador del juego.
            background:      (image) Imagen de fondo.
            players:         (dict((ID:Jugador)) Contiene objetos Jugadores.
    """

    def __init__(self, director, dict_players):
        """ Parametros:
                - director: Objeto MainFrame, manipulador del juego.
                - dict_players: Diccionario de clases Jugador (ID:Jugador)."""

        Scene.__init__(self, director)
        # Informacion de escena
        # backgound: Imagen de fondo.
        background_path = os.path.join("data", "background", "resultados.jpg")
        self.background = load_image(background_path)

        # Informacion del replay
        # players: Diccionario de clases Jugador (ID:Jugador).
        self.players = dict_players

        # Musica
        musica_path = os.path.join(
            "data", "music", "Victory and Respite(end).ogg")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(0, 0.0)

        self.info = dict()
        with open(path_log) as log:
            self.replay = log.readlines()
        
        # Agregamos los jugadores que ganaron en un diccionario
        # info = dict (id:list(int veces_muerto, int colisiones, 
        #              int disparos_efectivos, int disparos_fallidos))
        for line in self.replay:
            line = line.split(":")
            if line[0] == "resultado":
                self.info[line[1]] = [0,0,0,0]

        #Volvemos a recorrer la lista para contar las muertes y todo
        #lo necesario para hacer las estadisticas
        for line in self.replay:
            line = line.split(":")
            
            if linea[0] == "disparar":
                data = linea[1].split(",")
                if data[0] in self.info:
                    if data[2] != "None":
                        self.info[data[0]][2] += 1
                    else:
                        self.info[data[0]][3] += 1
            
            elif linea[0] == "colision":
                if linea[1] in self.info:
                    self.info[linea[0]][1] += 1
                    self.info[linea[0]][0] += 1

            elif linea[0] == "muerte":
                if linea[0] in self.info:
                    self.info[linea[0]][0] += 1
        """
        A la lista asociada a cada id_player se agrega un float efectividad, que corresponde 
        a ser el porcentaje de efectividad de los disparos de cada jugador.
        - efectividad negativa significa que falla mas tiros que los que acierta
        Despues de este for, la estructura del diccionario de los jugadores ganadores queda
        de la siguiente forma:
        info = dict (id:list(int veces_muerto, int colisiones, int disparos_efectivos, 
                    int disparos_fallidos, float efectividad_disparos))
        """
        for p_inf in self.info:
            efectividad_disparos = (self.info[p_inf][2] - self.info[p_inf][3])
            efectividad_disparos /= ((self.info[p_inf][2] + self.info[p_inf][3])*1.0)
            efectividad_disparos *=100
            efectividad_disparos = round(efectividad_disparos,1)
            self.info[p_inf].append(efectividad_disparos)

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """
        # TODO
        pass

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. """
        # TODO
        if event:
            self.start_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla."""

        # TODO
        
        ## Mostramos las estadisticas en la escena estadisticas
        
        screen.blit(self.background, (0, 0))

        title = fuenteL.render("Estadisticas",
                               0, (255, 255, 255))
        screen.blit(title, (115, 40))
        lin = 60
        i=1
        for plyr_inf in self.info:
            temp_str = ""
            if (i%7 == 1):
                temp_str = "ID jugador: "+plyr_inf+"\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))
            elif (i%7 == 2):
                temp_str = "Muertes: "+str(self.info[plyr_inf][0])+"\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))
            elif (i%7 == 3):
                temp_str = "Colisiones: "+str(self.info[plyr_inf][1])+"\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))
            elif (i%7 == 4):
                temp_str = "Disparos acertados: "+str(self.info[plyr_inf][2])+"\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))
            elif (i%7 == 5):
                temp_str = "Disparos fallidos: "+str(self.info[plyr_inf][3])+"\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))
            elif (i%7 == 6):
                temp_str = "Efectividad : "+str(self.info[plyr_inf][4])+"%\n\n"
                temporal = fuenteM.render(temp_str,
                                    0, (255, 255, 255))            
            screen.blit(temporal, (90, lin))
            lin +=20

# Clases de sprites.

class Jugador(pygame.sprite.Sprite):

    """ Informacion de un jugador.
        Campos:
            ID:                 (string) Identidicador del jugador.
            alerta:             (int) Estado de alerta.
            vidas:              (int) Cantidad de vidas.
            battlefieldpos_x:   (int) Posicion x de la matriz del juego.
            battlefieldpos_y:   (int) Posicion y de la matriz del juego.
            orientacion:        (int) Grados de orientacion, norte=0.
            images:             (list(images))Sprites de una nave.
            visible:            (int) indice, sprite de jugador."""

    def __init__(self, ID):
        """Parametros:
            - ID: string, identificador del jugador."""

        pygame.sprite.Sprite.__init__(self)
        # Datos jugador.
        self.ID = ID
        self.alerta = 0
        self.vidas = 2
        self.battlefieldpos_x = 0
        self.battlefieldpos_y = 0
        self.orientacion = 0

        # Datos dibujo.
        idspaceship = randint(0, SPACESHIPS-1)
        spaceship = choice(os.listdir(os.path.join("data",
                                                   "sprites",
                                                   "Players")))
        spaceship_path = os.path.join("data",
                                      "sprites",
                                      "Players",
                                      spaceship)

        explotion1_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion1.png")

        explotion2_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion2.png")
        # Sprites de una nave. [principal, explosion 1 , explosion 2]
        self.images = list() 
        self.images.append(cargar_sprite(spaceship_path))
        self.images.append(cargar_sprite(explotion1_path))
        self.images.append(cargar_sprite(explotion2_path))

        # Sprite visible de los 3.
        self.visible = 0

        # Informacion de pygame.Sprite
        self.image = self.images[self.visible]
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0

    def aparecer(self, (coor_x, coor_y)):
        """ Coloca un jugador en las coordenadas de cuadrilla x, y.
            Parametros:
                - (coor_x,coor_y): coordenadas del tablero."""
        sleep(0.05)

        # Se selecciona el sprite de nave.
        self.visible = 0
        self.image = self.images[self.visible]

        # Se determina su posicion y orientacion inicial.
        self.battlefieldpos_x = coor_x
        self.battlefieldpos_y = coor_y
        self.orientacion = 0

        # Se transforman las coordenas del tablero a las de pygame.
        new_x, new_y = transformar_coordenadas(coor_x, coor_y)
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def mostrar_tablero(self, screen):
        """ Muestra en pantalla el sprite del jugador.
            Paramteros:
                -screen: Ventana donde se muestra el juego."""

        screen.blit(self.image, self.rect)

    def mostrar_marcador(self, screen, coor_x, coor_y):
        """ Muestra informacion del jugador en una tabla. 
            Parametros:
                -screen: superficie donde se dibuja.
                -coor_x: coordenadas x de pygame.
                -coor_y: coordenadas y de pygame.
                """
        # Miniatura de la nave.
        sprite = pygame.transform.scale(self.image, (15, 15))
        nombre = fuenteM.render(self.ID, 0, (255, 255, 255))
        vidas = fuenteVidas.render("x"+str(self.vidas), 0, (240, 240, 240))

        screen.blit(sprite, (coor_x, coor_y))
        screen.blit(vidas, (coor_x+16, coor_y))
        screen.blit(nombre, (coor_x+50, coor_y))

    def mover(self, direccion):
        """ Cambia la posicion de un jugador hacia la direccion dada.
            Parametros:
                direccion: string, indica si la nave sube, baja,izq o dere."""

        # Mueve el sprite hasta llegar a la nueva coordenada de tablero.
        X, Y = MOV[direccion]
        if SETH[direccion] != self.orientacion:
            rotar = SETH[direccion]-self.orientacion
            self.orientacion = SETH[direccion]
            self.image = pygame.transform.rotate(self.image, rotar)
        else:
            self.battlefieldpos_x = round(self.battlefieldpos_x + X*0.1, 2)
            self.battlefieldpos_y = round(self.battlefieldpos_y + Y*0.1, 2)

            if self.battlefieldpos_y < -1:
                self.battlefieldpos_y = BATTLEFIELDDIVISIONS
            if self.battlefieldpos_y > BATTLEFIELDDIVISIONS+1:
                self.battlefieldpos_y = 0

            if self.battlefieldpos_x < -1:
                self.battlefieldpos_x = BATTLEFIELDDIVISIONS
            if self.battlefieldpos_x > BATTLEFIELDDIVISIONS+1:
                self.battlefieldpos_x = 0

            new_x, new_y = transformar_coordenadas(self.battlefieldpos_x,
                                                   self.battlefieldpos_y)
            self.rect.centerx = new_x
            self.rect.centery = new_y

    def disparar(self, direccion):
        """ La nave dispara a la direccion dada.
            Parametros:
                - direccion: (tupla), direccion a la que se disparo."""
        # TODO

        pass
    def ganar_vida(self):
        """ Le suma una vida al jugador."""
        self.vida += 1

    def quitar_vida(self):
        """ Le resta una vida al jugador."""
        self.vidas -= 1

    def morir(self):
        """ La nave explota, y luego desparece."""
        if self.visible == 0:
            self.visible += 1
            flag = False

            # SFX
            explosion = "explosion{0}.wav".format(choice("1234"))
            sfx_path = os.path.join("data", "sfx", explosion)
            pygame.mixer.Sound(sfx_path).play()

        elif self.visible == 1:
            self.visible += 1
            flag = False

        elif self.visible == 2:
            flag = True

        self.image = self.images[self.visible]
        return flag

    def cambiar_alerta(self, cambio):
        # TODO
        pass

# TODO


class Bala(pygame.sprite.Sprite):

    """ Objeto que representara a los disparos. """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Datos dibujo
        self.imagenes = list()
        for laser in os.listdir(os.path.join("data",
                                             "sprites",
                                             "Laser")):
            path = os.path.join("data",
                                "sprites",
                                "Laser",
                                laser)

            self.imagenes.append(load_image(path, True))

        self.rect = self.imagenes[0].get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0


# ------------------------
# DEFINICION DE FUNCIONES
# ------------------------

def cargar_sprite(path, escala=ESCALA):
    """ Carga imagenes para sprites.
        Parametros:
            escala: (float) escala de conversion."""
    image = load_image(path, True)

    width, height = image.get_size()

    return pygame.transform.scale(image,
                                  (int((width*escala)),
                                   int(height*escala)))


def dibujar_cuadricula(screen):
    """ Dibuja el tablero."""
    cuadrado = BATTLEFIELDSIZE / BATTLEFIELDDIVISIONS
    coor_x = BATTLEFIELDINICIO[0]
    coor_y = BATTLEFIELDINICIO[1]
    while coor_x < BATTLEFIELDINICIO[0]+BATTLEFIELDSIZE+cuadrado:
        pygame.draw.line(screen, (125, 125, 125),
                         (coor_x, BATTLEFIELDINICIO[1]),
                         (coor_x, BATTLEFIELDINICIO[1]+BATTLEFIELDSIZE),
                         1)
        pygame.draw.line(screen, (125, 125, 125),
                         (BATTLEFIELDINICIO[0], coor_y),
                         (BATTLEFIELDINICIO[0]+BATTLEFIELDSIZE, coor_y),
                         1)
        coor_x += cuadrado
        coor_y += cuadrado


def transformar_coordenadas(coor_x, coor_y):
    """ Transforma coordenadas de tablero a coordenadas de pygame.
        Paramatros:
            -coor_x: (int) coordenada x de tablero.
            -coor_y: (int) coordenada y de tablero.
    """
    cuadrado = BATTLEFIELDSIZE / BATTLEFIELDDIVISIONS
    new_x = BATTLEFIELDINICIO[0]+(coor_x*cuadrado)+(cuadrado/2)
    new_y = BATTLEFIELDINICIO[1]+(coor_y*cuadrado)+(cuadrado/2)
    return new_x, new_y


def cargar_jugadores(log):
    jugadores = dict()
    while True:
        linea = log.pop(0)
        accion, argumentos = linea.strip().split(":")
        if accion == "conectado":
            jugadores[argumentos] = Jugador(argumentos)
        elif argumentos == "comenzar":
            return jugadores

# TODO


def discriminar_accion(scene, accion, argumentos):
    """ Por cada comando del logfile, determina que accion tomar.
        Parametros:
            accion:     (string) accion leida del logfile-replay.
            argumentos: (string) argumentos correspondientes a la accion.
    """

    if accion == "aparecer":
        sleep(0.05)
        ID, x, y = argumentos.split(",")
        jugador = scene.players[ID]
        jugador.aparecer((int(x), int(y)))
        scene.next_turn = True
        scene.acciones[0] = "Aparecio: {0} en: ({1},{2})".format(ID, x, y)

    # falta si termina la partida
    elif accion == "juego" and argumentos == "terminar":
        sleep(3)
        scene.end_replay = True

    elif accion == "moverse":
        ID, new_x, new_y = argumentos.split(",")
        scene.acciones[0] = "Movimiento: {0} hacia: ({1},{2})".format(
            ID, new_x, new_y)
        new_x = int(new_x)
        new_y = int(new_y)

        jugador = scene.players[ID]
        coor_x = jugador.battlefieldpos_x
        coor_y = jugador.battlefieldpos_y
        resultado = (round(new_x - coor_x, 2), round(new_y - coor_y, 2))

        if 0.01 < resultado[0] <= 1 or resultado[0] < -1:
            jugador.mover("rigth")
        elif -0.01 > resultado[0] >= -1 or resultado[0] > 1:
            jugador.mover("left")
        elif 0.01 < resultado[1] <= 1 or resultado[1] < -1:
            jugador.mover("down")
        elif -0.01 > resultado[1] >= -1 or resultado[1] > 1:
            jugador.mover("up")
        else:
            scene.next_turn = True

    # TODO
    elif accion == "disparar":
        origen, coor_x, coor_y, objetivo = argumentos.split(",")
        jugador_origen = scene.players[origen]
        if objetivo == "None":
            scene.acciones[0] = "Disaparo fallido: {0} a ({1},{2})".format(
                origen, coor_x, coor_y)
        else:
            jugador_origen.ganar_vida()
            scene.acciones[0] = "Disaparo acertado: {0} a {1}".format(
                origen, objetivo)
            
        pass

    elif accion == "muerte":
        sleep(0.7)
        scene.acciones[0] = "Muere: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            jugador.quitar_vida()
            scene.turnos_restantes = Q_turnos

    elif accion == "colision":
        sleep(0.7)
        scene.acciones[0] = "Colisiona: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            jugador.quitar_vida()
            scene.turnos_restantes = Q_turnos

    elif accion == "desconectado":
        sleep(0.5)
        scene.acciones[0] = "Se ha desconectado: {0}".format(argumentos)
        del scene.players[argumentos]
        scene.next_turn = True

    # TODO
    elif accion == "resultado":
        pass

    elif accion == "alertar":
        ID, nivel = argumentos.split(",")
        scene.players[ID].alerta = int(nivel)

    else:
        print accion, argumentos
        pass

# -----
# MAIN
# -----

if __name__ == "__main__":
    # path = raw_input("Ingrese log: ")
    path = "test.log"
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main, path))
    Main.loop()
