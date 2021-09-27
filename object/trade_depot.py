from object.display import Pixel
from object.object import BasicObject
from service import screen_touch
from job.hub import WatchAd


class TradeDepot(BasicObject):
    def __init__(self):
        super().__init__('trade_depot')
        self.n_sample = 1

    def click_from_factory(self):
        self.service.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=Pixel(60, 500), sleep_in=2)

        count = 0
        ad_watch = WatchAd()
        while count < 2 and self.look() is None:
            count += 1
            ad_watch.execute(wait_time=0)
            self.service.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=Pixel(60, 500), sleep_in=2)

        if count == 2: return False
        return True
