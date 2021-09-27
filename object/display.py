import math

from utils.config import Config

"""
Pixel and Screen follow top-left xy-coordinator with non-rotated screen
"""


class Pixel:
    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __init__(self, x, y, convert_to_xy_device=False):
        config = Config.get_instance().device_config
        self.screen_x = config.screen_x
        self.screen_y = config.screen_y

        self.x = x
        self.y = y
        if convert_to_xy_device: self._to_device_xy()

    def __add__(self, other):
        return Pixel(self.x + other.x, self.y + other.y)

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __le__(self, other):
        return (self.x <= other.x) and (self.y <= other.y)

    def __ge__(self, other):
        return (self.x >= other.x) and (self.y >= other.y)

    def _to_device_xy(self):
        # Revert x and y axes
        temp = self.x
        self.x = self.y
        self.y = temp
        # Flip by x axis
        self.x = self.screen_x - self.x
        return self

    @classmethod
    def from_cv_point(cls, cv_point):
        return cls(cv_point[0], cv_point[1], convert_to_xy_device=True)

    def get_cv_point(self):
        return self.y, self.screen_x - self.x

    def diff_range(self, other, n_step):
        return Pixel((other.x - self.x)/n_step, (other.y - self.y)/n_step)

    def is_in(self, box=None):
        """
        Whether current Pixel is in a bounced box
        :param box: tuple of 2 Top-left and Bottom-right pixels of the box, if None, the fullscreen is applied
        :return:
        """
        box_top, box_bottom = (Pixel(0,0), Pixel(self.screen_x, self.screen_y)) if box is None else (box[0], box[1])
        return box_top <= self <= box_bottom


class Screen:
    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.center = Pixel(self.x_size/2, self.y_size/2)
