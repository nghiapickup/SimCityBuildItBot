import time
import timeit

from object import button
from object.banner_ad import BannerAd
from object.button import BntFactory
from object.item import ItemFactory
from object.object import BasicObject
from service import screen_touch, screen_capture

# Factory
FACTORY_SMALL = 1
FACTORY_BASIC = 2
FACTORY_MASS = 3

FACTORY_SLOT = {
    FACTORY_SMALL: 2,
    FACTORY_BASIC: 3,
    FACTORY_MASS: 4
}


class Factory(BasicObject):
    """
    A factory can produce only one product at a time
    """

    def __init__(self, factory_type, item_name):
        super().__init__("factory")
        self.n_sample = 2

        self.screen_touch = self.service_hub.screen_touch
        self.screen_capture = self.service_hub.screen_capture

        self.product_item = ItemFactory.from_str(item_name)
        self.num_slot = FACTORY_SLOT[factory_type]

        # Special and fixed places in factory,
        # they will be set at the first time we produce
        self.location = self.service_hub.device.screen.center
        self.next_bnt = BntFactory.make(button.BNT_RIGHT)
        self.banner_ad = BannerAd()
        self.bnt_collect = BntFactory.make(button.BNT_COLLECT)

        # produce time controlling
        self.start_time = None
        self.end_time = None

    def produce_time_left(self):
        # don't know is True
        is_done = (self.start_time is None and self.end_time is None) \
               or (timeit.default_timer() > self.end_time)
        if is_done: return 0
        return self.end_time - timeit.default_timer()

    def click_next(self, check_ad=False, sleep_in=1):
        self.logger.info(f'{self.__class__}: click_next')
        if self.next_bnt.location is None:
            screen_image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
            self.next_bnt.look(image=screen_image, save_loc=True)

        # Check whether ad is apply, only when time left > 20 mins
        # (to make sure there is no finished product outside, if is clicked, factory window will be closed)
        if check_ad and self.produce_time_left()>20*60:
            self.logger.info(f'{self.__class__}:click_next: check_ad')
            self.click() # Click center to find ad
            if self.banner_ad.watch().ok:
                return False # Watched ad, false to click

        # force to wait after click next -> change window
        self.screen_touch.execute(screen_touch.ACTION_CLICK, sleep_in=sleep_in, pixel=self.next_bnt.location)
        return True

    def _count_empty_slot(self, image):
        bnt_empty = BntFactory.make(button.BNT_EMPTY)
        find_empty = bnt_empty.look(image, get_all=True)
        if not find_empty.ok: return 0
        return len(find_empty.action_return)

    def start_produce(self):
        self.logger.info(f'{self.__class__}: start_produce {self.product_item.name}')
        if not self.look_and_wait(wait_time=1, try_time=1).ok:
            raise ModuleNotFoundError(f'{self.__class__}: Factory window is not open')
        # Save time by using previous screen shot
        screen_image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)

        # Collect all, count empty slot first, using a shared screenshot
        find_collected_bnt = self.bnt_collect.find_all_and_click(image=screen_image, try_time=0, sleep_time=0.2)
        num_collected = 0
        if find_collected_bnt.ok:
            num_collected = len(find_collected_bnt.action_return)

        empty_count = self._count_empty_slot(image=screen_image)
        empty_count = self._count_empty_slot(image=screen_image)
        total_empty = num_collected + empty_count

        if self.product_item.location is None:
            self.product_item.look(image=screen_image, save_loc=True)

        is_produced = False
        if total_empty:
            self.logger.info(f'{self.__class__}: found {total_empty} empty slot(s)')
            for _ in range(0, total_empty):
                self.screen_touch.execute(
                    screen_touch.ACTION_WIPE_TO_CENTER,
                    from_pixel=self.product_item.location,
                    n_step=3,
                    hold=0
                )
            # Set time after click
            self.start_time = timeit.default_timer()
            self.end_time = self.start_time + self.product_item.produce_time
            is_produced = True

        return is_produced
