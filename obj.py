import math
import numpy as np
import pygame


class Object:
    def __init__(self, eng, file_name, texture):
        self.eng = eng
        self.file_name = file_name
        self.texture = texture
        self.vertices, self.faces, self.uv, self.tex_map, self.textured = self.open_obj(self.file_name, texture)

    def open_obj(self, filename, texture):
        vertices = []
        faces = []
        uv = []
        textures_map = []
        with open(filename) as file:
            for line in file:
                if line.startswith('v '):
                    lines = line[2:].split()
                    v = [float(i) for i in lines]
                    vertices.append(v)
                    
                elif line.startswith('vt '):
                    uv.append(line[3:].split())
                    
                elif line.startswith('f '):
                    lines_2 = line[2:].split()
                    fc = [i.split('/') for i in lines_2]
                    if len(fc) == 1:
                        faces.append([lines_2[0], lines_2[1], lines_2[2]])

                        if len(lines_2) > 3:
                            faces.append([lines_2[0], lines_2[2], lines_2[3]])

                    else:
                        faces.append([fc[0][0],fc[1][0],fc[2][0]])
                        textures_map.append([fc[0][1],fc[1][1],fc[2][1]])
                        
                        if len(fc) > 3:
                            faces.append([fc[0][0], fc[2][0], fc[3][0]])
                            textures_map.append([fc[0][1], fc[2][1], fc[3][1]])

        vertices = np.asarray(vertices).astype(float)
        faces = np.asarray(faces).astype(int)

        if len(uv) > 0 and len(textures_map) > 0:
            textured = True
            uv = np.asarray(uv).astype(float)
            uv[:, 1] = 1 - texture_uv[:, 1]
            textures_map = np.asarray(textures_map).astype(int) - 1

        else:
            uv, textures_map = np.asarray(uv), np.asarray(texture_map)
            textured = False

        return vertices, faces, uv, textures_map, textured

    def rotation_x(self, angle):
        x = np.array([
            [1, 0, 0, 0],
            [0, math.cos(angle), math.sin(angle), 0],
            [0, math.sin(-angle), math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
        return x

    def rotation_y(self, angle):
        y = np.array([
            [math.cos(angle), 0, math.sin(-angle), 0],
            [0, 1, 0, 0],
            [math.sin(angle), 0, math.cos(angle), 0],
            [0, 0, 0, 1]
        ])
        return y

    def rotation_z(self, angle):
        z = np.array([
            [math.cos(angle), math.sin(angle), 0, 0],
            [math.sin(-angle), math.cos(angle), 0, 0],
            [0, 0, 1, 0],
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
        new_vertices1 = new_vertices.copy()
        
        new_vertices1 = new_vertices @ self.eng.cam.yaw(-self.eng.cam.rot_cam[3] + math.pi / 2)
        new_vertices = new_vertices1 @ self.eng.cam.pitch(-self.eng.cam.rot_cam[3])

        new_vertices[:, 2][(new_vertices[:,2] < 0.01) & (new_vertices[:, 2] > -0.01)] = -0.01

        return new_vertices

    def draw(self):
        vertices = self.camera_relation()
        vertices = np.dot(vertices, self.eng.cam.project_matrix())
        vertices /= vertices[:, -1].reshape(-1, 1)
        vertices = np.dot(vertices, self.eng.cam.screen_projection())

        for i in vertices[:,:2]:
            pygame.draw.circle(self.eng.screen, pygame.Color('red'), i, 2)
        vix = vertices[:,:2]
        for face in self.faces:
            pygame.draw.polygon(self.eng.screen, pygame.Color('white'), vix[face], 1)

