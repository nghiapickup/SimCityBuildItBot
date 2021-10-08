import time

from object import button
from object.banner_ad import BannerAd
from object.button import BntFactory
from object.display import Pixel
from object.item import ItemFactory
from object.object import BasicObject
from service import screen_touch, screen_capture
from utils.config import Config

# Factory ID
FACTORY = 1

FACTORY_ID_TO_NAME = {
    FACTORY: 'factory'
}


class ProducingSlot(BasicObject):
    EMPTY = 1
    IN_PROGRESS = 2

    def __init__(self, item, found_return, status):
        super(ProducingSlot, self).__init__('producing_box')
        self.producing_item = item
        self.status = status
        loc, _, _ = found_return
        self.location = loc
        self.finish_time = None
        if self.status == ProducingSlot.EMPTY:
            self.finish_time = 0

    def is_empty(self):
        return self.status == ProducingSlot.EMPTY

    def __lt__(self, other):
        # sort by boxes priority
        righter = self.location.y > other.location.y
        lower = (self.location.y == other.location.y) and (self.location.x < other.location.x)
        return righter or lower


class ManufacturerMeta(type):
    def __new__(mcs, name, bases, body):
        if name!='Manufacturer' and '_init_producing_time' not in body:
            raise TypeError(f"_init_producing_time is not defined in {name}!")
        if name!='Manufacturer' and 'start_produce' not in body:
            raise TypeError(f"start_produce is not defined in {name}!")
        return super().__new__(mcs, name, bases, body)


class Manufacturer(BasicObject, metaclass=ManufacturerMeta):
    def __init__(self, factory_id):
        name = FACTORY_ID_TO_NAME[factory_id]
        super(Manufacturer, self).__init__(name)

        self._init_config()
        self.producing_slots = []
        self.next_release_time = 0

    def _init_config(self):
        config = Config.get_instance().building_config
        base_product_names = config.__getattribute__(self.name)['base_products']
        self.base_product_list = [ItemFactory.from_str(name) for name in base_product_names]

        self.location = self.service_hub.device.screen.center

        # area where producing list is located
        producing_constraint = self.object_location.parse_location('manufacturer', 'producing_area')
        self.producing_area = [Pixel(int(producing_constraint.x - 50), 0),
                               Pixel(int(self.device.screen.x_size), int(self.device.screen.y_size))]

        # function items
        self.bnt_next = BntFactory.make(button.BNT_RIGHT)
        self.bnt_next.location = self.object_location.parse_location('manufacturer', 'bnt_next')
        self.banner_ad = BannerAd()
        self.bnt_collect = BntFactory.make(button.BNT_COLLECT)

    def _update_next_release_time(self):
        # ==0 if all are empty
        slot_times = [slot.finish_time for slot in self.producing_slots if self.producing_slots != ProducingSlot.EMPTY]
        self.next_release_time = min(slot_times) if len(slot_times) else 0

    def _extract_time_boxes(self, image,show=False):
        # find time button and match with producing list
        bnt_time = BntFactory.make(button.BNT_TIME)
        found_boxes = bnt_time.look(image=image, get_all=True)
        if found_boxes.ok:
            res = self.extract_location_and_text(image=image,
                                                 find_action_return=found_boxes.action_return,
                                                 text_filter=self.get_time_from_text,
                                                 show=show)
        else:
            self.logger.info(f'{self.__class__}: Cannot find bnt_time!')
            return []
        return res

    def init_producing_list(self, image, show=False):
        producing_image = self.apply_restricted_box(image, self.producing_area)
        # Check all base_product_list and matching with producing list
        for item in self.base_product_list:
            find_items = item.look(image=producing_image, get_all=True)
            if find_items.ok:
                for found_return in find_items.action_return:
                    new_box = ProducingSlot(item, found_return, ProducingSlot.IN_PROGRESS)
                    self.producing_slots.append(new_box)

        # Check emptybox
        empty_box = ItemFactory.from_str('empty')
        find_empty_box = empty_box.look(image=producing_image, get_all=True, show=show)
        if find_empty_box.ok:
            for found_box in find_empty_box.action_return:
                new_box = ProducingSlot(empty_box, found_box, ProducingSlot.EMPTY)
                self.producing_slots.append(new_box)

        # Order producing list by location
        self.producing_slots.sort(reverse=True)

        # Find time boxes and match with proding list by distance
        time_boxes = self._extract_time_boxes(producing_image, show=show)
        flag = self._init_producing_time(time_boxes=time_boxes)
        assert flag is not None, "_init_producing_time() has not defined yet!"
        self._update_next_release_time()

        current_time = time.time()
        log_info = [(slot.producing_item.name, slot.finish_time - current_time, slot.status) for slot in
                    self.producing_slots]
        self.logger.info(f'{self.__class__}:init {self.name}:{log_info}')
        return True

    def click_next(self, check_ad=False, sleep_in=1):
        self.logger.info(f'{self.__class__}: click_next, check_ad={check_ad}')
        if check_ad:
            # Check whether ad is apply, only when time left > 10 mins
            # (to make sure there is no finished product outside, if is clicked, factory window will be closed)
            time_left = time.time() - self.next_release_time
            if time_left > 10 * 60:
                self.logger.info(f'{self.__class__}:click_next: check_ad')
                self.click(wait_open_window=True)  # Click center to find ad
                if self.banner_ad.watch().ok:
                    for slot in self.producing_slots:
                        slot.finish_time=0 # Update finish_time and return
                    return False  # Watched ad, false to click
        # force to wait after click next -> change window
        self.screen_touch.execute(screen_touch.ACTION_CLICK,
                                  sleep_in=sleep_in,
                                  pixel=self.bnt_next.location)
        return True

    def collect_finish_product(self):
        self.logger.info('Start collect_finish_product')
        current_time = time.time()
        collected = False
        for slot in self.producing_slots:
            remaining_time = slot.finish_time-current_time
            if not slot.is_empty() and remaining_time <= 2:
                if remaining_time >= -1:
                    # wait at least 1s to collect fresh-hot items
                    self.sleep(abs(remaining_time), 'Remaining time is small.')
                collected = True
                self.click(sleep_in=0.25)
                slot.status = ProducingSlot.EMPTY

        if collected:
            self.click(wait_open_window=True)  # click again to return manufacturer window

    def assert_current_window(self):
        find = self.look()
        image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
        if not find.ok: # temp click adapt mismatch
            ad_banner = BannerAd()
            if ad_banner.look(image=image).ok:
                ad_banner.watch()
                self.sleep(2)
                for slot in self.producing_slots:
                    slot.finish_time = 0
                self.collect_finish_product()
            self.click(wait_open_window=True)
            assert self.look().ok, f'{self.__class__}: {self.name} window is not open!'
        return self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
