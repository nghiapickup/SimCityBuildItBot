import time
import cv2
import re

from object.display import Pixel
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
    _lag_scale = Config.get_instance().device_config.lag_scale

    def __init__(self, name, category=''):
        self.logger = LogHandle('objects').logger
        if category == '':
            self.image_dir = BasicObject._image_dir + f'{name}/'
        else:
            self.image_dir = BasicObject._image_dir + f'{category}/{name}/'

        self.name = name
        self.location = None
        self.service_hub = ServiceHub.get_instance()
        self.object_location = self.service_hub.object_location
        self.device = self.service_hub.device
        self.screen_touch = self.service_hub.screen_touch
        self.screen_capture = self.service_hub.screen_capture

        # Config for template matching
        self.matching_service = screen_capture.SCREEN_MATCH_TEMPLATE
        self.imread = cv2.IMREAD_GRAYSCALE
        self.matching_metric = cv2.TM_CCOEFF_NORMED
        self.threshold = 0.8  # Most of the cases are exactly 1:1 matching, the score should be near 1.0
        self.n_sample = 2
        self.restricted_box = None  # Object is only exist in this box

    @staticmethod
    def apply_restricted_box(image, box):
        return image[box[0].x:box[1].x, box[0].y:box[1].y]

    @staticmethod
    def show(image):
        cv2.imshow("", image)
        cv2.waitKey(0)
        cv2.destroyWindow("")

    def look(self, image=None, get_all=False, save_loc=False, show=False):
        """
        Take a screen shot and find one object with the highest matching score
        :return: Pixel object contain matched object location, return action None if not.
        """
        look_return = self.service_hub.screen_capture.execute(
            self.matching_service,
            image=image,
            obj=self,
            imread=self.imread,
            metric=self.matching_metric,
            return_all=get_all,
            show=show)

        res = ObjectActionReturn(action_return=look_return, callback_return=None)
        self.logger.info(f'{self.__class__} look for {self.name}: {res.ok}')
        if save_loc and look_return: self.location = look_return[0][0]
        return res

    def look_and_wait(self, image=None, wait_time=1, try_time=1,
                      get_all=False):
        assert try_time >= 0, f'{self.__class__}: try_time >= 0 but {try_time} found!'

        look_action = self.look(image, get_all=get_all)
        while not look_action.ok and try_time:
            try_time -= 1
            if wait_time > 0:
                self.sleep(wait_time)
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
        self.logger.info(f'{self.__class__}: find {self.name} and click, loop={loop}')
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

    def click(self, sleep_in=0, wait_open_window=False):
        self.logger.info(f'{self.__class__}: Click')
        assert self.location, f'{self.__class__}: Location is None!'
        self.service_hub.screen_touch.execute(
            screen_touch.ACTION_CLICK,
            pixel=self.location, sleep_in=sleep_in
        )
        if wait_open_window:
            self.sleep(1)

    def find_all_and_click(self, image=None, wait_time=1,
                           try_time=1, sleep_time=1,
                           callback=None, **callback_args):
        self.logger.info(f'{self.__class__}: find ALL {self.name} and click')
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

    def extract_location_and_text(self, image, find_action_return, text_filter=None, show=False):
        res = []
        for found_result in find_action_return:
            loc, _, template = found_result
            # extract obj bounding box
            image_loc = loc.get_image_point()
            x_range = int(image_loc[0] - template.shape[0] / 2), int(image_loc[0] + template.shape[0] / 2)
            y_range = int(image_loc[1] - template.shape[1] / 2 - 5), int(image_loc[1] + template.shape[1] / 2 + 5)
            obj_image = image[x_range[0]:x_range[1], y_range[0]:y_range[1]]
            if show: self.show(obj_image)
            # get text from obj's box
            text = self.screen_capture.execute(screen_capture.EXTRACT_STRING, image=obj_image)
            if text_filter:
                text = text_filter(text)
            res.append([loc, text])

        return res

    def get_time_from_text(self, text):
        rs = re.findall('([0-9]+)s', text)
        assert len(rs) <= 1, f'There are more than 1 s charater!'
        rm = re.findall('([0-9]+)m', text)
        assert len(rm) <= 1, f'There are more than 1 m charater!'
        rh = re.findall('([0-9]+)h', text)
        assert len(rh) <= 1, f'There are more than 1 h charater!'

        s = 0
        if len(rs) > 0: s = int(rs[0])
        m = 0
        if len(rm) > 0: m = int(rm[0])
        h = 0
        if len(rh) > 0: h = int(rh[0])

        self.logger.info(f'{self.name}: {h}h:{m}m:{s}s')
        return 3600 * h + 60 * m + s

    def sleep(self, second, info=''):
        sleep_by_lag = BasicObject._lag_scale * second
        self.logger.info(f'Sleep {sleep_by_lag}s:{info}')
        time.sleep(second)
