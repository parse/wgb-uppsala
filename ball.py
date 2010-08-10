import random

import pygame
from pygame.locals import *

def randsign():
    if(random.randint(0, 1)):
        return 1
    else:
        return -1
        
class Ball:
    def __init__(self, surface, (x, y), (vx,vy) ):
        self.surface = surface
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = 255, 0, 0
        self.radius = 5
        self.active = True
        
    @staticmethod
    def createRandomBallsAsList(number, screen):
        balls = []
            
        for i in range (0,number):
            balls.append( Ball(screen, (random.randint(50, 550), random.randint(50, 200)), (randsign()*random.uniform(1.0,3.0),random.uniform(1.0,3.0)) ) )

        return balls
    
        
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
        
