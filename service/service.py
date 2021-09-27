from service.log import LogHandle


class AbsService:
    def __init__(self):
        log = LogHandle('service')
        self.logger = log.get_logger()