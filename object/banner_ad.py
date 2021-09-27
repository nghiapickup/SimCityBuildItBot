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

        if ad_bnt.find_and_click(wait_time=wait_time) is not None:
            self.logger.info(f'{self.__class__}: Start to watch Ad!')
            time.sleep(25)  # watch ad
            close_bnt = BntFactory.make(button.BNT_AD_CLOSE)
            # Close ad video
            if close_bnt.find_and_click(wait_time=5, sleep_time=2) is None:
                return False
            if callback is not None: # action after close the ad video
                return callback(**callback_args) # return is callback output

        return True