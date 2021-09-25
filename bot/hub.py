from service.screen_touch import *
from service.screen_capture import *
from bot.job.change_map_view import ChangeMapView
from bot.job.click_center import ClickCenter
from bot.job.click_storage import ClickStorage


def sleep(s):
    time.sleep(s)


class ServiceHub:
    def __init__(self, device):
        self.device = device
        self.screen_touch = Touch(device)
        self.screen_capture = Capture(device)


class JobHub:
    def __init__(self, device, service_hub):
        self.device = device
        self.service_hub = service_hub

        self.sleep = sleep
        self.change_map_view = ChangeMapView(device, service_hub)
        self.click_center = ClickCenter(device, service_hub)
        self.click_storage = ClickStorage(device, service_hub)

