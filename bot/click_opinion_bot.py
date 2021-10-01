import time
from bot.basicbot import BasicBot


class ClickOpinionBot(BasicBot):
    def __init__(self):
        super().__init__('Click Opinion Bot')

    def run(self):
        while True:
            self.job_hub.click_opinion.execute()
            time.sleep(5)
