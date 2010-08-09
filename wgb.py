from paddle import *
from ball import *

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

        balls = [Ball(screen,(1,1) ), Ball(screen, (1,2) ), Ball(screen, (-1,2) )]

        paddle = Paddle(screen)
        gameover = False

        while not gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True

            for ball in balls: 
                ball.update()
                
            paddle.update()

            screen.fill((0, 0, 0))
            
            for ball in balls:
                ball.draw()
                
            paddle.draw()
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()