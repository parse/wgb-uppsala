import pygame
from pygame.locals import *

class Ball:
    def __init__(self, surface, (vx,vy) ):
        self.surface = surface
        self.x = surface.get_width() / 2.0
        self.y = surface.get_height() - 150.0
        self.vx = vx
        self.vy = vy
        self.color = 255, 0, 0
        self.radius = 5
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        if self.y > self.surface.get_height() and self.active == True:
            self.active = False
            return True
        else:
            return False

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)