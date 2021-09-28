import time
import cv2

from utils.config import Config
from service.hub import ServiceHub
from service import screen_capture, screen_touch
from utils.log import LogHandle


class ObjectActionReturn:
    def __init__(self, action_return=None, callback_return=None):
        self.action_return = action_return
        self.callback_return = callback_return


class BasicObject:
    _image_dir = Config.get_instance().resource_config.object_image_dir

    def __init__(self, name):
        self.logger = LogHandle('objects').logger
        self.image_dir = BasicObject._image_dir + f'{name}/'
        self.name = name

        self.in_storage = 0
        self.max_quantity = 0

        self.service_hub = ServiceHub.get_instance()

        # Config for template matching
        self.matching_service = screen_capture.SCREEN_MATCH_TEMPLATE
        self.imread = cv2.IMREAD_GRAYSCALE
        self.matching_metric = cv2.TM_CCOEFF_NORMED
        self.threshold = 0.8  # Most of the cases are exactly 1:1 matching, the score should be near 1.0
        self.n_sample = 2
        self.restricted_box = None  # Object is only exist in this box

    def look(self, get_all=False, show=False):
        """
        Take a screen shot and find one object with the highest matching score
        :return: Pixel object contain matched object location, return action None if not.
        """
        look_return = self.service_hub.screen_capture.execute(
            self.matching_service,
            imread=self.imread,
            metric=self.matching_metric,
            threshold=self.threshold,
            obj=self,
            return_all=get_all,
            show=show)

        return ObjectActionReturn(action_return=look_return, callback_return=None)

    def find_and_wait(self, wait_time=5):
        """
        find and re-find again if object is not exist after wait_time second(s)
        :param wait_time: to wait between find and re-find, skip re-find if wait_time=0
        :return: find_one return
        """
        found_action = self.look()
        if found_action.action_return is None and wait_time > 0:
            time.sleep(wait_time)
            found_action = self.look()
        if found_action.action_return is None:
            mes = f'{self.__class__}: {self.name} can not be found!'
            self.logger.info(mes)
            return ObjectActionReturn()

        return ObjectActionReturn(action_return=found_action.action_return, callback_return=None)

    def find_and_click(self, wait_time=0, sleep_time=1,
                       loop=False, skip_loop_wait=True,
                       callback=None, **callback_args):
        """
        find_wait_and_raise then click on object

        :param wait_time: time between find and re-find, look at find_wait_and_raise
        :param sleep_time: sleep second after click
        :param loop: Find and click, execute callback loop until all object is gone
        :param skip_loop_wait: skip wait_time when loop
        :param callback: execute callback after click if not None,
        callback must return True for loop to continue and False to stop the loop
        :return: find_one return
        """
        find_action = self.find_and_wait(wait_time)
        callback_return = False
        if find_action.action_return is not None:
            found_loc, _, _ = find_action.action_return[0]
            self.service_hub.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=sleep_time)
            if callback is not None:
                callback_return = callback(find_action.action_return, **callback_args)
                if not callback_return:
                    return ObjectActionReturn(action_return=find_action.action_return, callback_return=callback_return)

            # only loop when found the first one
            if loop:
                if skip_loop_wait: wait_time = 0
                loop_action = self.find_and_wait(wait_time)
                while loop_action.action_return is not None:
                    found_loc, _, _ = loop_action.action_return[0]
                    self.service_hub.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=sleep_time)
                    if callback is not None:
                        callback_return = callback(loop_action.action_return, **callback_args)
                        if not callback_return: break

                    loop_action = self.find_and_wait(wait_time)

        return ObjectActionReturn(action_return=find_action.action_return, callback_return=callback_return)
