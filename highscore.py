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
        self.cur.execute("SELECT COUNT(*) FROM highscore" )
        result = self.cur.fetchall()
        nrecs = result[0][0]
        if nrecs > 10:
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 9,1')
            last = self.cur.fetchone()
            #print last
            if last[2] < score:
                try:
                    self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
                except sqlite3.Error, e:
                    print "Ooops:", e.args[0]
        else:
            try:
                self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
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
        i = 20
        font2 = pygame.font.SysFont('Arial Black', 40)
       #pygame.draw.rect(self.surface, (255,255,255), (self.surface.get_width()/2-129, 79,302, 462), 0)
        trans = pygame.Surface((300, 350))
        trans.fill((0,0,0))
        pygame.Surface.convert_alpha(trans)
        trans.set_alpha(128)

        self.surface.blit(trans, (self.surface.get_width()/2-130,80))                                
        
        gameOverImg = font2.render("Game Over", True, (255, 0, 0))
        highScoreImg = font.render("Name      Score", True, (255, 0, 0))
        pressSpaceImg = font.render("Press space to try again", True, (255, 0, 0))
        
        for row in player:
            self.surface.blit(row, (self.surface.get_width()/2-100, 140+i))
            i += 20
            

        self.surface.blit(gameOverImg, (self.surface.get_width()/2-120, 70))
        self.surface.blit(highScoreImg, (self.surface.get_width()/2-100, 140))
        self.surface.blit(pressSpaceImg, (self.surface.get_width()-250, self.surface.get_height()-30))
