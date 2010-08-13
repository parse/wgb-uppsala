#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Multimediaprogrammering i Python ST2010
# written by Jonatan Jansson, Anders Hassis & Johan Nänzen
# using Python 2.6.4
#

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
        if ball.x - ball.radius > obj.x + obj.w: # If the ball is to the right of the object...
            if ball.x - ball.radius + ball.vx <= obj.x + obj.w: # AND will collide next time...
                if ball.y + ball.vy >= obj.y and ball.y + ball.vy <= obj.y + obj.h: # And is correct in Y-axis
                    ball.vx *= -1
        if ball.x + ball.radius < obj.x: # If the ball is to the left of the object... 
            if ball.x + ball.radius + ball.vx >= obj.x: # AND will collide next time...
                if ball.y + ball.vy >= obj.y and ball.y + ball.vy <= obj.y + obj.h: # And is correct in Y-axis
                    ball.vx *= -1
        if ball.y - ball.radius > obj.y + obj.h: # If the ball is under of the object...
            if ball.y - ball.radius + ball.vy <= obj.y + obj.h: # AND will collide next time...
                if ball.x + ball.vx >= obj.x and ball.x + ball.vx <= obj.x + obj.w: # And is correct in X-axis
                    ball.vy *= -1                    
        if ball.y + ball.radius < obj.y: # If the ball is above the object...
            if ball.y + ball.radius + ball.vy >= obj.y: # AND will collide next time...
                if ball.x + ball.vx >= obj.x and ball.x + ball.vx <= obj.x + obj.w: # And is correct in X-axis
                    ball.vy *= -1
                    if isinstance(obj, Paddle): # Is it the paddle it will collide with?
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
