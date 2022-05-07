import color


class Material:
    # diffuse = Color()
    # specular = Color()
    # reflection = Color()
    # phong = 0.0
    # trans = 0.0

    def __init__(self, diffuse: color.Color, specular: color.Color, reflection: color.Color, phong: float, trans: float):
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.phong = phong
        self.trans = trans
