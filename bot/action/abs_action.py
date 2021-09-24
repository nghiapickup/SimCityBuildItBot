import time
from bot.device import Device


class AbsAction:
    def __init__(self, name, device):
        self.name = name
        self.device = device
        assert isinstance(device, Device)

        self.action_map = {}

    def execute(self, action_code, **kwargs):
        pass

    @staticmethod
    def sleep(s):
        time.sleep(s)
