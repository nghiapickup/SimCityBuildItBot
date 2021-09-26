import time
from bot.bot import Bot


class ClickOpinionBot(Bot):
    def __init__(self):
        super().__init__('Click Opinion Bot')

    def run(self):
        # Change View
        # self.job_hub.change_map_view.execute()

        while True:
            self.job_hub.click_opinion.execute()
            time.sleep(5)
