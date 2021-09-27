from service.hub import ServiceHub
from utils.log import LogHandle
from job.hub import JobHub


class Bot:
    def __init__(self, name):
        """
        A bot performs a single or combination of tasks, independent to each others,
        and a game can have multiple bots running at the same time.
        It is easier to have single action bot like this,
        .i.e, click opinion bot, run factory bot, trade bot,
        then we don't worry about the logic of combination of many task
        (which is the first, which should perform after another, ...),
        and try to test new bot when the others are running.

        At each time, only one bot can handle the game (device and action),
        a bot must complete it's task and release the device for other bots.
        :param name:
        """
        self.logger = LogHandle('bot').logger
        self.name = name

        self.service_hub = ServiceHub.get_instance()
        self.job_hub = JobHub.get_instance()

    def run(self):
        pass
