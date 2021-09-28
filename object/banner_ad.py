import time
from object import button
from object.button import BntFactory
from object.object import BasicObject


class BannerAd(BasicObject):
    def __init__(self):
        super().__init__("banner_ad")
        self.n_sample = 1
        self.threshold = 0.9

    def watch(self, wait_time=0, callback=None, **callback_args):
        # find ad buttion and watch
        ad_bnt = BntFactory.make(button.BNT_AD_WATCH)

        ad_action = ad_bnt.find_and_click(wait_time=wait_time)
        if ad_action.action_return is not None:
            self.logger.info(f'{self.__class__}: Start to watch Ad!')
            time.sleep(25)  # watch ad
            close_bnt = BntFactory.make(button.BNT_AD_CLOSE)
            # Close ad video
            close_action = close_bnt.find_and_click(wait_time=5, sleep_time=2)
            if close_action.action_return is None:
                return False
            if callback is not None: # action after close the ad video
                return callback(**callback_args) # return is callback output

        return True