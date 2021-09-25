from bot.job.common import AbsJob
from service.hub import *


class ClickStorage(AbsJob):
    def __init__(self, device, service_hub):
        super().__init__('Click City Storage', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self):
        city_storage = Pixel(817,54)
        self.touch.execute(ACTION_CLICK, pixel=city_storage)