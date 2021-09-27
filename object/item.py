from object.object import BasicObject

# Item type id
METAL = 1
WOOD = 2
PLASTIC = 3
SEED = 4
MINERAL = 5
CHEMICAL = 6
TEXTILE = 7

ITEM_STR = {
    'metal': METAL,
    'wood': WOOD,
    'plastic': PLASTIC,
    'seed': SEED,
    'mineral': MINERAL,
    'chemical': CHEMICAL,
    'textile': TEXTILE
}


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


class ItemFactory:
    item_map = {
        METAL: Metal,
        WOOD: Wood,
        PLASTIC: Plastic,
        SEED: Seed,
        MINERAL: Mineral,
        CHEMICAL: Chemical,
        TEXTILE: Textile
    }

    @staticmethod
    def make(item_id):
        return ItemFactory.item_map[item_id]()