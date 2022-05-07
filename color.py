class Color:
    r = 0
    g = 0
    b = 0

    # we need to check incorrect rgb values (not in 0-1?)
    def __init__(self, r: float, g: float, b: float):
        self.r = r
        self.g = g
        self.b = b

    def plus(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def mul_color(self, other):
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def mul_scalar(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def get_red(self):
        return int(255 * self.r)

    def get_green(self):
        return int(255 * self.g)

    def get_blue(self):
        return int(255 * self.b)

    def gray_scale(self):
        outSum = self.r + self.g + self.b
        return outSum / 3
