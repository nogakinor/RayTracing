import shape
import numpy as np
import ray
import vector
import intersection
import material
import shape
import ray


class Plane(shape.Shape):
    # normal = np.array()
    # offset = 0.0

    def __init__(self, normal: np.ndarray, offset: float, inputMaterial: material.Material):
        shape.Shape.__init__(self, inputMaterial)
        self.normal = vector.normalized(normal)
        self.offset = offset

    def intersect(self, inputRay: ray.Ray, shadow:bool):
        dot_prod = vector.dot_product(inputRay.direction, self.normal)
        if abs(dot_prod < 0.01):
            return
        dprod = vector.dot_product(inputRay.start_point, self.normal)
        t = (self.offset - dprod) / dot_prod

        if t <= 0 or np.isnan(t):
            return

        inter_point = vector.add(inputRay.start_point, vector.multiply(inputRay.direction, t))
        d = pow(vector.vector_len(vector.minus(inter_point, inputRay.start_point)), 2)

        if d < 0.01:
            return

        inter_normal = vector.multiply(self.normal, -dot_prod)

        return intersection.Intersection(inter_point, inter_normal, inputRay.direction, self.material)
