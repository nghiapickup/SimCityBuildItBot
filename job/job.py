from service.hub import ServiceHub
from utils.log import LogHandle


class AbsJob:
    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.logger = LogHandle('jobs').logger
        self.name = name

        self.service_hub = ServiceHub.get_instance()
        self.device = self.service_hub.device

    def execute(self, **kwargs):
        pass

