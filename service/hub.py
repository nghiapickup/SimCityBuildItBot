from service.object_location import Location
from service.screen_touch import *
from service.screen_capture import *
from service.device import Device


class ServiceHub:
    _instance = None

    @staticmethod
    def get_instance():
        if ServiceHub._instance is None:
            ServiceHub()
        return ServiceHub._instance

    def __init__(self):
        self.device = Device()
        self.object_location = Location()
        self.screen_touch = Touch(self.device)
        self.screen_capture = Capture(self.device)

        ServiceHub._instance = self
