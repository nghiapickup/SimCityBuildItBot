from service.log import LogHandle


class AbsJob:
    def __repr__(self):
        return self.name

    def __init__(self, name, device, service_hub):
        self.logger = LogHandle('bot_job').get_logger()
        self.name = name
        self.device = device
        self.service_hub = service_hub

    def execute(self, **kwargs):
        pass


