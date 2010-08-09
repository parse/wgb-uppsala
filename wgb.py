from paddle import *
from ball import *
from collisionhandler import *
from wall import *

import pygame
from pygame.locals import *

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
        lifes = 30
        time = 0;

        #Load scoreboard
        scoreBoard = font.render("Life: " + str(lifes) + " Score: ", True, (255, 0, 0))
        
        while not gameover:
            # Check for quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
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

            if time >= screen.get_width() or lifes <= 0:
                pygame.time.set_timer(TIMEEVENT, 0)
                gameOverImg = font.render("Game Over", True, (255, 0, 0))
                screen.blit(gameOverImg, (screen.get_width()/2, screen.get_height()/2))
             
            # Update screen
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
