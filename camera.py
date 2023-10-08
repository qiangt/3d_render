import pygame as pg
from matrix_utils import *

class Camera:
    def __init__(self, render, position) -> None:
        self.render = render
        # changing to homogeneous coordinate
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100

        self.moving_speed = 0.02
        self.rotation_speed = 1.0 * math.pi / 180.0 # 1 degree in radians

        self.anglePitch = 0
        self.angleYaw = 0
        self.angleRoll = 0        

    def control(self):
        key = pg.key.get_pressed()
        # left / right
        if key[pg.K_a]:
            self.position[0] -= self.moving_speed
        if key[pg.K_d]:
            self.position[0] += self.moving_speed
        # in an out
        if key[pg.K_w]:
            self.position[2] += self.moving_speed
        if key[pg.K_s]:
            self.position[2] -= self.moving_speed
        # up and down
        if key[pg.K_q]:
            self.position[1] += self.moving_speed
        if key[pg.K_e]:
            self.position[1] -= self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)            
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)

    def camera_yaw(self, angle):
        self.angleYaw += angle

    def camera_pitch(self, angle):
        self.anglePitch += angle      

    def axiiIdentity(self):
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])

    def camera_update_axii(self):
        self.axiiIdentity()
        # translate the the cordinate origin first, then rotate and then translate it back
        transform = rotate_x(self.anglePitch) @ rotate_y(self.angleYaw)
        # transform = translate_t(+obj_center) @ rotate_y(self.angleYaw) @ rotate_x(self.anglePitch) @ translate_t(-obj_center)
        self.forward = self.forward @ transform
        self.right = self.right @ transform
        self.up = self.up @ transform

    # return the matrix to camera coordinate
    def translate_matrix(self):
        x, y, z, w = self.position

        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
    
    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        ux, uy, uz, w = self.up
        fx, fy, fz, w = self.forward

        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        self.camera_update_axii()
        return self.translate_matrix() @ self.rotate_matrix()