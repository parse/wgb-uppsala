import pygame
from pygame.locals import *

class Wall:
    def __init__(self, surface, (x,y), (w,h) ):
        self.surface = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = 128, 0, 128

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))