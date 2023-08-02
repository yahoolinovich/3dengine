# main.py
# This project takes in .obj files and outputs their vertices with 3d projection.


import pygame
from camera import *
from obj import *
from numba import njit


class Engine:
    def __init__(self):
        pygame.init()
        self.RES = self.width, self.height = 1600, 900
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.frame = np.ones((self.width, self.height, 3)).astype('uint8')
        self.z_buffer = np.ones((self.width, self.height))
        self.cam = Camera(self,[10,5.5,-200])
        self.objects = [Object(self, 'Glass desk.obj', 'cubetx.png')]
        
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)



    def play(self):
        light = np.asarray([0.5, 1, 1])

        while 1:
            light /= np.linalg.norm(light)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
            self.z_buffer = 100000000
            self.screen.fill((0,0,0))
            self.cam.move()
            for i in self.objects:
                i.draw()
            # self.obj.draw()
            pygame.mouse.set_pos(400, 300)
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == '__main__':
    eng = Engine()
    eng.play()
