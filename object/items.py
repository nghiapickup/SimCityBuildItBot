from object.objects import BasicObject


class Metal(BasicObject):
    def __init__(self):
        super().__init__("metal")
        self.n_sample = 2


class Wood(BasicObject):
    def __init__(self):
        super().__init__("wood")
        self.n_sample = 2


class Plastic(BasicObject):
    def __init__(self):
        super().__init__("plastic")
        self.n_sample = 2


class Textile(BasicObject):
    def __init__(self):
        super().__init__("textile")
        self.n_sample = 2


class Seed(BasicObject):
    def __init__(self):
        super().__init__("seed")
        self.n_sample = 2


class Mineral(BasicObject):
    def __init__(self):
        super().__init__("mineral")
        self.n_sample = 2


class Chemical(BasicObject):
    def __init__(self):
        super().__init__("chemical")
        self.n_sample = 2
