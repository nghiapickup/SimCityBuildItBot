from service.log import LogHandle


class AbsService:
    def __init__(self):
        self.logger = LogHandle('service').get_logger()
