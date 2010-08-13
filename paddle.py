#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Multimediaprogrammering i Python ST2010
# written by Jonatan Jansson, Anders Hassis & Johan Nänzen
# using Python 2.6.4
#

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
        
        if self.x + self.w >= self.surface.get_width()-10:
            self.x = self.surface.get_width() - self.w - 10
        if self.x < 10:
            self.x = 10
            
    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))