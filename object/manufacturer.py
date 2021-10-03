import re
import queue
from object import button
from object.button import BntFactory
from object.display import Pixel
from object.item import ItemFactory
from object.object import BasicObject


class ProducingBox(BasicObject):
    EMPTY = 1
    IN_PROGRESS = 2
    DONE = 3

    def __init__(self, item):
        super(ProducingBox, self).__init__('producing_box')
        self.status = None
        self.producing_item = item
        self.end_producing_time = None


class Manufacturer(BasicObject):
    def __init__(self, name, base_product_names):
        super(Manufacturer, self).__init__(name)
        # Restricted screen area for producing box: 1/4 of bottom screen

        self.base_product_list = [ItemFactory.from_str(name) for name in base_product_names]
        empty_box = ItemFactory.from_str('empty')
        self.base_product_list.append(empty_box)
        self.producing_list = queue.Queue()
        self.producing_list = []

    def update_producing_list(self, image, show=False):
        producing_image = self.apply_restricted_box(image, self.producing_area)
        # Check all base_product_list and matching with producing list
        for item in self.base_product_list:
            find_items = item.look(image=producing_image, get_all=True, show=show)
            if find_items.ok:
                for _ in find_items.action_return:
                    new_box = ProducingBox(item)
                    self.producing_list.append(new_box)
