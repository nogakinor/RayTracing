import numpy as np
import Color

class light_point:
    position = np.array()
    color = Color()
    specular = 0.0
    shadow = 0.0
    radius = 0.0

    def __init__(self, position, color, specular, shadow, radius):
        self.position = position
        self.color = color
        self.specular = specular
        self.shadow = shadow
        self.radius = radius


