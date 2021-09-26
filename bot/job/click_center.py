from bot.job.common import AbsJob
from service.hub import *


class ClickCenter(AbsJob):
    def __init__(self, device, service_hub):
        super().__init__('Click center', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self, shift_pixel=None):
        click_loc = self.screen.center
        if shift_pixel is not None:
            click_loc = click_loc + shift_pixel

        self.touch.execute(ACTION_CLICK, pixel = click_loc)