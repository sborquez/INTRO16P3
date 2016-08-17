import pygame
from pygame.local import *
from escenas import *

class Inicio(Scene):
    """ Ventana de inicio del juego"""

    def __init__(self, director):
        Scene.__init__(self, director)
        self.background = None
        self.sound = None

    def on_update(self):
        pass
    
    def on_event(self, event):
        pass
 
    def on_draw(self, screen): 
        pass

class Principal(Scene):

    """ Aqui se muestra toda la accion, se lee el log, se ven 
        los jugadores, sfx, movimientos, etc."""

    def __init__(self, director, logfile):
        Scene.__init__(self, director)
        self.logfile = logfile
        self.background = None
        self.sound = None

   def on_update(self):
        pass
    
    def on_event(self, event):
        pass
 
    def on_draw(self, screen): 
        pass


class Estadisticas(Scene):

    """ Ventana final del juego, muestra los resultados, tablas, etc."""

    def __init__(self, director):
        Scene.__init__(self, director)
        self.background = None
        self.sound = None

   def on_update(self):
        pass
    
    def on_event(self, event):
        pass
 
    def on_draw(self, screen): 
        pass

class Jugador(pygame.Sprite):

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
    Main = MainFrame()
    Main.change_scene(Inicio(Main))
    Main.loop()