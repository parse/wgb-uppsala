#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Multimediaprogrammering i Python ST2010
# written by Jonatan Jansson, Anders Hassis & Johan Nänzen
# using Python 2.6.4
#

import pygame
from pygame.locals import *

class Wall:
    def __init__(self, surface, (x,y), (w,h) ):
        self.surface = surface
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = 200, 0, 128

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))