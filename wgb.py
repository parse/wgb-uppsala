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
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()
        ch = CollisionHandler()

        # Load our balls
        balls = [
            Ball(screen, (3,2) ), 
            Ball(screen, (1,3) )
        ]
        
        for ball in balls:
            ch.addBall(ball)

        # Insert walls
        walls = [
            Wall( screen, (0,0), (10, screen.get_height()) ),
            Wall( screen, (screen.get_width()-10,0), (10, screen.get_height()) ), 
            Wall( screen, (0,0), (screen.get_width(), 10) ) 
        ]
        
        for wall in walls:
            ch.addObject(wall)
        
        paddle = Paddle(screen)
        ch.addObject(paddle)
        
        # Game variables
        gameover = False
        lifes = 30
        
        while not gameover:
            # Check for quits
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
            
            # Update positions for balls
            for ball in balls: 
                if ball.update():
                    lifes -= 1
            
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
             
            # Update screen
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()