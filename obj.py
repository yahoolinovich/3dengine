import math
import numpy as np
import pygame

class Object:
    def __init__(self, eng):
        self.eng = eng
        self.vertices = np.array([
            [-1,-1,1,1],[-1,-1,-1,1],[-1,1,1,1],[-1,1,-1,1],
            [1,1,1,1],[1,1,-1,1],[1,-1,1,1],[1,-1,-1,1]
        ])
        self.faces = np.array([
            [0,1,3,2],[3,2,4,5],[4,5,7,6],[7,6,0,1],[0,2,4,6],[7,1,3,5]
        ])

    def rotation_x(self, angle):
        x = np.array([
            [1, 0, 0,0],
            [0, math.cos(angle), math.sin(angle), 0],
            [0, math.sin(-angle), math.cos(angle), 0],
            [0,0,0,1]
        ])
        return x

    def rotation_y(self, angle):
        y = np.array([
            [math.cos(angle), 0, math.sin(-angle),0],
            [0, 1, 0,0],
            [math.sin(angle), 0, math.cos(angle),0],
            [0, 0, 0, 1]
        ])
        return y

    def rotation_z(self, angle):
        z = np.array([
            [math.cos(angle), math.sin(angle), 0,0],
            [math.sin(-angle), math.cos(angle), 0,0],
            [0, 0, 1,0],
            [0, 0, 0, 1]
        ])
        return z

    def translation(self, pos):
        x, y, z = pos
        return np.array([
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [x,y,z,1]
        ])

    def scale(self, amt):
        return np.array([
            [amt, 0, 0, 0],
            [0, amt, 0, 0],
            [0, 0, amt, 0],
            [0, 0, 0, 1]
        ])

    def camera_relation(self):
        new_vertices = self.vertices - self.eng.cam.pos
        return new_vertices

    def draw(self):
        # self.vertices = np.dot(self.vertices,self.rotation_x(math.radians(1)))
        vertices = self.camera_relation()
        print(f'1: {vertices[0]} \n')
        vertices = np.dot(vertices, self.eng.cam.project_matrix())
        print(f'2: {vertices[0]} \n')
        vertices /= vertices[:, -1].reshape(-1, 1)
        print(f'3: {vertices[0]} \n')
        vertices = np.dot(vertices, self.eng.cam.screen_projection())
        print(f'4: {vertices[0]} \n')
        for i in vertices[:,:2]:
            pygame.draw.circle(self.eng.screen, pygame.Color('red'), i, 3)
        vix = vertices[:,:2]
        for face in self.faces:
            pygame.draw.polygon(self.eng.screen, pygame.Color('white'), vix[face], 1)
