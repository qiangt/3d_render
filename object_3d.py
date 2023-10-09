import pygame as pg
from matrix_utils import *

class Object3D:
    def __init__(self, render, vertices=None, faces=None) -> None:
        self.render = render

        # vertices are in homogeneous coordinate
        if vertices is None or faces is None:
            self.vertices = np.array([
                (0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1), 
                (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1), 
            ])

            # the order is important, I always start from left-bottom and go clock-wise
            self.faces = np.array([
                (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (3, 2, 6, 7),
                (1, 5, 6, 2), (0, 4, 7, 3)
            ])
        else:
            self.vertices = vertices
            self.faces = faces

        self.movement_flag, self.draw_vertices = False, True            

    def draw(self):
        self.screen_project()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(-(pg.time.get_ticks() % 0.005))

    def screen_project(self):
        # to camera coordinate first
        vertices = self.vertices @ self.render.camera.camera_matrix()
        # project to frustum
        vertices = vertices @ self.render.projection.project_matrix
        # normalization
        vertices /= vertices[:, -1].reshape(-1, 1)
        # clipping
        vertices[(vertices > 2) | (vertices < -2)] = 0
        # to screen
        vertices = vertices @ self.render.projection.to_screen_matrix
        # get 2D
        vertices = vertices[:, :2]       

        for face in self.faces:
            polygon = vertices[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), polygon, 3)

        if self.draw_vertices:
            for vertex in vertices:
                if not np.any( (vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT) ):
                    pg.draw.circle(self.render.screen, pg.Color('red'), vertex, 6)

    def get_center(self):
        center = np.mean(self.vertices, axis=0)
        return center

    def translate(self, pos):
        self.vertices = self.vertices @ translate_t(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale_a(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)        