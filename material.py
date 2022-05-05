import Color

class material:
    diffuse = Color()
    specular = Color()
    reflection = Color()
    phong = 0.0
    trans = 0.0

    def __init__(self, diffuse, specular, reflection, phong, trans):
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.phong = phong
        self.trans = trans