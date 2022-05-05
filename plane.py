import shape
import numpy as np
import ray
import vector
import Intersection

class plane(shape):
    normal = np.array()
    offset = 0.0

    def __init__(self, normal, offset, material):
        shape.__init__(material)
        self.normal = normal
        self.offset = offset

    def intersect(self, r, shadow):
        dot_prod = vector.dot_product(r.direction, self.normal)
        if abs(dot_prod < 0.01):
            return
        dprod = vector.dot_product(r.start_point, self.normal)
        t = (self.offset -dprod) / dot_prod

        if t <= 0 or np.isnan(t):
            return

        inter_point = vector.plus(r.start_point, vector.multiply(r.direction, t))
        d = pow(vector.vector_len(vector.minus(inter_point, r.start_point)), 2)

        if d < 0.01:
            return

        inter_normal = vector.multiply(self.normal, -dot_prod)

        return Intersection(inter_point, inter_normal, r.direction, self.material)