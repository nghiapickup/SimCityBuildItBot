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

    def find_one(self, show=False):
        """
        Take a screen shot and find one object
        :return: Pixel object contain matched object location, return None if not.
        """
        return self.service.screen_capture.execute(
            self.matching_service,
            imread=self.imread,
            metric=self.matching_metric,
            threshold=self.threshold,
            n_sample=self.n_sample,
            obj=self,
            show=show)

    def find_wait_and_raise(self, wait_time=5):
        """
        find and re-find again if object is not exist after wait_time
        and raise exception if cannot re-find failed.
        :param wait_time: to between find and re-find
        :return:
        """
        found_obj = self.find_one()
        if found_obj is None:
            time.sleep(wait_time)
            found_obj = self.find_one()
        if found_obj is None:
            mes = f'{self.name} can not be found!'
            raise ModuleNotFoundError(mes)
        return found_obj

    def find_and_click(self, wait_time=5):
        """
        find_wait_and_raise then click on object
        :param wait_time: time between find and re-find, look at find_wait_and_raise
        :return:
        """
        found_obj = self.find_wait_and_raise(wait_time)
        found_loc, _, _ = found_obj
        self.service.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=1)

        return found_obj
