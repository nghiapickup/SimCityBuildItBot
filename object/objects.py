import time

import cv2

from service.config import Config
from service.hub import ServiceHub
from service import screen_capture, screen_touch
from service.log import LogHandle

# Item
METAL = 1
WOOD = 2
PLASTIC = 3
TEXTILE = 4
SEED = 5
MINERAL = 6
CHEMICAL = 7

# Button
BNT_EMPTY = 100
BNT_TRADE_NEW = 101
BNT_COLLECT = 102
BNT_AD_WATCH = 103
BNT_AD_CLOSE = 104
BNT_AD_REWARD = 105
BNT_NO_THANKS = 106
BNT_TRADE_PLUS = 107
BNT_TRADE_DONE = 108
BNT_CLOSE_BLUE = 109
BNT_TRADE_PUT = 110
BNT_AD_REWARD_COLLECTED = 111

# People opinion
OPINION_BLUE = 1000
OPINION_SIMOLEON = 1001

ObjectId = {
    'metal': METAL,
    'wood': WOOD,
    'plastic': PLASTIC,
    'textile': TEXTILE,
    'seed': SEED,
    'mineral': MINERAL,
    'chemical': CHEMICAL,

    'bnt_empty': BNT_EMPTY,
    'bnt_trade_new': BNT_TRADE_NEW,
    'bnt_collect': BNT_COLLECT,
    'bnt_ad_watch': BNT_AD_WATCH,
    'bnt_ad_close': BNT_AD_CLOSE,
    'bnt_ad_reward': BNT_AD_REWARD,
    'bnt_no_thanks': BNT_NO_THANKS,
    'bnt_trade_plus': BNT_TRADE_PLUS,
    'bnt_trade_done': BNT_TRADE_DONE,
    'bnt_close_blue': BNT_CLOSE_BLUE,
    'bnt_trade_put': BNT_TRADE_PUT,
    'bnt_ad_reward_collected': BNT_AD_REWARD_COLLECTED,

    'opinion_blue': OPINION_BLUE,
    'opinion_simoleon': OPINION_SIMOLEON
}


class BasicObject:
    _image_dir = Config.get_instance().resource_config.object_image_dir

    def __init__(self, name):
        self.logger = LogHandle('objects').get_logger()
        self._id = ObjectId[str.lower(name)]
        self.image_dir = BasicObject._image_dir + f'{name}/'
        self.name = name
        self.in_storage = 0

        self.service = ServiceHub.get_instance()

        # Config for template matching
        self.matching_service = screen_capture.SCREEN_MATCH_TEMPLATE
        self.imread = cv2.IMREAD_GRAYSCALE
        self.matching_metric = cv2.TM_CCOEFF_NORMED
        self.threshold = 0.8  # Most of the cases are exactly 1:1 matching, the score should be near 1.0
        self.n_sample = 2
        self.restricted_box = None  # Object is only exist in this box

    def look(self, all=False, show=False):
        """
        Take a screen shot and find one object with the highest matching score
        :return: Pixel object contain matched object location, return None if not.
        """
        return self.service.screen_capture.execute(
            self.matching_service,
            imread=self.imread,
            metric=self.matching_metric,
            threshold=self.threshold,
            obj=self,
            return_all=all,
            show=show)

    def find_and_wait(self, wait_time=5):
        """
        find and re-find again if object is not exist after wait_time second(s)
        :param wait_time: to wait between find and re-find, skip re-find if wait_time=0
        :return: find_one return
        """
        found_obj = self.look()
        if found_obj is None and wait_time>0:
            time.sleep(wait_time)
            found_obj = self.look()
        if found_obj is None:
            mes = f'{self.__class__}: {self.name} can not be found!'
            self.logger.info(mes)
            return None

        return found_obj

    def find_and_click(self, wait_time=0, sleep_time=1, loop=False, skip_loop_wait=True, callback=None):
        """
        find_wait_and_raise then click on object

        :param wait_time: time between find and re-find, look at find_wait_and_raise
        :param sleep_time: sleep second after click
        :param loop: Find and click, execute callback loop until all object is gone
        :param skip_loop_wait: skip wait_time when loop
        :param callback: execute callback after click if not None,
        callback must return True for loop to continue and False to stop the loop
        :return: find_one return
        """
        found_obj = self.find_and_wait(wait_time)
        if found_obj is not None:
            found_loc, _, _ = found_obj
            self.service.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=sleep_time)
            if callback is not None:
                res = callback(found_obj)
                if not res: return found_obj

            # only loop when found the first one
            if loop:
                if skip_loop_wait: wait_time = 0
                loop_obj = self.find_and_wait(wait_time)
                while loop_obj is not None:
                    found_loc, _, _ = loop_obj
                    self.service.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=sleep_time)
                    if callback is not None:
                        res = callback(loop_obj)
                        if not res: break

                    loop_obj = self.find_and_wait(wait_time)

        return found_obj
