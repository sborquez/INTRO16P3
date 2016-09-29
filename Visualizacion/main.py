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
            self.replay.pop(0)
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

        if event == pygame.K_SPACE:
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
            acciones:        (list(str) Pila de informacion ya leida.
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
            self.director.change_scene(Estadisticas(self.director))

        # Si se termino de actualizar los datos de un turno, leer el siguiente.
        if self.next_turn:
            sleep(0.05)
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
                - event: Indica si se ha apretado 'espacio'.
        """

        # TEST
        if event == pygame.K_SPACE:
            pygame.mixer.music.stop()
            self.end_replay = True

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla.
            Parametros:
                - screen: Ventana donde se dibuja.
        """

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
            if not jugador.sigue_vivo():
                continue
            jugador.mostrar_tablero(screen)
            jugador.mostrar_marcador(screen, coor_x, coor_y)
            coor_y += 18
            if coor_y + 30 >= HEIGHT:
                coor_y = 150
                coor_x = 180
        for ide, jugador in self.players.items():
            if jugador.ha_disparado():
                jugador.mostrar_disparo(screen)


class Estadisticas(Scene):

    """ Ventana final del juego, muestra los resultados, tablas, etc.
        Campos:
            director:        (MainFrame) Manipulador del juego.
            background:      (image) Imagen de fondo.
            resultados:      (dict(id:list()) Resultados de un jugador(id)
                                    id: veces_muerto
                                        colisiones,
                                        disparos_efectivos,
                                        disparos_fallidos,
                                        % de acierto,
                                        % de muerte por colision
            top:             (list) Lista ordenada (disparos_efectivos,vidas,jugador)
    """

    def __init__(self, director):
        """ Parametros:
                - director: Objeto MainFrame, manipulador del juego.
        """

        Scene.__init__(self, director)
        # Informacion de escena.
        # backgound: Imagen de fondo.
        background_path = os.path.join("data", "background", "resultados.jpg")
        self.background = load_image(background_path)

        # Musica.
        musica_path = os.path.join(
            "data", "music", "Victory and Respite(end).mp3")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(0, 0.0)

        # Resultados de la partida.
        self.resultados = dict()
        self.top = list()

        with open(director.path_log) as log:
            self.replay = log.readlines()
            self.replay.pop(0)

        while len(self.replay) > 0:
            try:
                linea = self.replay.pop(0)
                accion, argumentos = linea.strip().split(":")
                # Agregamos los jugadores a resultados
                if accion == "conectado":
                    self.resultados[argumentos] = [0, 0, 0, 0, 0, 0]
                elif accion == "disparar":
                    jugador, _, _, objetivo = argumentos.split(",")
                    if objetivo == "None":
                        # Disparos fallidos.
                        self.resultados[jugador][3] += 1
                    else:
                        # Disparos efectivos.
                        self.resultados[jugador][2] += 1
                elif accion == "colision":
                    jugador = argumentos
                    # Colisiones
                    self.resultados[jugador][1] += 1
                    # Muertes
                    self.resultados[jugador][0] += 1
                elif accion == "muerte":
                    self.resultados[argumentos][0] += 1
            except KeyError:
                print "Archivo log posee incongruencias."

        for jugador, resultados in self.resultados.items():
            porcentaje_aciertos = calcular_porcentaje(
                                            resultados[3] + resultados[2],
                                            resultados[2])
            porcentaje_muerte_colision = calcular_porcentaje(
                                            resultados[0],
                                            resultados[1])
            self.resultados[jugador][4] = porcentaje_aciertos
            self.resultados[jugador][5] = porcentaje_muerte_colision
            self.top.append((resultados[2]-resultados[0],
                             resultados[2],
                            jugador))
            self.top.sort()
            self.top.reverse()

        self.primero_mostrando = 1
        self.total_jugadores = len(self.top)

    def on_update(self):
        """ Actualizar datos, cambia de escena si es necesario. """
        pass

    def on_event(self, event):
        """ Revisa si ocurrio un evento en el bucle principal. """
        if event == pygame.K_DOWN:
            if self.total_jugadores - self.primero_mostrando + 1 > 12:
                self.primero_mostrando += 1
        elif event == pygame.K_UP:
            if self.primero_mostrando != 1:
                self.primero_mostrando -= 1

    def on_draw(self, screen):
        """ Refrescar datos en la pantalla."""
        # Mostramos las estadisticas en la escena estadisticas

        screen.blit(self.background, (0, 0))
        formato_h = "{0}  {1}                    {2}  {3}  {4}  {5}  {6}  {7}"
        formato_id = "{0}  {1}"

        title = fuenteL.render("Estadisticas", 0, (255, 255, 255))
        screen.blit(title, (320, 40))
        cabezera = fuenteM.render(formato_h.format("n", "ID", 
                                                 "Aciertos", "Fallidos",
                                                 "Muertes", "Colisiones", 
                                                 "Eficiencia", "Accidentes"),
                                                  0, (255, 255, 255))
        screen.blit(cabezera, (40,80))
        inicial = self.primero_mostrando
        Y = 120
        while Y < 480:
            try:
                jugador = self.top[inicial-1][2]
            except IndexError:
                Y += 480
                continue
            jugador_id = fuenteM.render(formato_id.format(inicial, jugador),
                                        0, (255, 255, 255))
            aciertos = fuenteM.render(str(self.resultados[jugador][2]),
                                      0, (255, 255, 255))
            fallidos = fuenteM.render(str(self.resultados[jugador][3]),
                                      0, (255, 255, 255))
            muertes = fuenteM.render(str(self.resultados[jugador][0]),
                                     0, (255, 255, 255))
            colisiones = fuenteM.render(str(self.resultados[jugador][1]),
                                        0, (255, 255, 255))
            eficiencia = fuenteM.render(str(self.resultados[jugador][4])+"%",
                                        0, (255, 255, 255))
            accidentes = fuenteM.render(str(self.resultados[jugador][5])+"%",
                                        0, (255, 255, 255))

            screen.blit(jugador_id, (40,Y))
            screen.blit(aciertos, (200,Y))
            screen.blit(fallidos, (300,Y))
            screen.blit(muertes, (400,Y))
            screen.blit(colisiones, (500,Y))
            screen.blit(eficiencia, (610,Y))
            screen.blit(accidentes, (730,Y))

            inicial += 1
            Y += 30

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
            visible:            (int) indice, sprite de jugador.
            laser:              (Bala)objero bala de la nave.
    """

    def __init__(self, ID):
        """Parametros:
            - ID: string, identificador del jugador."""

        pygame.sprite.Sprite.__init__(self)
        # Datos jugador.
        self.ID = ID
        self.alerta = 0
        self.vidas = 3
        self.battlefieldpos_x = -1
        self.battlefieldpos_y = -1
        self.orientacion = 0

        # Porcetanje cargado de disparo. Animacion disparo
        self.__disparo = 0.0
        self.laser = Bala()

        # Datos dibujo.
        idspaceship = randint(0, SPACESHIPS-1)
        spaceship = choice(os.listdir(os.path.join("data",
                                                   "sprites",
                                                   "Players")))
        spaceship1_path = os.path.join("data",
                                       "sprites",
                                       "Players",
                                       spaceship)

        spaceship2_path = os.path.join("data",
                                       "sprites",
                                       "Shooting",
                                       spaceship)

        explotion1_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion1.png")

        explotion2_path = os.path.join("data",
                                       "sprites",
                                       "Explotions",
                                       "Explosion2.png")

        # Sprites de una nave. [principal, explosion 1 , explosion 2,shooting]
        self.images = list()
        self.images.append(cargar_sprite(spaceship1_path))
        self.images.append(cargar_sprite(explotion1_path))
        self.images.append(cargar_sprite(explotion2_path))
        self.images.append(cargar_sprite(spaceship2_path))

        # Sprite visible de los 4.
        self.visible = 0

        # Informacion de pygame.Sprite
        self.image = self.images[self.visible]
        self.rect = self.image.get_rect()
        self.rect.centerx = -100
        self.rect.centery = -100

    def ha_disparado(self):
        """ Revisa si se a disparado en este turno. """
        return self.laser.fue_disparado()

    def mostrar_disparo(self, screen):
        """ Muestra la Bala en pantalla. """
        self.laser.mostrar_tablero(screen)

    def sigue_vivo(self):
        """ Revisa si el jugador aun tiene vidas. """
        if self.vidas <= 0:
            return False
        return True

    def sound_fx(self, sfx_path_list, volumen):
        """ Reproduce un efecto de sonido.
            Parametros:
                -sfx_path:  (list(string)) elementos del path
                -volumen:   (float) volumen de reproduccion (0 a 1)
        """
        sfx_path = os.path.join(*sfx_path_list)
        sfx = pygame.mixer.Sound(sfx_path)
        sfx.set_volume(volumen)
        sfx.play()

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
                -screen: Ventana donde se muestra el juego.
        """

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
                direccion: string, indica si la nave sube, baja,izq o dere.
        """

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

    def disparar(self, coor_x, coor_y, objetivo):
        """ La nave dispara a la direccion dada.
            Parametros:
                - direccion: (tupla), direccion a la que se disparo.
        """

        if round(self.__disparo, 3) >= 1.00:
            if objetivo != "None":
                self.ganar_vida()
            else:
                self.sound_fx(["data", "sfx", "miss.ogg"], 1)
            self.__disparo = 0.0
            self.laser.cambio_disparado()
            return True

        elif round(self.__disparo, 4) > 0.50:
            self.laser.rotate()

        elif round(self.__disparo, 4) == 0.50:
            # SFX
            self.visible = 0
            laser = "laser{0}.wav".format(choice("123"))
            self.sound_fx(["data", "sfx", laser], 0.2)
            self.laser.disparo_a(int(coor_x), int(coor_y))
            self.laser.cambio_disparado()

        elif round(self.__disparo, 4) > 0.00:
            if int(self.__disparo*50) % 2:
                self.visible = 0
            else:
                self.visible = 3
        else:
            # SFX
            #self.sound_fx(["data", "sfx", "charging.wav"], 0.2)
            pass
        self.image = pygame.transform.rotate(
            self.images[self.visible], self.orientacion)
        self.__disparo = round(self.__disparo + 0.025, 4)
        return False

    def ganar_vida(self):
        """ Le suma una vida al jugador."""
        self.vidas += 1
        self.sound_fx(["data", "sfx", "lifeup.wav"], 0.3)

    def quitar_vida(self):
        """ Le resta una vida al jugador."""
        self.vidas -= 1
        self.sound_fx(["data", "sfx", "lifedown.ogg"], 1)

    def morir(self):
        """ La nave explota, y luego desparece."""
        if self.visible == 0:
            self.visible += 1
            flag = False

            # SFX
            explosion = "explosion{0}.wav".format(choice("1234"))
            self.sound_fx(["data", "sfx", explosion], 1)

        elif self.visible == 1:
            self.visible += 1
            flag = False

        elif self.visible == 2:
            flag = True

        self.image = self.images[self.visible]
        return flag


class Bala(pygame.sprite.Sprite):

    """ Representa a un disparo de una nave.
        Campos:
            imagen_master:      (image) Imagen original de la Bala.
            image:              (image) Imagen rotada de la Bala.
            battlefieldpos_x:   (int)   Posicion x en tablero.
            battlefieldpos_y:   (int)   Posicion y en tablero.
            orientacion:        (int)   grado de orientacion para rotar.
            disparado:          (int/bool) Indica si la bala se muetra.
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # Datos dibujo
        # Sprites
        path = os.path.join("data", "sprites", "Laser", "Laser.png")
        self.imagen_master = cargar_sprite(path, 1.5)
        self.image = cargar_sprite(path)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0

        # Posicion
        self.battlefieldpos_x = 0
        self.battlefieldpos_y = 0

        # Orientacion
        self.orientacion = 0

        # Estado
        self.disparado = 0

    def cambio_disparado(self):
        """ Cambia si se muestra la bala."""
        self.disparado += 1
        self.disparado %= 2

    def fue_disparado(self):
        """ Pregunta si la bala debe mostrarse."""
        return bool(self.disparado)

    def rotate(self):
        """ Gira la imagen de la bala."""
        self.orientacion += 120
        self.orientacion %= 360
        self.image = pygame.transform.rotate(
            self.imagen_master, self.orientacion)
        new_x, new_y = transformar_coordenadas(self.battlefieldpos_x,
                                               self.battlefieldpos_y)
        self.rect = self.image.get_rect()

        self.rect.centerx = new_x
        self.rect.centery = new_y

    def disparo_a(self, coor_x, coor_y):
        """ Determinar el lugar del tablero donde fue disparada.
            Parametros:
                coor_x:   (int)   Posicion x en tablero.
                coor__y:   (int)   Posicion y en tablero.
        """
        # Se determina su posicion y orientacion inicial.
        self.battlefieldpos_x = coor_x
        self.battlefieldpos_y = coor_y
        self.orientacion = 0

        # Se transforman las coordenas del tablero a las de pygame.
        new_x, new_y = transformar_coordenadas(coor_x, coor_y)
        self.rect = self.image.get_rect()
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def mostrar_tablero(self, screen):
        """ Dibuja el disparo en la pantalla.s """
        screen.blit(self.image, self.rect)

# ------------------------
# DEFINICION DE FUNCIONES
# ------------------------


def cargar_sprite(path, escala=1):
    """ Carga imagenes para sprites.
        Parametros:
            escala: (float) escala de conversion.
    """
    escala = 4.0/BATTLEFIELDDIVISIONS * escala
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


def cargar_jugadores(replay):
    """ Carga los jugadores desde log/replay a un diccionario.
        Parametros:
            -replay:    (list(string)) Lineas del log.
    """
    jugadores = dict()
    while True:
        linea = replay.pop(0)
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
        sleep(0.03)
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

    elif accion == "disparar":
        origen, coor_x, coor_y, objetivo = argumentos.split(",")
        jugador_origen = scene.players[origen]
        scene.next_turn = jugador_origen.disparar(coor_x, coor_y, objetivo)
        if objetivo == "None":
            scene.acciones[0] = "Disaparo fallido: {0} a ({1},{2})".format(
                origen, coor_x, coor_y)
        else:
            scene.acciones[0] = "Disaparo acertado: {0} a {1}".format(
                origen, objetivo)

    elif accion == "muerte":
        sleep(0.25)
        scene.acciones[0] = "Muere: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            jugador.quitar_vida()
            scene.turnos_restantes = Q_turnos

    elif accion == "colision":
        sleep(0.25)
        scene.acciones[0] = "Colisiona: {0}".format(argumentos)
        jugador = scene.players[argumentos]
        scene.next_turn = jugador.morir()
        if scene.next_turn:
            jugador.quitar_vida()
            scene.turnos_restantes = Q_turnos

    elif accion == "desconectar":
        sleep(0.25)
        scene.acciones[0] = "Se ha desconectar: {0}".format(argumentos)
        del scene.players[argumentos]
        scene.next_turn = True

    elif accion == "alertar":
        scene.next_turn = True

    else:
        scene.next_turn = True
        print accion, argumentos


def buscar_logs():
    """ Busca en el directorio logs, guarda los archivos en un diccionario."""
    logs = list()
    for log in os.listdir("logs"):
        name, ext = os.path.splitext(log)
        if ext == ".log":
            try:
                with open(os.path.join("logs", log), 'r') as replay:
                    line = replay.readline()
                    TITLE, DATA = line.strip().split(";")
                    FECHA, TAMANHO = DATA.split("/")
                    TAMANHO = int(TAMANHO)
                    logs.append((
                        os.path.join("logs", log), FECHA, TAMANHO))
            except ValueError:
                print "{0} NO tiene el formato correcto.".format(log)
    return logs


def elegir_partidas(logs):
    """ Muestra los archivos encontrados, pide elegir uno para reproducir.
        Parametros:
            -logs:  (dict(name:(path,fecha,hora,tamanho)
                        name:       (str)Nombre de la partida.
                        path:       (str)ruta de la partida.
                        fecha:      (str)fecha de la partida.
                        hora:       (str)hora de la partida.
                        tamanho:    (int)tamanho del tablero."""
    print "Archivos encontrados:"
    for log, (path, FECHA, TAMANHO) in enumerate(logs):
        print "\t> {0}:\t".format(log),
        print "Path:{0}\tFecha:{1}\tTamanho:{2}".format(path,FECHA, TAMANHO)

    while True:
        try:
            log = int(raw_input("Seleccione log: "))
            path, _, tamanho = logs[log]
            return path, tamanho
        except IndexError:
            print "Entrada incorrecta."
        except  ValueError:
            print "Ingrese un numero."

def calcular_porcentaje(total, porcion):
    try:
        return round((porcion/float(total))*100,1)
    except ZeroDivisionError:
        return 0.0
# -----
# MAIN
# -----

if __name__ == "__main__":
    logs = buscar_logs()
    path, BATTLEFIELDDIVISIONS = elegir_partidas(logs)

    Main = MainFrame(TITULO, path)

    Main.change_scene(Inicio(Main, path))
    Main.loop()
