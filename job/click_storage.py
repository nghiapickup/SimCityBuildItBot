from job.job import AbsJob
from service.hub import *


class ClickStorage(AbsJob):
    def __init__(self):
        super().__init__('Click City Storage')
        self.touch = self.service_hub.screen_touch

    def execute(self):
        city_storage = Pixel(817,54)
        self.touch.execute(ACTION_CLICK, pixel=city_storage)