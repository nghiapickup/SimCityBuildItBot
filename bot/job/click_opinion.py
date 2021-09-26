import time

from bot.job.common import AbsJob
from object.buttons import BntAdWatch, BntAdClose, BntAdReward, BntNoThanks
from service import screen_touch
from object.opinions import OpinionBlue, OpinionSimoleon, OPINION


class ClickOpinion(AbsJob):
    """
    Scan the screen and handle opinion
    - Click and close normal opinion
    - Watch ad opinion and collect reward
    - close opinion simoleon
    """
    def __init__(self, device, service_hub):
        super().__init__('Click Opinion', device, service_hub)
        self.screen_touch = service_hub.screen_touch
        self.screen_capture = service_hub.screen_capture
        self.screen = device.screen

    def execute(self):
        opinion = OpinionBlue()
        found_opinion = opinion.find_one()
        while found_opinion is not None:
            opinion_loc, template_id, score = found_opinion
            self.logger.info(f'Found opinion {OPINION[template_id]}:{score}!')
            print(f'Found opinion {OPINION[template_id]}:{score}!')
            self._handle_ad(opinion_loc) if template_id == 1 else self._handle_normal(opinion_loc)
            found_opinion = opinion.find_one()

        simoleon = OpinionSimoleon()
        found_simoleon = simoleon.find_one()
        while found_simoleon is not None:
            opinion_loc, _, score = found_simoleon
            self.logger.info(f'Found opinion simoleon:{score}!')
            print(f'Found opinion simoleon:{score}!')
            self._handle_simoleon(opinion_loc)
            found_simoleon = simoleon.find_one()

    def _handle_normal(self, opinion_loc):
        self.logger.info("Click normal opinion!")
        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc, sleep_in=1)
        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc)

    def _handle_ad(self, opinion_loc):
        self.logger.info("Watch ad opinion!")

        ad_bnt = BntAdWatch()
        ad_bnt.find_and_click(5)
        time.sleep(30) # watch ad

        close_bnt = BntAdClose()
        close_bnt.find_and_click(5)

        # find reward button, if not, raise error
        reward_bnt = BntAdReward()
        reward_loc, _ = reward_bnt.find_and_click(5)
        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=reward_loc, sleep_in=5) # click to close

    def _handle_simoleon(self, opinion_loc):
        self.logger.info("Close simoleon opinion!")
        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc, sleep_in=1)

        no_bnt = BntNoThanks()
        no_bnt.find_and_click()