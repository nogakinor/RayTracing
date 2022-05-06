
class Color:
    r = 0
    g = 0
    b = 0

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def plus(self, other):
        return Color(self.r + other.r, self.g+other.g, self.b+other.b)

    def mul_color(self, other):
        return Color(self.r * other.r, self.g*other.g , self.b*other.b)

    def mul_scalar(self, scalar):
        return Color(self.r*scalar, self.g*scalar, self.b*scalar)

    def get_red(self):
        return bytes(255*self.r)

    def get_green(self):
        return bytes(255*self.g)

    def get_blue(self):
        return bytes(255*self.b)

    def gray_scale(self):
        sum = self.r + self.g + self.b
        return sum/3