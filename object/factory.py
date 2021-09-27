from object.item import ItemFactory, ITEM_STR
from object.object import BasicObject
from utils.config import Config

# Factory
FACTORY_SMALL = 1
FACTORY_BASIC = 2
FACTORY_MASS = 3


class Factory(BasicObject):
    def __init__(self, factory_type):
        super().__init__("factory")
        self.n_sample = 2

        building_config = Config.get_instance().building_config
        self.max_quantity = building_config.factory_count
        produce_list_name = building_config.factory_produce_list
        assert(len(produce_list_name) == self.max_quantity,
               f'Factory number is different from produce_list size({produce_list_name} != {self.max_quantity})')
        self.produce_list = [ItemFactory.make(ITEM_STR[name]) for name in produce_list_name]

        self.slot_number = {
            FACTORY_SMALL: 2,
            FACTORY_BASIC: 3,
            FACTORY_MASS: 4
        }[factory_type]