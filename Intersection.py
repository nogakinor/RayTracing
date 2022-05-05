import vector
import material
import numpy as np

class Intersection:
    inter_point = np.array()
    normal = np.array()
    direction = np.array()
    material = np.array()

    def __init__(self, inter_point, normal, direction, material):
        self.inter_point = inter_point
        self.normal = normal
        self.direction = direction
        self.material = material

