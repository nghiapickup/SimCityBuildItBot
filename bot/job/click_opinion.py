import time

from bot.job.common import AbsJob
from object.button import BntFactory
from object.opinion import Opinion, OPINION_TEMPLATE_NAME
from object import opinion, button
from service import screen_touch


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
        opinion = Opinion()
        opinion.find_and_click(loop=True, sleep_time=2, callback=self._handle_opinion)

    def _handle_opinion(self, found_opinion):
        opinion_loc, template_id, score = found_opinion
        self.logger.info(f'Found opinion {OPINION_TEMPLATE_NAME[template_id]}:{score}!')

        if template_id == opinion.OPINION_AD:
            self._handle_ad()
        elif template_id == opinion.OPINION_SIMOLEON1 or template_id == opinion.OPINION_SIMOLEON2:
            self._handle_simoleon()
        else:
            self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc) # close though bubble
        return True

    def _handle_ad(self):
        self.logger.info(f'{self.__class__} Watch ad opinion!')
        is_watched = False
        ad_bnt = BntFactory.get(button.BNT_AD_WATCH)
        if ad_bnt.find_and_click(wait_time=5) is not None:
            time.sleep(25) # watch ad
            close_bnt = BntFactory.get(button.BNT_AD_CLOSE)
            # Close and watch reward box appear!
            if close_bnt.find_and_click(wait_time=5, sleep_time=3) is not None:
                # find reward button
                reward_bnt = BntFactory.get(button.BNT_AD_REWARD)
                # Long sleep after collect reward -> change to opened box
                found_reward = reward_bnt.find_and_click(wait_time=5, sleep_time=7)
                collected_reward_bnt = BntFactory.get(button.BNT_AD_REWARD_COLLECTED)
                found_collected_reward = collected_reward_bnt.find_and_click(5)
                if found_reward is not None and found_collected_reward is not None:
                    is_watched = True

        if not is_watched:
            mes = f'{self.__class__}: cannot finish watching opinion ad!'
            raise ModuleNotFoundError(mes)
        return True

    def _handle_simoleon(self):
        no_bnt = BntFactory.get(button.BNT_NO_THANKS)
        if no_bnt.find_and_click(wait_time=3) is None:
            mes = f'{self.__class__} cannot BntNoThanks to close simoleon opinion!'
            raise ModuleNotFoundError(mes)
        return True
