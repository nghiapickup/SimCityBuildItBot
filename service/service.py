from utils.log import LogHandle


class AbsService:
    def __init__(self):
        self.logger = LogHandle('services').logger