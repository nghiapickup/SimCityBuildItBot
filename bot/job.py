from device import Device

class AbsJob:
    def __init__(self, name, device):
        self.name = name
        self.device = device
        assert isinstance(device, Device.__class__)
