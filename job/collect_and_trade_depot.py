import time

from job.job import AbsJob
from object.button import BntTradeDone, BntTradeNew, BntCloseBlue, BntTradePlus, BntTradePut
from service import screen_touch


class CollectAndTradeDepot(AbsJob):
    def __init__(self):
        """
        This is intended that trade pot is already open
        (need to sleep after click trade pot before)
        and close depot when job is done
        :param device:
        :param service_hub:
        """
        super().__init__('Collect and trade depot')
        self.screen_touch = self.service_hub.screen_touch

