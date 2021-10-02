from utils.log import LogHandle


class BasicService:
    def __init__(self):
        self.logger = LogHandle('services').logger