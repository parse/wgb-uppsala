from paddle import *
from ball import *
from collisionhandler import *
from wall import *

import inputbox

import random
import pygame
import sqlite3

def main():
    pygame.init()
    try:
        w = 640
        h = 480

        screen = pygame.display.set_mode((w, h))
        font = pygame.font.SysFont('Arial Black', 20)
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        ch = CollisionHandler()

        TIMEEVENT = USEREVENT + 1
        pygame.time.set_timer(TIMEEVENT, 15)

        # Load our balls
        balls = [
            Ball(screen, (70, 15), (random.randint(1,3),random.randint(1,3)) ), 
            Ball(screen, (200, 60), (random.randint(1,3),random.randint(1,3)) ), 
            Ball(screen, (random.randint(50, 200), 75), (3,2) ), 
            Ball(screen, (50, 45), (3,2) ), 
            Ball(screen, (100, 200), (1,3) )
        ]
        
        for ball in balls:
            ch.addBall(ball)

        # Insert walls
        walls = [
            Wall( screen, (0,30), (10, screen.get_height()) ),
            Wall( screen, (screen.get_width()-10,30), (10, screen.get_height()) ), 
            Wall( screen, (0,30), (screen.get_width(), 10) ) 
        ]
        
        for wall in walls:
            ch.addObject(wall)
        
        paddle = Paddle(screen)
        ch.addObject(paddle)
        
        # Game variables
        run = True
        gameover = False
        viewHighScore = False;
        lifes = len(balls)-1
        time = 0
        name = "Johan"
        score = 0

        # Sqllite init
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()        
        try:
            cursor.execute('CREATE TABLE highscore (id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
        except sqlite3.Error, e:
            print "Create table:", e.args[0]
                
        # Load scoreboard
        scoreBoard = font.render("Life: " + str(lifes) + " Score: ", True, (255, 0, 0))
        
        while not gameover:
            # Check for quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    cursor.close()
                    connection.commit()
                    connection.close()
                if event.type == TIMEEVENT:
                    time += 1
            
            # Update positions for balls
            for ball in balls: 
                if ball.update():
                    lifes -= 1
            
            # Update positions for paddle
            paddle.update()

            # Update collision handler
            if ch.update():
                score += 1
                
            # Draw background
            screen.fill((0, 0, 0))
            
            # Draw walls
            for wall in walls:
                wall.draw()
                
            # Draw paddle
            paddle.draw()    
            
            # Draw balls
            for ball in balls:
                ball.draw()

            #Draw scoreboard
            if run:
                scoreBoard = font.render("Life: " + str(lifes) + " Score: " + str(score), True, (255, 0, 0))

            pygame.draw.rect(screen, (0, 255, 255), (0, 0, time, 30))
            screen.blit(scoreBoard, (0, 5)) 

            if time >= screen.get_width():
                time = 0;
                balls.append(ch.addBall(Ball(screen, (random.randint(50, 100), random.randint(100, 200)), (random.randint(1,3),random.randint(1,3)) )))
                
            if lifes <= 0 and run:
                pygame.time.set_timer(TIMEEVENT, 0)
                finalScore = score
                viewHighScore = True
                run = False
                name = inputbox.ask(screen, "Your name ")
                try:
                    cursor.execute("SELECT id FROM highscore WHERE name = ?", (name,))
                    data=cursor.fetchone()
                    if data is None:
                        print('There is no component named %s'%name)
                        cursor.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
                    else:
                        print('Component %s found with rowid %s'%(name,data[0]))
                except sqlite3.Error, e:
                    print "Ooops:", e.args[0]
                    
                cursor.execute("UPDATE highscore SET score='"+str(finalScore)+"' WHERE name='"+name+"'")
                cursor.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 0,10')
                i = 1
                player = []
                
                for row in cursor:				#Loopa genom
                    player.append(font.render(str(i) + '. ' + str(row[1]) + ' - ' + str(row[2]), True, (255, 0, 0)))
                    i += 1
                print answer
                scoreBoard = font.render("Life: 0 Score: " + str(finalScore), True, (255, 0, 0))                
                
            if viewHighScore:                
                i = 30
                gameOverImg = font.render("Game Over", True, (255, 0, 0))
                highScoreImg = font.render("   Name      Score", True, (255, 0, 0))
                for row in player:
                    screen.blit(row, (screen.get_width()/2-100, screen.get_height()/2+50+i))
                    i += 30
                                
                screen.blit(gameOverImg, (screen.get_width()/2, screen.get_height()/2))
                screen.blit(highScoreImg, (screen.get_width()/2-100, screen.get_height()/2+50))
                
            # Update screen
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
