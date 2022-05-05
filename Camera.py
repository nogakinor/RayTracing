import numpy as np
import vector

class Camera:
    position = np.array()
    look_at = np.array()
    up = np.array()
    screen_d = 0
    screen_w = 0
    right = np.array()
    x = [3]

    def __init__(self, position, look_at, up, screen_d, screen_w, right, x):
        self.position = position
        self.look_at = vector.normalized(vector.minus(look_at,position))
        self.up = vector.normalized(vector.projected_left(up, self.look_at))
        self.screen_d = screen_d
        self.screen_w = screen_w
        self.right = vector.normalized(vector.cross_product(up, self.look_at))




