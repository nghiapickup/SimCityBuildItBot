from device import Device


class AbsAction:
    def __init__(self, name, device):
        self.name = name
        self.device = device
        assert isinstance(device, Device.__class__)