import time
from bot.bot import Bot


class ClickOpinionBot(Bot):
    def __init__(self):
        super().__init__('Click Opinion Bot')

    def run(self):
        while True:
            self.job_hub.click_opinion.execute()
            time.sleep(5)
