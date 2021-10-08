import time
from bot.basicbot import BasicBot
from object import button
from object.banner_ad import BannerAd
from object.button import BntFactory
from object.popup import OpinionPopup, AdPopup, SimoleonPopup
from service import screen_touch


class ClickOpinionBot(BasicBot):
    def __init__(self):
        super().__init__('Click Opinion Bot')
        self.screen_touch = self.service_hub.screen_touch

        self.opinion = OpinionPopup()
        self.ad_popup = AdPopup()
        self.simoleon = SimoleonPopup()

    def run(self):
        self.job_hub.change_map_view.execute()

        while True:
            self.opinion.find_and_click(loop=True, try_time=0, callback=self._handle_opinion)
            self.simoleon.find_and_click(loop=True, try_time=0, sleep_time=0.5, callback=self._handle_simoleon)
            self.ad_popup.find_and_click(loop=True, try_time=0, sleep_time=0.5, callback=self._handle_ad)
            self.opinion.sleep(3)

    def _handle_opinion(self, found_opinion):
        opinion_loc, score, template = found_opinion[0]
        self.logger.info(f'Found opinion: Score: {score}!')

        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=opinion_loc) # close though bubble
        return True

    def _handle_ad(self, found_opinion):
        self.ad_popup.sleep(0.5)
        opinion_loc, score, template = found_opinion[0]
        self.logger.info(f'Found ad: {score}')

        BannerAd().watch(wait_time=2)

        is_collected = False
        # find reward button
        reward_bnt = BntFactory.make(button.BNT_AD_REWARD)
        if reward_bnt.find_and_click(try_time=2, wait_time=1, sleep_time=5).ok:
            # Long sleep after collect reward -> change to opened box
            collected_reward_bnt = BntFactory.make(button.BNT_AD_REWARD_COLLECTED)
            collected_reward_action = collected_reward_bnt.find_and_click(try_time=2, wait_time=2, sleep_time=1)
            if collected_reward_action.ok:
                is_collected = True

        if not is_collected:
            mes = f'{self.__class__}: cannot finish watching opinion ad!'
            raise ModuleNotFoundError(mes)
        return True

    def _handle_simoleon(self, found_opinion):
        self.simoleon.sleep(0.5)
        opinion_loc, score, template = found_opinion[0]
        self.logger.info(f'Found simoleon: {score}!')

        no_bnt = BntFactory.make(button.BNT_NO_THANKS)
        no_action = no_bnt.find_and_click()
        if not no_action.ok:
            mes = f'{self.__class__}_handle_simoleon: cannot close simoleon opinion!'
            raise ModuleNotFoundError(mes)
        return True
