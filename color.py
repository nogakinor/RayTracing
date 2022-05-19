class Color:
    # we need to check incorrect rgb values (not in 0-1?)
    def __init__(self, r: float, g: float, b: float):
        self.r = self.round_number(r)
        self.g = self.round_number(g)
        self.b = self.round_number(b)

    def round_number (self, col) :
        if col < 0: col = 0
        elif col >1: col = 1
        return col

    def plus(self, other):
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def mul_color(self, other):
        return Color(self.r * other.r, self.g * other.g, self.b * other.b)

    def mul_scalar(self, scalar):
        return Color(self.r * scalar, self.g * scalar, self.b * scalar)

    def get_red(self):
        return self.r

    def get_green(self):
        return self.g

    def get_blue(self):
        # return 255 * self.b
        return self.b

    def gray_scale(self):
        outSum = self.r + self.g + self.b
        return outSum / 3
