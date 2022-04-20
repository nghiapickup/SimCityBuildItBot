from service.hub import ServiceHub
from utils.log import LogHandle
from job.hub import JobHub


class BasicBot:
    def __init__(self, name):
        self.logger = LogHandle('objects').logger
        self.logger.info(f'{self.__class__}: Start bot {name}')
        self.name = name

        self.service_hub = ServiceHub.get_instance()
        self.job_hub = JobHub.get_instance()

    def run(self):
        pass
