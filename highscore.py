import sqlite3
import pygame
from pygame.locals import *

class Highscore:
    def __init__(self, surface, connection):
        self.surface = surface
        self.db = connection
        self.cur = self.db.cursor()

    def update(self, name, score, font):
        player = []
        i = 1
        try:
            self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
#                    cursor.execute("SELECT id FROM highscore WHERE name = ?", (name,))
#                    data=cursor.fetchone()
#                    if data is None:
#                        print('There is no component named %s'%name)
#                        cursor.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
#                    else:
#                        print('Component %s found with rowid %s'%(name,data[0]))
        except sqlite3.Error, e:
            print "Ooops:", e.args[0]
            
        try: 
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 0,10')
        except sqlite3.Error, e:
            print "Ooops:", e.args[0]

        for row in self.cur:				#Loopa genom
            player.append(font.render(str(i) + '. ' + str(row[1]) + ' - ' + str(row[2]), True, (255, 0, 0)))
            i += 1
        return player

    def draw(self, player, font):
        i = 30
        
        gameOverImg = font.render("Game Over", True, (255, 0, 0))
        highScoreImg = font.render("Name      Score", True, (255, 0, 0))
        for row in player:
            self.surface.blit(row, (self.surface.get_width()/2-100, 150+i))
            i += 30
                                
        self.surface.blit(gameOverImg, (self.surface.get_width()/2-100, 100))
        self.surface.blit(highScoreImg, (self.surface.get_width()/2-100, 150))
