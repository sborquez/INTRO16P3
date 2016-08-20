import os
import pygame
from random import randint, choice
from pygame.locals import *
from escenas import *
from time import sleep

TITULO = "Intro 2016"
SPACESHIPS = 45
BATTLEFIELDSIZE = 460.0
BATTLEFIELDDIVISIONS = 20
BATTLEFIELDINICIO = (351, 10)
ESCALA = 4.0/BATTLEFIELDDIVISIONS
MOV = {"up": (0,  -1),
        "down": (0, 1),
        "left": (-1,  0),
        "rigth": (1,  0)}

SETH = {"up"   : 0,
        "down" : 180,
        "left" : -90,
        "rigth": 90}


class Inicio(Scene):

    """ Ventana de inicio del juego"""

    def __init__(self, director, path_log):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "portada.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        self.start_replay = False

        # Informacion del replay
        with open(path_log) as log:
            self.replay = log.readlines()
        self.players = cargar_jugadores(self.replay)

        # Musica
        musica_path = os.path.join("data", "music", "xeon6(intro).ogg")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        if self.start_replay:
            pygame.mixer.music.stop()
            self.director.change_scene(Principal(self.director,
                                                 self.players,
                                                 self.replay))

    def on_event(self, event):
        if event:
            self.start_replay = True

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))


class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, dict_players, replay):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "tablero.jpg")
        self.background = load_image(background_path)

        # Estados de escena
        self.next_turn = True
        self.end_replay = False
        self.linea = ""

        # Informacion del replay
        self.replay = replay
        self.players = dict_players

        # Musica
        musica_path = os.path.join(
            "data", "music", "Arabesque(Main theme).mp3")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(100, 0.0)

    def on_update(self):

        # Si se termino de leer la partida, pasar a los resultados.
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))

        # Si se termino de actualizar los datos de un turno, leer el siguiente.
        if self.next_turn:
            self.next_turn = False
            linea = self.replay.pop(0)
            self.linea = linea.strip().split(":")
        accion, argumentos = self.linea
        discriminar_accion(self, accion, argumentos)

    def on_event(self, event):
        if event:
            pygame.mixer.music.stop()
            # TEST
            self.end_replay = True

    def on_draw(self, screen):
        # Fondo
        screen.blit(self.background, (0, 0))

        # Cuadrilla
        dibujar_cuadricula(screen)

        # Jugadores
        for ide, jugador in self.players.items():
            jugador.mostrar(screen)


class Estadisticas(Scene):
    # TODO

    """ Ventana final del juego, muestra los resultados, tablas, etc."""

    def __init__(self, director, dict_players):
        Scene.__init__(self, director)
        # Informacion de escena
        background_path = os.path.join("data", "background", "portada.jpg")
        self.background = load_image(background_path)

        # Informacion del replay
        self.players = dict_players

        # Musica
        musica_path = os.path.join(
            "data", "music", "Victory and Respite(end).mp3")
        pygame.mixer.music.load(musica_path)
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        # TODO
        pass

    def on_event(self, event):
        # TODO
        if event:
            pass

    def on_draw(self, screen):
        # TODO
        screen.blit(self.background, (0, 0))
        pass


class Jugador(pygame.sprite.Sprite):

    """ Informacion de un jugador """

    def __init__(self, ID):
        pygame.sprite.Sprite.__init__(self)
        # Datos jugador
        self.ID = ID
        self.alerta = 0
        self.vidas = 5
        self.battlefieldpos_x = 0
        self.battlefieldpos_y = 0
        self.orientacion = 0

        # Datos dibujo
        self.image = cargar_sprite()
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.speed = [0.5, -0.5]

    def aparecer(self, (coor_x, coor_y)):
        """ Coloca un jugador en las coordenadas de cuadrilla x, y."""

        self.battlefieldpos_x = coor_x
        self.battlefieldpos_y = coor_y

        new_x, new_y = transformar_coordenadas(coor_x, coor_y)
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def mostrar(self, screen):
        """ Muestra en pantalla el sprite del jugador."""

        screen.blit(self.image, self.rect)

    def mover(self, direccion):
        """ Cambia la posicion de un jugador hacia la direccion dada."""
        # TODO
        X, Y = MOV[direccion]
        if SETH[direccion] != self.orientacion:
            rotar = SETH[direccion]-self.orientacion
            self.orientacion = SETH[direccion]
            self.image=pygame.transform.rotate(self.image,-rotar)
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
        # TODO

        pass

    def quitarvida(self):
        # TODO

        pass

    def morir(self, (coor_x, coor_y)):
        # TODO
        pass

    def cambiar_alerta(self, cambio):
        # TODO
        pass


def cargar_sprite(escala=ESCALA):
    idspaceship = randint(0, SPACESHIPS-1)

    spaceship = choice(os.listdir(os.path.join("data", "sprites", "Players")))
    spaceship_path = os.path.join("data", "sprites", "Players", spaceship)
    image = load_image(spaceship_path, True)

    width, height = image.get_size()

    return pygame.transform.scale(image,
                                  (int((width*escala)),
                                   int(height*escala)))


def dibujar_cuadricula(screen):
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
            print "conectado:", argumentos
            jugadores[argumentos] = Jugador(argumentos)
        elif argumentos == "comenzar":
            return jugadores

# TODO


def discriminar_accion(scene, accion, argumentos):
    """ Por cada comando del logfile, determina que accion tomar."""

    if accion == "aparecer":
        ID, x, y = argumentos.split(",")
        jugador = scene.players[ID]
        jugador.aparecer((int(x), int(y)))
        scene.next_turn = True

    # falta si termina la partida
    elif accion == "juego" and argumentos == "terminar":
        sleep(3)
        scene.end_replay = True

    elif accion == "moverse":
        ID, new_x, new_y = argumentos.split(",")
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
        pass
    # TODO
    elif accion == "muerte":
        pass
    # TODO
    elif accion == "desconectado":
        pass
    # TODO
    elif accion == "resultado":
        pass
    # TODO
    elif accion == "alertar":
        pass
    # TODO
    else:
        print accion, argumentos
        pass

if __name__ == "__main__":
    #path = raw_input("Ingrese log: ")
    path = "test.log"
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main, path))
    Main.loop()
