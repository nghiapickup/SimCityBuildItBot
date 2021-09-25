class Pixel:
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Pixel(self.x + other.x, self.y + other.y)

    def diff_range(self, other, n_step):
        return Pixel((other.x - self.x)/n_step, (other.y - self.y)/n_step)


class Screen:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.center = Pixel(self.x_size/2, self.y_size/2)
