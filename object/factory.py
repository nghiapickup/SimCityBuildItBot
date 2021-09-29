import time
import timeit

from object import button
from object.banner_ad import BannerAd
from object.button import BntFactory
from object.item import ItemFactory
from object.object import BasicObject
from service import screen_touch

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

        self.product_item = ItemFactory.from_str(item_name)
        self.num_slot = FACTORY_SLOT[factory_type]

        # Special and fixed places in factory,
        # they will be set at the first time we produce
        self.location = self.service_hub.device.screen.center
        self.next_bnt = BntFactory.make(button.BNT_RIGHT)
        self.banner_ad = BannerAd()
        self.bnt_collect = BntFactory.make(button.BNT_COLLECT)

        # produce time controling
        self.start_time = None
        self.end_time = None

    def produce_time_left(self):
        # don't know is True
        is_done = (self.start_time is None and self.end_time is None) \
               or (timeit.default_timer() > self.end_time)
        if is_done: return 0
        return self.end_time - timeit.default_timer()

    def click_next(self, check_ad=False):
        self.logger.info(f'{self.__class__}: click_next')
        if self.next_bnt.location is None:
            self.next_bnt.look(save_loc=True)

        # Check whether ad is apply
        if check_ad:
            self.logger.info(f'{self.__class__}:click_next: check_ad')
            self.click() # Click center to find ad
            if self.banner_ad.look_and_wait().ok and self.banner_ad.watch().ok:
                return False # Watched ad, false to click

        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=self.next_bnt.location, sleep_in=1)
        return True

    def _count_empty_slot(self):
        bnt_empty = BntFactory.make(button.BNT_EMPTY)
        find_empty = bnt_empty.look(get_all=True)
        if not find_empty.ok: return 0
        return len(find_empty.action_return)

    def start_produce(self):
        self.logger.info(f'{self.__class__}: start_produce {self.product_item.name}')
        if self.product_item.location is None:
            self.product_item.look(save_loc=True)

        # Collect all finished item first
        # find collect button (no re-find if is not) and click all (no wait after click)
        # it is safe for click and find again
        self.bnt_collect.find_all_and_click(sleep_time=0.15)

        is_produced = False
        empty_count = self._count_empty_slot()
        if empty_count:
            self.logger.info(f'{self.__class__}: found {empty_count} empty slot(s)')
            for _ in range(0, empty_count):
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
