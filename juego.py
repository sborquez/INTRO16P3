import escenas
import pygame
from pygame.local import *

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

class Jugador(pygame.Sprite)

    def __init__(self, ID, coor_x, coor_y):
        self.ID = ID
        self.x = coor_x
        self.y = coor_y
        self.vidas = 5
        self.alerta = 0

    def mover(self):
        pass

    def disparar(self):
        pass

    def respawn(self):
        pass

if __name__ == "__main__":
    Main = Mainframe()
    Main.change_scene(Inicio(Main))
    Main.loop()