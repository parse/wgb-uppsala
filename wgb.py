from paddle import *
from ball import *
from collisionhandler import *
from wall import *

import random
import pygame
from pygame.locals import *
from pysqlite2 import dbapi2 as sqlite

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
        pygame.time.set_timer(TIMEEVENT, 100)

        # Load our balls
        balls = [
            Ball(screen, (70, 15), (3,2) ), 
            Ball(screen, (200, 60), (3,2) ), 
            Ball(screen, (190, 75), (3,2) ), 
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
        gameover = False
        viewHighScore = False;
        lifes = 2
        time = 0
        name = "Kalle"
        score = 0

        # Sqllite init
        connection = sqlite.connect('test.db')
        cursor = connection.cursor()        
        try:
            cursor.execute('CREATE TABLE highscore (id INTEGER PRIMARY KEY, name VARCHAR(50), score INTEGER)')
        except sqlite.Error:
            pass
        try:
            cursor.execute("SELECT id FROM highscore WHERE name = ?", (name,))
            data=cursor.fetchone()
            if data is None:
                print('There is no component named %s'%name)
                cursor.execute('INSERT INTO highscore VALUES (null, ?, ?)', (name, score))
                connection.commit()
            else:
                print('Component %s found with rowid %s'%(name,data[0]))
        except sqlite.Error, e:
            print "Ooops:", e.args[0]
        
        # Load scoreboard
        scoreBoard = font.render("Life: " + str(lifes) + " Score: ", True, (255, 0, 0))
        
        while not gameover:
            # Check for quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    cursor.close()
                    connection.close()
                if event.type == TIMEEVENT:
                    time += 1
            
            # Update positions for balls
            for ball in balls: 
                if ball.update():
                    lifes -= 1
                    scoreBoard = font.render("Life: " + str(lifes) + " Score: ", True, (255, 0, 0))
            
            # Update positions for paddle
            paddle.update()

            # Update collision handler
            ch.update()
			
            if lifes <= 0:
                gameover = True
                
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
            pygame.draw.rect(screen, (0, 255, 255), (0, 0, time, 30))
            screen.blit(scoreBoard, (0, 5)) 

            if time >= screen.get_width() or lifes <= 1:
                pygame.time.set_timer(TIMEEVENT, 0)
                lifes = 30;
                viewHighScore = True;
                score = random.randint(1, 100);
                                
                sql = "UPDATE highscore SET score='"+str(score)+"' WHERE name='"+name+"'"
                cursor.execute(sql)
                cursor.execute('SELECT * FROM highscore WHERE name="'+name+'"')
                text = cursor.fetchone()

                gameOverImg = font.render("Game Over", True, (255, 0, 0))
                higheScoreImg = font.render("ID: " + str(text[0]) + " Name: " + text[1] + " - " + str(text[2]), True, (255, 0, 0))
                
            if viewHighScore:
                
                screen.blit(gameOverImg, (screen.get_width()/2, screen.get_height()/2))
                screen.blit(higheScoreImg, (screen.get_width()/2, screen.get_height()/2+50))
                
            # Update screen
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
