import numpy as np
import vector


class Camera:
    # CTRL+/ to comment or uncomment uncomment
    # # 3D vectors:
    # position = np.zeros(3)
    # look_at = np.zeros(3)
    # up = np.zeros(3)
    # # doubles:
    # screen_d = 0
    # screen_w = 0
    # # 3d Vector:
    # right = np.zeros(3)
    # # 10 sized vector
    # x = [3]

    # position, look_at,up,right are 3D vectors.
    # screen_d, screen_w are numbers.
    # x is an array of 10 integers.
    def __init__(self, position, look_at, up, screen_d, screen_w):
        # Normalize Vectors from input.
        self.position = position
        self.look_at = vector.normalized(vector.minus(look_at, position))
        self.up = vector.normalized(vector.projected_left(up, self.look_at))
        self.screen_d = screen_d
        self.screen_w = screen_w
        self.right = vector.normalized(vector.cross_product(up, self.look_at))
        self.x = np.zeros(10, dtype=int)
