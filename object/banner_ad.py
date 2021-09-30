import time
from object import button
from object.button import BntFactory
from object.object import BasicObject, ObjectActionReturn
from service import screen_capture


class BannerAd(BasicObject):
    def __init__(self):
        super().__init__("banner_ad")
        self.n_sample = 1
        self.threshold = 0.9

        self.screen_capture = self.service_hub.screen_capture
        self.ad_bnt = BntFactory.make(button.BNT_AD_WATCH)

    def watch(self, wait_time=0, callback=None, **callback_args):
        action_return = None
        cb_return = None
        if self.look().ok:
            screen_image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
            click_ad_bnt = self.ad_bnt.find_and_click(image=screen_image, wait_time=wait_time)
            cb_return = None
            if click_ad_bnt.ok:
                self.logger.info(f'{self.__class__}: Start 20s to watch Ad!')
                time.sleep(20)  # watch ad
                close_bnt = BntFactory.make(button.BNT_AD_CLOSE)
                # Close ad video
                close_action = close_bnt.find_and_click(wait_time=3, try_time=3, sleep_time=2)
                if close_action.ok:
                    action_return = close_action.action_return
                    if callback is not None:  # action after close the ad video
                        cb_return = callback(**callback_args)  # return is callback output

        return ObjectActionReturn(action_return=action_return, callback_return=cb_return)
