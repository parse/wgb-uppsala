#
# Multimediaprogrammering i Python ST2010
# written by Jonatan Jansson, Anders Hassis & Johan Nänzen
# using Python 2.6.4
#

import sqlite3
import pygame
from pygame.locals import *

# Klass highscore.
# Skriver ut och uppdaterar highscores

class Highscore:
    # Initiering av higscore
    def __init__(self, surface):

        # Skapar en sqlite-anslutning till test.db, denna skapas om den inte finns.
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()        

        # Skapar en tabell vid namn highscore där namn och poäng lagras.
        # Om tabellen redan finns får man ett exception, som hanteras och stänger den öppna pekaren mot anslutningen.
        try:
            cursor.execute('CREATE TABLE highscore (id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
            cursor.close()
        except sqlite3.Error, e:
            cursor.close()
            
        self.surface = surface      # ytan som highscore ska skrivas ut på
        self.db = connection        # anslutningen till databasen
        self.cur = self.db.cursor() # pekarenmot databasen

    # Uppdaterar highscore
    # tar emot ett namn, poäng och en font.
    # Detta lagras sedan i databasen.
    def update(self, name, score, font):
        player = []
        i = 1
    
        self.cur.execute("SELECT COUNT(*) FROM highscore" )     # Kollar antalet inlägg i databasen
        result = self.cur.fetchall()
        nrecs = result[0][0]
        
        if nrecs > 10:              # Om det är mer än 10 inlägg
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 9,1')       # Väljer det sista och kollar om det är mindre poäng än det som användaren fick.
            last = self.cur.fetchone()
            #print last
            if last[2] < score:
                try:                
                    self.cur.execute('UPDATE highscore SET name=?, score=? WHERE id=?', (name, score, last[0]))    # Har användaren högre poäng läggs det in på det ID som petas ut.
                except sqlite3.Error, e:
                    print "Ooops:", e.args[0]
        else:                       # Lägg annars till det i tabellen
            try:
                self.cur.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
            except sqlite3.Error, e:
                print "Ooops:", e.args[0]
            
        try: 
            self.cur.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 0,10')      # Välj 10 inlägg med start från första
        except sqlite3.Error, e:
            print "Ooops:", e.args[0]

        for row in self.cur:				#Loopa genom inläggen och spara i en array för att sedan kunna skriva ut highscoren
            player.append(font.render(str(i) + '. ' + str(row[1]) + '  '*(8-len(row[1])) + str(row[2]), True, (255, 0, 0)))
            i += 1
            
        return player                   # Returnera arrayen med det som ska skrivas ut

    # Skriver ut highscore.
    # tar in player som är en array med listan av highscore.
    def draw(self, player, font):
        i = 20
        font2 = pygame.font.SysFont('Arial Black', 40)
        trans = pygame.Surface((300, 350))              # Skapar en genomskinlig ruta som ligger bakom highscore
        trans.fill((0,0,0))
        pygame.Surface.convert_alpha(trans)
        trans.set_alpha(128)

        self.surface.blit(trans, (self.surface.get_width()/2-130,80))        # Skriv ut rektangeln                        
        
        gameOverImg = font2.render("Game Over", True, (255, 0, 0))                  # Skapar en Game Over text
        highScoreImg = font.render("Name      Score", True, (255, 0, 0))            # Skapar Name Score till highscore
        pressSpaceImg = font.render("Press space to try again", True, (255, 0, 0))  # Skapar Press space to try again som  ligger i nedre högra hörnet
        
        for row in player:              # Loppa igenom player och skriv ut varje rad på skärmen
            self.surface.blit(row, (self.surface.get_width()/2-100, 140+i))
            i += 20                 # 20 pixlar mellan varje rad

        self.surface.blit(gameOverImg, (self.surface.get_width()/2-120, 70))                            # Skriver ut game over
        self.surface.blit(highScoreImg, (self.surface.get_width()/2-100, 140))                          # Skriver ut highscore headern
        self.surface.blit(pressSpaceImg, (self.surface.get_width()-250, self.surface.get_height()-30))  # Skriver ut press space again...
