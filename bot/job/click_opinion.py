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
        opinion.find_and_click(loop=True, callback=self._handle_opinion)

        simoleon = OpinionSimoleon()
        simoleon.find_and_click(loop=True, callback=self._handle_simoleon)

    def _handle_opinion(self, found_opinion):
        opinion_loc, template_id, score = found_opinion
        self.logger.info(f'Found opinion {OPINION[template_id]}:{score}!')

        if template_id == 1:
            self._handle_ad()
        else:
            self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc) # close though bubble

    def _handle_ad(self):
        self.logger.info(f'{self.__class__} Watch ad opinion!')
        is_watched = False
        ad_bnt = BntAdWatch()
        if ad_bnt.find_and_click(5) is not None:
            time.sleep(30) # watch ad
            close_bnt = BntAdClose()
            if close_bnt.find_and_click(5) is not None:
                # find reward button, if not, raise error
                reward_bnt = BntAdReward()
                reward_loc, _ = reward_bnt.find_and_click(5)
                self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=reward_loc, sleep_in=5) # click again to close
                is_watched = True
        if not is_watched:
            mes = f'{self.__class__} cannot watch opinion ad!'
            raise ModuleNotFoundError(mes)
        return True

    def _handle_simoleon(self, found_simoleon):
        opinion_loc, _, score = found_simoleon
        self.logger.info(f'Found opinion simoleon:{score}!')

        no_bnt = BntNoThanks()
        if no_bnt.find_and_click() is None:
            mes = f'{self.__class__} cannot BntNoThanks to close simoleon opinion!'
            raise ModuleNotFoundError(mes)
        return True