# main.py
import pygame
from camera import *
from obj import *


class Engine:
    def __init__(self):
        pygame.init()
        self.RES = self.width, self.height = 1600, 900
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.cam = Camera(self,[0,0,0])
        self.obj = Object(self, 'Glass desk.obj')
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

    def play(self):
        self.obj.vertices = self.obj.vertices @ self.obj.translation([0,0,400])
        while 1:
        # for i in range(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0,0,0))
            self.cam.move()
            self.obj.draw()
            pygame.mouse.set_pos(400, 300)
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    eng = Engine()
    eng.play()
