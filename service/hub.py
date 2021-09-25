from service.screen_touch import *
from service.screen_capture import *
from service.device import Device
from bot.job.change_map_view import ChangeMapView
from bot.job.click_center import ClickCenter
from bot.job.click_storage import ClickStorage


class ServiceHub:
    _instance = None

    @staticmethod
    def get_instance():
        if ServiceHub._instance is None:
            ServiceHub()
        return ServiceHub._instance

    def __init__(self):
        self.device = Device()
        self.screen_touch = Touch(self.device)
        self.screen_capture = Capture(self.device)
        ServiceHub._instance = self


class JobHub:
    def __init__(self, service_hub):
        self.service_hub = service_hub
        self.device = self.service_hub.device

        self.change_map_view = ChangeMapView(self.device, service_hub)
        self.click_center = ClickCenter(self.device, service_hub)
        self.click_storage = ClickStorage(self.device, service_hub)

