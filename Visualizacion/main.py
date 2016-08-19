import pygame
from pygame.locals import *
from escenas import *
from random import randint

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
        self.players_loaded = False

        # Informacion del replay
        self.logfile = None
        self.players = dict()

        # Musica
        pygame.mixer.music.load("data/music/xeon6(intro).ogg")
        pygame.mixer.music.play(0, 0.0)

    def on_update(self):
        if self.start_replay:
            pygame.mixer.music.stop()
            self.director.change_scene(Principal(self.director,
                                                 self.players,
                                                 self.logfile))
        pass

    def on_event(self, event):
        if event:
            print "ok"
            self.start_replay = True
        pass

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
  

class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, dict_players, logfile):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/tablero.jpg")

        # Estados de escena
        self.end_replay = False

        # Informacion del replay
        self.logfile = logfile
        self.players = dict_players
        self.jugadores = []

        # TEST
        for i in xrange(30):
            self.jugadores.append(Jugador(i, randint(10,80), randint(10,30)))

        # Musica
        pygame.mixer.music.load("data/music/Arabesque(Main theme).mp3")
        pygame.mixer.music.play(100, 0.0)

    def on_update(self):
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))

    def on_event(self, event):
        if event:
            print "doble ok"
            pygame.mixer.music.stop()
            # TEST
            self.end_replay = True

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
        # TEST
        for jugador in self.jugadores:
            jugador.mostrar(screen)
        pass


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
            print "triple ok"
        pass

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
        pass


class Jugador(pygame.sprite.Sprite):

    """ Informacion de un jugador """

    def __init__(self, ID, coor_x, coor_y):
        pygame.sprite.Sprite.__init__(self)
        # Datos jugador
        self.ID = ID
        self.alerta = 0
        self.vidas = 5
        self.battlefieldpos_x = coor_x
        self.battlefieldpos_y = coor_y

        # Datos dibujo
        self.image = cargar_sprite()
        self.rect = self.image.get_rect()
        mapa_x, mapa_y = transformar_coordenadas(coor_x, coor_y)
        self.rect.centerx = mapa_x
        self.rect.centery = mapa_y
        self.speed = [0.5, -0.5]

    def mostrar(self, screen):
        screen.blit(self.image, self.rect)

    def mover(self, direccion):
        pass

    def disparar(self, direccion):
        pass

    def quitarvida(self):
        pass

    def morir(self, coor_x, coor_y):
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
    new_x = coor_x*10
    new_y = coor_y*10
    return new_x, new_y

if __name__ == "__main__":
    #path = raw_input("Ingrese log: ")
    path=0
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main, path))
    Main.loop()
