import time

from object.display import Pixel
from service.service import BasicService

# Event list
TOUCH_DOWN = 1
TOUCH_UP = 2
ABS_AXIS = 3
SENT_SYN = 4
SENT_MT_SYN = 5
ABS_PRESSURE = 6

ACTION_WIPE = 7
ACTION_CLICK=8
ACTION_CLICK_CENTER=9
ACTION_WIPE_CENTER=10
ACTION_WIPE_TO_CENTER=11


class EV_KEY:
    type = 1
    BTN_TOUCH = 330


class EV_ABS:
    type = 3
    ABS_MT_PRESSURE = 58
    ABS_MT_POSITION_X = 53
    ABS_MT_POSITION_Y = 54


class EV_SYN:
    type = 0
    SYN_MT_REPORT = 2
    SYN_REPORT = 0


class Touch(BasicService):
    def __init__(self, device):
        super().__init__()

        self.device = device
        self.screen = self.device.screen

        self.action_map = {
            TOUCH_DOWN: self._touch_down,
            TOUCH_UP: self._touch_up,
            ABS_AXIS: self._set_axis,
            SENT_SYN: self._send_syn,
            SENT_MT_SYN: self._send_mt_syn,
            ABS_PRESSURE: self._set_pressure,

            ACTION_WIPE: self._wipe,
            ACTION_CLICK: self._click_on,
            ACTION_CLICK_CENTER: self._click_center,
            ACTION_WIPE_CENTER: self._wipe_center,
            ACTION_WIPE_TO_CENTER: self._wipe_to_center
        }

    def execute(self, action_code, sleep_in=0, **kwargs):
        self.action_map[action_code](**kwargs)
        if sleep_in:
            self.logger.info(f'{self.__class__}: sleep_in={sleep_in} seconds')
            time.sleep(sleep_in)

    def _touch_down(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 1)]
        self.device.abd_sendevents(events)

    def _touch_up(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 0)]
        self.device.abd_sendevents(events)

    def _set_pressure(self):
        events = [(EV_ABS.type, EV_ABS.ABS_MT_PRESSURE, 2)]
        self.device.abd_sendevents(events)

    def _set_axis(self, x, y):
        events = [(EV_ABS.type, EV_ABS.ABS_MT_POSITION_X, x),
                  (EV_ABS.type, EV_ABS.ABS_MT_POSITION_Y, y)]
        self.device.abd_sendevents(events)

    def _send_syn(self):
        events = [(EV_SYN.type, EV_SYN.SYN_MT_REPORT, 0),
                  (EV_SYN.type, EV_SYN.SYN_REPORT, 0)]
        self.device.abd_sendevents(events)

    def _send_mt_syn(self):
        events = [(EV_SYN.type, EV_SYN.SYN_MT_REPORT, 0)]
        self.device.abd_sendevents(events)

    def _wipe(self, pixel_path, n_step=10, hold=0):
        """
        Wipe follow a list of pixels.
        The wipe will click on the first pixel and release at the final path.

        :param pixel_path: list of pixel to follow
        :param n_step: step between 2 moving pixel
        :param hold: sleep hold second(s) after touch down at the first pixel
        :return:
        """
        self.logger.info(f'{self.__class__}:_wipe')
        for p in range(0, len(pixel_path) - 1):
            from_pixel = pixel_path[p]
            to_pixel = pixel_path[p+1]

            x_step = (to_pixel.x - from_pixel.x)/n_step
            y_step = (to_pixel.y - from_pixel.y)/n_step

            self.execute(TOUCH_DOWN)
            self.execute(ABS_PRESSURE)
            time.sleep(hold)

            for i in range (0, n_step+1):
                self.execute(ABS_AXIS, x=from_pixel.x + x_step*i, y=from_pixel.y +y_step*i)
                self.execute(SENT_SYN)

        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)

    def _click_on(self, pixel, hold=0):
        self.logger.info(f'{self.__class__}:_click_on Pixel{pixel}')
        self.execute(TOUCH_DOWN)
        self.execute(ABS_PRESSURE)
        self.execute(ABS_AXIS, x=pixel.x, y=pixel.y)
        self.execute(SENT_SYN)
        time.sleep(hold)
        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)

    def _click_center(self, shift_pixel=None, hold=0):
        self.logger.info(f'{self.__class__}:_click_center')
        click_loc = self.screen.center
        if shift_pixel is not None:
            click_loc = click_loc + shift_pixel

        self._click_on(pixel=click_loc, hold=hold)

    def _wipe_center(self, n_step=3, wipe_length=0.25, hold=1):
        self.logger.info(f'{self.__class__}:_wipe_center')
        start = self.screen.center
        end = start + Pixel(0, -self.screen.y_size * wipe_length)
        self._wipe(pixel_path=[start, end], n_step=n_step, hold=hold)

    def _wipe_to_center(self, from_pixel, n_step=3, hold=1):
        self.logger.info(f'{self.__class__}:_wipe_to_center')
        end = self.screen.center
        start = from_pixel
        self._wipe(pixel_path=[start, end], n_step=n_step, hold=hold)