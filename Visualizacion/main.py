import pygame
from pygame.locals import *
from escenas import *

TITULO = "Intro 2016"


class Inicio(Scene):

    """ Ventana de inicio del juego"""

    def __init__(self, director):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/portada.jpg")

        # Estados de escena
        self.start_replay = False

        # Informacion del replay
        self.logfile = None
        self.players = dict()
        self.testsprite = load_image("data/sprites/Players/PS12.png",
                                     transparent=True)

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
        pass


class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, dict_players, logfile):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/back.png")

        # Estados de escena
        self.end_replay = False

        # Informacion del replay
        self.logfile = logfile
        self.players = dict_players

        # Musica
        pygame.mixer.music.load("data/music/Arabesque(Main theme).mp3")
        pygame.mixer.music.play(100, 0.0)

    def on_update(self):
        if self.end_replay:
            self.director.change_scene(Estadisticas(self.director,
                                                    self.players))
        pass

    def on_event(self, event):
        if event:
            print "doble ok"
            pygame.mixer.music.stop()
            # TEST
            self.end_replay = True
        pass

    def on_draw(self, screen):
        screen.blit(self.background, (0, 0))
        pass


class Estadisticas(Scene):

    """ Ventana final del juego, muestra los resultados, tablas, etc."""

    def __init__(self, director, dict_players):
        Scene.__init__(self, director)
        # Informacion de escena
        self.background = load_image("data/background/back.png")

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


class Jugador():

    """ Informacion de un jugador """

    def __init__(self, ID, coor_x, coor_y):
        self.ID = ID
        self.x = coor_x
        self.y = coor_y
        self.vidas = 5
        self.alerta = 0
        # self.sprite = ...
        # self.rect = ...

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


if __name__ == "__main__":
    Main = MainFrame(TITULO)
    Main.change_scene(Inicio(Main))
    Main.loop()
