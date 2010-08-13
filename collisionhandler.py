from ball import *
from paddle import *

import pygame
from pygame.locals import *

class CollisionHandler:
    _balls = []
    _objects = []
    
    def __init__(self):
        pass
    
    def addBall(self, ball):
        self._balls.append(ball)
        return ball
    
    def addObject(self, object):
        self._objects.append(object)
        return object
    
    def reset(self):
        self._balls = []
        self._objects = []
    
    def update(self):
        i = 1
        
        for ball in self._balls:
            for obj in self._objects:
                if self._ballOnObject(ball, obj):
                    return True
                
            for ball2 in self._balls[i:]:
                self._ballOnBall(ball, ball2)
                
            i += 1
    
    def _ballOnObject(self, ball, obj):
        if ball.x - ball.radius > obj.x + obj.w: # Om bollen ar till hoger om objectet...
            if ball.x - ball.radius + ball.vx <= obj.x + obj.w: # Och kommer att vara krocka nasta gang...
                if ball.y + ball.vy >= obj.y and ball.y + ball.vy <= obj.y + obj.h: # Och ligger ratt i y-led
                    ball.vx *= -1
        if ball.x + ball.radius < obj.x: # Om bollen ar till vanster om objectet...
            if ball.x + ball.radius + ball.vx >= obj.x: # Och kommer att vara krocka nasta gang...
                if ball.y + ball.vy >= obj.y and ball.y + ball.vy <= obj.y + obj.h: # Och ligger ratt i y-led
                    ball.vx *= -1
        if ball.y - ball.radius > obj.y + obj.h: # Om bollen ar under objectet...
            if ball.y - ball.radius + ball.vy <= obj.y + obj.h: # Och kommer att vara krocka nasta gang...
                if ball.x + ball.vx >= obj.x and ball.x + ball.vx <= obj.x + obj.w: # Och ligger ratt i x-led
                    ball.vy *= -1                    
        if ball.y + ball.radius < obj.y: # Om bollen ar till ovanfor objectet...
            if ball.y + ball.radius + ball.vy >= obj.y: # Och kommer att vara krocka nasta gang...
                if ball.x + ball.vx >= obj.x and ball.x + ball.vx <= obj.x + obj.w: # Och ligger ratt i x-led
                    ball.vy *= -1
                    if isinstance(obj, Paddle): # Kollar om det ar paddlen som bollen krockar med
                        return True
    
    def _ballOnBall(self, ball1, ball2):
        dy = ball1.y - ball2.y
        dx = ball1.x - ball2.x
        
        sumRad = ball1.radius + ball2.radius
        sqrRad = sumRad * sumRad
        
        distSqr = (dy * dy) + (dx * dx)
        
        if distSqr <= sqrRad:
            self._handleBallOnBallCollision(ball1, ball2)
            
    def _handleBallOnBallCollision(self, ball1, ball2):
        tempx = ball1.x
        tempy = ball1.y
        ball1.x = ball2.x
        ball1.y = ball2.y
        ball2.x = tempx
        ball2.y = tempy
