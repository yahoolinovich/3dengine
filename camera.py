import math
import numpy as np
import pygame.key


class Camera:
    def __init__(self, eng, pos):
        self.eng = eng
        self.proj_cam = np.array([*pos, 0.0])
        self.rot_cam = np.array([2, 0.0])
        self.H_FOV = math.pi / 4
        self.V_FOV = self.H_FOV * (eng.height / eng.width)
        self.clip_near = 100
        self.clip_far = 10000.0

    def move(self):
        key = pygame.key.get_pressed()
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_rel()
        speed = 5
        mouse_sensitivity = 0.001
        if key[pygame.K_s]:
            self.proj_cam -= [math.cos(self.rot_cam[0]) * speed, 0, math.sin(self.rot_cam[0]) * speed, 0]
        if key[pygame.K_w]:
            self.proj_cam += [math.cos(self.rot_cam[0]) * speed, 0, math.sin(self.rot_cam[0]) * speed, 0]
        if key[pygame.K_a]:
            self.proj_cam += [math.cos(self.rot_cam[0] + (math.pi/2)) * speed, 0, math.sin(self.rot_cam[0] + (math.pi/2)) * speed, 0]
        if key[pygame.K_d]:
            self.proj_cam += [math.cos(self.rot_cam[0] - (math.pi/2)) * speed, 0, math.sin(self.rot_cam[0] - (math.pi/2)) * speed, 0]

        if mouse_pos_y < 0:
            self.rot_cam[1] -= mouse_sensitivity * mouse_pos_y
        elif mouse_pos_y > 0:
            self.rot_cam[1] -= mouse_sensitivity * mouse_pos_y
        if mouse_pos_x < 0:
            self.rot_cam[0] -= mouse_sensitivity * mouse_pos_x
        elif mouse_pos_x > 0:
            self.rot_cam[0] -= mouse_sensitivity * mouse_pos_x

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
            [0,0,(-self.clip_far * self.clip_near) / (self.clip_far - self.clip_near),0]
        ])

    def pitch(self,a):
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
