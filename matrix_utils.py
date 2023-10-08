import math
import numpy as np

# we are using the left hand coordinate system and matrix on the right hand side
# up: y, right: x, inward: z

translate_t = lambda pos: np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [pos[0], pos[1], pos[2], 1],
], dtype=np.float32)

rotate_x = lambda alpha: np.array([
    [1, 0, 0, 0],
    [0, math.cos(alpha), math.sin(alpha), 0],
    [0, -math.sin(alpha), math.cos(alpha), 0],
    [0, 0, 0, 1],
], dtype=np.float32)

rotate_y = lambda theta: np.array([
    [math.cos(theta), 0, -math.sin(theta), 0],
    [0, 1, 0, 0],
    [math.sin(theta), 0, math.cos(theta), 0],
    [0, 0, 0, 1],
], dtype=np.float32)

rotate_z = lambda sigma: np.array([
    [math.cos(sigma), math.sin(sigma), 0, 0],
    [-math.sin(sigma), math.cos(sigma), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
], dtype=np.float32)

scale_a = lambda a: np.array([
    [a, 0, 0, 0],
    [0, a, 0, 0],
    [0, 0, a, 0],
    [0, 0, 0, 1],
])

