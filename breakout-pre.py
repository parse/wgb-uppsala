import pygame
from pygame.locals import *

class Ball:
    def __init__(self, surface):
        self.surface = surface
        self.x = surface.get_width() / 2.0
        self.y = surface.get_height() - 150.0
        self.vx = 1.0
        self.vy = 1.0
        self.color = 255, 0, 0
        self.radius = 5

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.radius < 0:
            self.vx *= -1
        elif self.x + self.radius > self.surface.get_width():
            self.vx *= -1
        if self.y - self.radius < 0:
            self.vy *= -1
        elif self.y + self.radius > self.surface.get_height():
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.radius)

class Paddle:
    def __init__(self, surface):
        self.surface = surface
        self.x = 0
        self.y = surface.get_height() - 30
        self.w = 100
        self.h = 10
        self.color = 128, 0, 128

    def update(self):
        self.x = pygame.mouse.get_pos()[0] - self.w / 2

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.w, self.h))
        

def main():
    pygame.init()
    try:
        w = 640
        h = 480

        screen = pygame.display.set_mode((w, h))
        pygame.mouse.set_visible(False)
        clock = pygame.time.Clock()

        ball = Ball(screen)
        paddle = Paddle(screen)
        gameover = False

        while not gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True

            ball.update()
            paddle.update()

            screen.fill((0, 0, 0))
            ball.draw()
            paddle.draw()
            pygame.display.flip()

            clock.tick(60)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
        
