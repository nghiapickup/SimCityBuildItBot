import cv2

from service.config import Config
from service.hub import ServiceHub
from service import screen_capture
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
    'bnt_collect': BNT_COLLECT
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
        self.threshold = 0.97
        self.n_sample = 2
        self.restricted_box = None # Object is only exist in this box

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
            item=self,
            show=show)
