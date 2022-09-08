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
        self.cam = Camera(self,[0,0,-40])
        self.obj = Object(self, 'Glass desk.obj')

    def play(self):
        # self.obj.vertices = np.dot(self.obj.vertices, self.obj.scale(100))
        while 1:
        # for i in range(1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.screen.fill((0,0,0))
            self.cam.move()
            self.obj.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    eng = Engine()
    eng.play()
