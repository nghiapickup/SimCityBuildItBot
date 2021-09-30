import time
import cv2

from utils.config import Config
from service.hub import ServiceHub
from service import screen_capture, screen_touch
from utils.log import LogHandle


class ObjectActionReturn:
    def __init__(self, action_return=None, callback_return=None):
        self.ok = action_return is not None
        self.action_return = action_return
        self.callback_return = callback_return


class BasicObject:
    _image_dir = Config.get_instance().resource_config.object_image_dir

    def __init__(self, name):
        self.logger = LogHandle('objects').logger
        self.image_dir = BasicObject._image_dir + f'{name}/'
        self.name = name

        self.location = None
        self.service_hub = ServiceHub.get_instance()

        # Config for template matching
        self.matching_service = screen_capture.SCREEN_MATCH_TEMPLATE
        self.imread = cv2.IMREAD_GRAYSCALE
        self.matching_metric = cv2.TM_CCOEFF_NORMED
        self.threshold = 0.8  # Most of the cases are exactly 1:1 matching, the score should be near 1.0
        self.n_sample = 2
        self.restricted_box = None  # Object is only exist in this box

    def look(self, image=None, get_all=False, save_loc=False, show=False):
        """
        Take a screen shot and find one object with the highest matching score
        :return: Pixel object contain matched object location, return action None if not.
        """
        look_return = self.service_hub.screen_capture.execute(
            self.matching_service,
            image=image,
            imread=self.imread,
            metric=self.matching_metric,
            threshold=self.threshold,
            obj=self,
            return_all=get_all,
            show=show)

        if save_loc and look_return: self.location = look_return[0][0]
        return ObjectActionReturn(action_return=look_return, callback_return=None)

    def look_and_wait(self, image=None, wait_time=1, try_time=1,
                      get_all=False):
        assert try_time >= 0, f'{self.__class__}: try_time >= 0 but {try_time} found!'

        look_action = self.look(image, get_all=get_all)
        while not look_action.ok and try_time:
            try_time -= 1
            if wait_time > 0:
                time.sleep(wait_time)
            look_action = self.look(image, get_all=get_all)

        if not look_action.ok:
            self.logger.info(f'{self.__class__}:look_and_wait: {self.name} cannot be found')
            return ObjectActionReturn()

        self.logger.info(f'{self.__class__}: {self.name} is found')
        return ObjectActionReturn(action_return=look_action.action_return, callback_return=None)

    def find_and_click(self, image=None, wait_time=1,
                       try_time=1, sleep_time=1,
                       loop=False, skip_loop_wait=True,
                       callback=None, **callback_args):
        find_action = self.look_and_wait(image, wait_time, try_time)
        callback_return = None
        if find_action.ok:
            found_loc, _, _ = find_action.action_return[0]
            self.service_hub.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc, sleep_in=sleep_time)
            if callback:
                callback_return = callback(find_action.action_return, **callback_args)
                if not callback_return:
                    return ObjectActionReturn(find_action.action_return, callback_return)

            # only loop when found the first one
            if loop:
                if skip_loop_wait: wait_time = 0
                loop_action = self.look_and_wait(image, wait_time)
                while loop_action.ok:
                    found_loc, _, _ = loop_action.action_return[0]
                    self.service_hub.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found_loc,
                                                          sleep_in=sleep_time)
                    if callback:
                        callback_return = callback(loop_action.action_return, **callback_args)
                        if not callback_return: break

                    loop_action = self.look_and_wait(image, wait_time)

        return ObjectActionReturn(find_action.action_return, callback_return)

    def click(self, sleep_in=0):
        self.logger.info(f'{self.__class__}: Click')
        assert self.location, f'{self.__class__}: Location is None!'
        self.service_hub.screen_touch.execute(
            screen_touch.ACTION_CLICK,
            pixel=self.location, sleep_in=sleep_in
        )

    def find_all_and_click(self, image=None, wait_time=1,
                           try_time=1, sleep_time=1,
                           callback=None, **callback_args):
        callback_return = None
        found_all = self.look_and_wait(
            image=image,
            wait_time=wait_time,
            try_time=try_time,
            get_all=True)

        if found_all.action_return:
            for found in found_all.action_return:
                self.service_hub.screen_touch.execute(
                    screen_touch.ACTION_CLICK,
                    pixel=found[0], sleep_in=sleep_time)
                if callback is not None:
                    callback_return = callback(found, **callback_args)
                    if not callback_return:
                        callback_return = callback(found, **callback_args)
                        if not callback_return:
                            break

        return ObjectActionReturn(found_all.action_return, callback_return)
