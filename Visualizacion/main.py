import os
import pygame
from random import randint
from pygame.locals import *
from escenas import *

TITULO = "Intro 2016"
SPACESHIPSPath = "data/sprites/Players/PS{0}{1}.png"
SPACESHIPS = 45


class Inicio(Scene):

    """ Ventana de inicio del juego"""

    def __init__(self, director, path_log):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/portada.jpg")

        # Estados de escena
        self.start_replay = False

        # Informacion del replay
        with open(path_log) as log:
            self.replay = log.readlines()
        self.players = cargar_jugadores(self.replay)

        # Musica
        pygame.mixer.music.load("data/music/xeon6(intro).ogg")
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        if self.start_replay:
            pygame.mixer.music.stop()
            self.director.change_scene(Principal(self.director,
                                                 self.players,
                                                 self.replay))
        pass

    def on_event(self, event):
        if event:
            self.start_replay = True
        pass

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
  

class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, dict_players, replay):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/tablero.jpg")

        # Estados de escena
        self.next_turn = True
        self.end_replay = False

        # Informacion del replay
        self.replay = replay
        self.players = dict_players

        # Musica
        pygame.mixer.music.load("data/music/Arabesque(Main theme).mp3")
        pygame.mixer.music.play(100, 0.0)

    def on_update(self):
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))
        if self.next_turn:
            self.next_turn = False
            linea = self.replay.pop(0)
            accion, argumentos = linea.strip().split(":")
            discriminar_accion(self, accion, argumentos)

    def on_event(self, event):
        if event:
            pygame.mixer.music.stop()
            # TEST
            self.end_replay = True

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
        for ide, jugador in self.players.items(): 
            jugador.mostrar(screen)

class Estadisticas(Scene):

    """ Ventana final del juego, muestra los resultados, tablas, etc."""

    def __init__(self, director, dict_players):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/portada.jpg")

        # Informacion del replay
        self.players = dict_players

        # Musica
        pygame.mixer.music.load("data/music/Victory and Respite(end).mp3")
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        pass

    def on_event(self, event):
        if event:
            pass

    def on_draw(self, screen):
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

        # Datos dibujo
        self.image = cargar_sprite()
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = 0
        self.speed = [0.5, -0.5]

    def aparecer(self, (coor_x, coor_y)):
        new_x, new_y = transformar_coordenadas(coor_x, coor_y)
        self.rect.centerx = new_x
        self.rect.centery = new_y

    def mostrar(self, screen):
        screen.blit(self.image, self.rect)

    def mover(self, direccion):
        pass

    def disparar(self, direccion):
        pass

    def quitarvida(self):
        pass

    def morir(self, (coor_x, coor_y)):
        pass

    def cambiar_alerta(self, cambio):
        pass


def cargar_sprite(escala=0.2):
    idspaceship = randint(0, SPACESHIPS-1)
    if idspaceship/10 != 0:
        image = load_image(SPACESHIPSPath.format("", idspaceship), True)
    else:
        image = load_image(SPACESHIPSPath.format("0", idspaceship), True)
    width, height = image.get_size()

    return pygame.transform.scale(image,
                                  (int((width*escala)),
                                   int(height*escala)))


def transformar_coordenadas(coor_x, coor_y):
    new_x = coor_x*100
    new_y = coor_y*100
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

def discriminar_accion(scene, accion, argumentos):
    if accion == "aparecer":
        ID, x, y = argumentos.split(",")
        jugador = scene.players[ID]
        jugador.aparecer((int(x), int(y)))
        scene.next_turn = True
    else:
        pass

if __name__ == "__main__":
    #path = raw_input("Ingrese log: ")
    path = "test.log"
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main, path))
    Main.loop()
