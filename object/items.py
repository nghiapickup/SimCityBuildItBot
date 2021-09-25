import cv2
from object.objects import BasicObject


class Metal(BasicObject):
    def __init__(self):
        super().__init__("metal")

class Wood(BasicObject):
    def __init__(self):
        super().__init__("wood")


class Plastic(BasicObject):
    def __init__(self):
        super().__init__("plastic")


class Textile(BasicObject):
    def __init__(self):
        super().__init__("textile")


class Seed(BasicObject):
    def __init__(self):
        super().__init__("seed")


class Mineral(BasicObject):
    def __init__(self):
        super().__init__("mineral")


class Chemical(BasicObject):
    def __init__(self):
        super().__init__("chemical")