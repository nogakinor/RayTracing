import vector
import shape
import math
import Intersection
import numpy as np

class sphere(shape):
    center = vector()
    radius = 0.0
    radius_sq = 0.0

    def __init__(self, center, radius, material):
        shape.__init__(material)
        self.center = center
        self.radius = radius
        self.radius_sq = radius*radius

    def intersect(self, ray, shadow):
        l = vector.minus(self.center, ray.start_point)
        tca = vector.dot_product(l, ray.direction)
        if tca < 0:
            return
        l_dot_p = vector.dot_product(l, l)
        d_square = l_dot_p - (tca*tca)
        if d_square > self.radius_sq:
            return
        if l_dot_p < self.radius_sq:
            if shadow :
                return Intersection(ray.start_point, vector.negative(vector.normalized(l)), ray.direction, self.material)
            else:
                return

        thc = math.sqrt(self.radius_sq - d_square)
        inter_point = vector.plus(ray.start_point, vector.multiply(ray.direction, tca-thc))
        inter_normal = vector.normalized(vector.minus(inter_point, self.center))
        return Intersection(inter_point, inter_normal, ray.direction, self.material)
