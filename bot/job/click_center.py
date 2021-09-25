from bot.job.common import AbsJob
from service.hub import *


class ClickCenter(AbsJob):
    def __init__(self, device, service_hub):
        super().__init__('Click center', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self):
        self.touch.execute(ACTION_CLICK, pixel = self.screen.center)