from object.object import BasicObject

LOCK = 1
CAMERA = 2
BAR =3

BLADE = 4
EXHAUST = 5
WHEEL = 6


class Lock(BasicObject):
    def __init__(self):
        super().__init__("lock", category='special_item')
        self.n_sample = 2
        self.threshold = 0.7


class Bar(BasicObject):
    def __init__(self):
        super().__init__("bar", category='special_item')
        self.n_sample = 2
        self.threshold = 0.7


class Camera(BasicObject):
    def __init__(self):
        super().__init__("camera", category='special_item')
        self.n_sample = 2
        self.threshold = 0.7


class Blade(BasicObject):
    def __init__(self):
        super().__init__("blade", category='special_item')
        self.n_sample = 2
        self.threshold = 0.7


class Exhaust(BasicObject):
    def __init__(self):
        super().__init__("exhaust", category='special_item')
        self.n_sample = 1
        self.threshold = 0.7


class Wheel(BasicObject):
    def __init__(self):
        super().__init__("wheel", category='special_item')
        self.n_sample = 1
        self.threshold = 0.7


class SpecialItemFactory:
    item_map = {
        'lock': Lock,
        'bar': Bar,
        'camera': Camera,

        'blade': Blade,
        'exhaust': Exhaust,
        'wheel': Wheel
    }

    @staticmethod
    def from_str(item_name):
        return SpecialItemFactory.item_map[item_name]()