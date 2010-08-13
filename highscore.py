#!/usr/bin/python
# -*- coding: utf8 -*-
#
# Multimediaprogrammering i Python ST2010
# written by Jonatan Jansson, Anders Hassis & Johan Nänzen
# using Python 2.6.4
# 

import sqlite3
import pygame
from pygame.locals import *

# Class highscore.
# Prints and updates the highscore tabel

class Highscore:
    # Init higscore
    def __init__(self, surface):

        # Creates a sqlite connection to test.db, will be created if non-exist
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()        

        # Creates a table where name and score are stored
        try:
            cursor.execute('CREATE TABLE highscore (id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
            cursor.close()
        except sqlite3.Error, e:
            cursor.close()
            
        self.surface = surface      
        self.db = connection        
        self.cur = self.db.cursor() 

    # Updates highscore and store in database
    def update(self, name, score, font):
        player = []
        i = 1
    
        self.cur.execute("SELECT COUNT(*) FROM highscore" )     # Check number of rows in table
        result = self.cur.fetchall()
        nrecs = result[0][0]
        
        if nrecs > 10:              # If 10 or more rows
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 9,1')       # Compares the last row with the current score
            last = self.cur.fetchone()
            #print last
            if last[2] < score:
                try:                
                    self.cur.execute('UPDATE highscore SET name=?, score=? WHERE id=?', (name, score, last[0]))    # Update the last row with new score and name
                except sqlite3.Error, e:
                    print "Ooops:", e.args[0]
        else:                       # Add a new row in table
            try:
                self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
            except sqlite3.Error, e:
                print "Ooops:", e.args[0]
            
        try: 
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 0,10')      # Choose the first 10 rows
        except sqlite3.Error, e:
            print "Ooops:", e.args[0]

        for row in self.cur:				# Loop though the rows and adds to a array
            player.append(font.render(str(i) + '. ' + str(row[1]) + '  '*(8-len(row[1])) + str(row[2]), True, (255, 0, 0)))
            i += 1
            
        return player                   # Return the array

    # Genereate and prints highscore.
    def draw(self, player, font):
        i = 20
        font2 = pygame.font.SysFont('Arial Black', 40)
        trans = pygame.Surface((300, 350))              # Creates transparent rectangle
        trans.fill((0,0,0))
        pygame.Surface.convert_alpha(trans)
        trans.set_alpha(128)

        self.surface.blit(trans, (self.surface.get_width()/2-130,80))                        
        
        gameOverImg = font2.render("Game Over", True, (255, 0, 0))                 
        highScoreImg = font.render("Name      Score", True, (255, 0, 0))            
        pressSpaceImg = font.render("Press space to try again", True, (255, 0, 0))  
        
        for row in player:              # Loops through player and blits every row with 20px between
            self.surface.blit(row, (self.surface.get_width()/2-100, 140+i))
            i += 20

        self.surface.blit(gameOverImg, (self.surface.get_width()/2-120, 70))                            
        self.surface.blit(highScoreImg, (self.surface.get_width()/2-100, 140))                          
        self.surface.blit(pressSpaceImg, (self.surface.get_width()-250, self.surface.get_height()-30))
