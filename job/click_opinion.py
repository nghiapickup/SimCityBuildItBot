import time

from job.job import AbsJob
from object.banner_ad import BannerAd
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
    def __init__(self):
        super().__init__('Click Opinion')
        self.screen_touch = self.service_hub.screen_touch

    def execute(self):
        opinion = Opinion()
        opinion.find_and_click(loop=True, sleep_time=1, callback=self._handle_opinion)

    def _handle_opinion(self, found_opinion):
        opinion_loc, template_id, score = found_opinion[0]
        self.logger.info(f'Found opinion {OPINION_TEMPLATE_NAME[template_id]}:{score}!')

        if template_id == opinion.OPINION_AD:
            BannerAd().watch(wait_time=3, callback=self._collect_ad_reward)
        elif template_id == opinion.OPINION_SIMOLEON1 or template_id == opinion.OPINION_SIMOLEON2:
            self._handle_simoleon()
        else:
            self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc) # close though bubble
        return True

    def _collect_ad_reward(self):
        is_collected = False
        # find reward button
        reward_bnt = BntFactory.make(button.BNT_AD_REWARD)
        if reward_bnt.find_and_click(try_time=3, wait_time=2, sleep_time=5).ok:
            # Long sleep after collect reward -> change to opened box
            collected_reward_bnt = BntFactory.make(button.BNT_AD_REWARD_COLLECTED)
            collected_reward_action = collected_reward_bnt.find_and_click(try_time=3, wait_time=3, sleep_time=1)
            if collected_reward_action.ok:
                is_collected = True

        if not is_collected:
            mes = f'{self.__class__}: cannot finish watching opinion ad!'
            raise ModuleNotFoundError(mes)
        return True

    def _handle_simoleon(self):
        no_bnt = BntFactory.make(button.BNT_NO_THANKS)
        no_action = no_bnt.find_and_click(wait_time=3)
        if not no_action.ok:
            mes = f'{self.__class__}_handle_simoleon: cannot close simoleon opinion!'
            raise ModuleNotFoundError(mes)
        return True
