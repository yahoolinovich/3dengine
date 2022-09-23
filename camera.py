import math
import numpy as np
import pygame.key


class Camera:
    def __init__(self, eng, pos):
        self.eng = eng
        self.pos = np.array([*pos, 0.0])
        self.H_FOV = math.pi / 3
        self.V_FOV = self.H_FOV * (eng.height / eng.width)
        self.clip_near = 100
        self.clip_far = 10000.0

    def move(self):
        key = pygame.key.get_pressed()
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_rel()
        print(mouse_pos_x, mouse_pos_y)
        speed = 5
        rot_speed = 0.003
        diff = self.eng.obj.camera_relation()
        if key[pygame.K_s]:
            self.pos -= [0, 0, speed, 0]
        if key[pygame.K_w]:
            self.pos += [0, 0, speed, 0]
        if key[pygame.K_a]:
            self.pos -= [speed, 0, 0, 0]
        if key[pygame.K_d]:
            self.pos += [speed, 0, 0, 0]

        if mouse_pos_y < 0:
            self.eng.obj.vertices = self.eng.obj.vertices @ self.pitch(rot_speed * mouse_pos_y)
        if mouse_pos_y > 0:
            self.eng.obj.vertices = self.eng.obj.vertices @ self.pitch(rot_speed * mouse_pos_y)
        if mouse_pos_x < 0:
            self.eng.obj.vertices = self.eng.obj.vertices @ self.yaw(rot_speed * mouse_pos_x)
        if mouse_pos_x > 0:
            self.eng.obj.vertices = self.eng.obj.vertices @ self.yaw(rot_speed * mouse_pos_x)

    def normalize_x(self):
        x = fov(self.H_FOV)
        return x

    def normalize_y(self):
        y = fov(self.V_FOV)
        return y

    def normalize_z(self):
        z = (self.clip_far)/(self.clip_far-self.clip_near)
        return z

    def project_matrix(self):
        return np.array([
            [self.normalize_x(),0,0,0],
            [0,self.normalize_y(),0,0],
            [0,0,self.normalize_z(),1],
            [0,0,(-self.clip_far * self.clip_near) / (self.clip_far - self.clip_near),0]#(self.clip_near * self.clip_far * 2) / (self.clip_near - self.clip_far),0]
        ])

    def pitch(self,a):
        x,y,z,w = self.pos
        return np.array([
            [1,0,0,0],
            [0,math.cos(a),-math.sin(a),0],
            [0,math.sin(a),math.cos(a),0],
            [0,0,0,1]
        ])

    def yaw(self,angle):
            y = np.array([
                [math.cos(angle), 0, math.sin(angle), 0],
                [0, 1, 0, 0],
                [math.sin(-angle), 0, math.cos(angle), 0],
                [0, 0, 0, 1]
                ])
            return y

    def screen_projection(self):
        return np.array([
            [self.eng.width / 2,0,0,0],
            [0,-self.eng.height / 2,0,0],
            [0,0,1,0],
            [(self.eng.width / 2),(self.eng.height / 2),0,1]
        ])


def fov(angle):
    x = 1/(math.tan(angle/2))
    return x
