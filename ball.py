from paddle import *

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

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius < 0:
            self.vx *= -1
        elif self.x + self.radius > self.surface.get_width():
            self.vx *= -1
        if self.y - self.radius < 0:
            self.vy *= -1
        elif self.y + self.radius > self.surface.get_height():
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)