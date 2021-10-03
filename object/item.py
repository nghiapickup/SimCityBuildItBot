from object.object import BasicObject

# Factory
EMPTY = 0
METAL = 1
WOOD = 2
PLASTIC = 3
SEED = 4
MINERAL = 5
CHEMICAL = 6
TEXTILE = 7
SUGAR = 8

ITEM_STR = {
    'empty': EMPTY,
    'metal': METAL,
    'wood': WOOD,
    'plastic': PLASTIC,
    'seed': SEED,
    'mineral': MINERAL,
    'chemical': CHEMICAL,
    'textile': TEXTILE,
    'sugar': SUGAR
}


class BasicItem(BasicObject):
    def __init__(self, name):
        super().__init__(name)
        self.produce_time = None
        self.produce_time_off = None
        self.threshold = 0.9

    def set_produce_time(self, time, time_off):
        assert  time > time_off, \
            f'{self.__class__}: produce_time must be > produce_time_off'
        self.produce_time_off = time_off
        self.produce_time = time - time_off


class EmptyBox(BasicItem):
    def __init__(self):
        super().__init__("empty_box")
        self.n_sample = 2


class Metal(BasicItem):
    def __init__(self):
        super().__init__("metal")
        self.n_sample = 2
        self.set_produce_time(1*60, 2)



class Wood(BasicItem):
    def __init__(self):
        super().__init__("wood")
        self.n_sample = 2
        self.set_produce_time(3*60, 2)


class Plastic(BasicItem):
    def __init__(self):
        super().__init__("plastic")
        self.n_sample = 2
        self.set_produce_time(9*60, 2)


class Seed(BasicItem):
    def __init__(self):
        super().__init__("seed")
        self.n_sample = 2
        self.set_produce_time(20*60, 2)


class Mineral(BasicItem):
    def __init__(self):
        super().__init__("mineral")
        self.n_sample = 2
        self.set_produce_time(30*60, 2)


class Chemical(BasicItem):
    def __init__(self):
        super().__init__("chemical")
        self.n_sample = 2
        self.set_produce_time(2*60*60, 2)


class Textile(BasicItem):
    def __init__(self):
        super().__init__("textile")
        self.n_sample = 2
        self.set_produce_time(3*60*60, 2)


class Sugar(BasicItem):
    def __init__(self):
        super().__init__("sugar")
        self.n_sample = 2
        self.set_produce_time(4*60*60, 2)


class ItemFactory:
    item_map = {
        EMPTY: EmptyBox,
        METAL: Metal,
        WOOD: Wood,
        PLASTIC: Plastic,
        SEED: Seed,
        MINERAL: Mineral,
        CHEMICAL: Chemical,
        TEXTILE: Textile,
        SUGAR: Sugar
    }

    @staticmethod
    def from_id(item_id):
        return ItemFactory.item_map[item_id]()

    @staticmethod
    def from_str(item_name):
        return ItemFactory.item_map[ITEM_STR[item_name]]()