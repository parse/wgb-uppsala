import pygame
from pygame.locals import *

class Paddle:
    def __init__(self, surface):
        self.surface = surface
        self.x = 0
        self.y = surface.get_height() - 30
        self.w = 100
        self.h = 10
        self.color = 128, 0, 128
 
    def update(self):
        self.x = pygame.mouse.get_pos()[0] - self.w / 2

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))