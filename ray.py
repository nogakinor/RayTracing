import vector
import numpy as np

class ray:
    start_point = np.array()
    direction = np.array()

    def __init__(self, start_point, direction):
        self.direction = direction
        self.start_point = start_point