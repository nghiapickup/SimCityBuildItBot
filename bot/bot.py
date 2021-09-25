from device import Device


class bot:
    def __init__(self, name):
        self.name = name
        self.device = Device(name)
        self.scheduled_job = []

    def run(self):
        pass