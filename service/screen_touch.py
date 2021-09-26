import time
from service.service import AbsService

# Event list
TOUCH_DOWN = 1
TOUCH_UP = 2
ABS_AXIS = 3
SENT_SYN = 4
SENT_MT_SYN = 5
ABS_PRESSURE = 6

ACTION_WIPE = 7
ACTION_CLICK=8


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


class Touch(AbsService):
    def __init__(self, device):
        super().__init__()

        self.device = device

        self.action_map = {
            TOUCH_DOWN: self._touch_down,
            TOUCH_UP: self._touch_up,
            ABS_AXIS: self._set_axis,
            SENT_SYN: self._send_syn,
            SENT_MT_SYN: self._send_mt_syn,
            ABS_PRESSURE: self._set_pressure,

            ACTION_WIPE: self._wipe,
            ACTION_CLICK: self._click_on
        }

    def execute(self, action_code, sleep_in=None, **kwargs):
        self.action_map[action_code](**kwargs)
        if sleep_in is not None: time.sleep(sleep_in)

    def _touch_down(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 1)]
        self.device.abd_sendevents(events)

    def _touch_up(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 0)]
        self.device.abd_sendevents(events)

    def _set_pressure(self):
        events = [(EV_ABS.type, EV_ABS.ABS_MT_PRESSURE, 1)]
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
        for p in range(0, len(pixel_path) - 1):
            from_pixel = pixel_path[p]
            to_pixel = pixel_path[p+1]

            x_step = (to_pixel.x - from_pixel.x)/n_step
            y_step = (to_pixel.y - from_pixel.y)/n_step

            self.execute(TOUCH_DOWN)
            self.execute(ABS_PRESSURE)
            time.sleep(hold)

            for i in range (0, n_step):
                self.execute(ABS_AXIS, x=from_pixel.x + x_step*i, y=from_pixel.y +y_step*i)
                self.execute(SENT_SYN)

        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)

    def _click_on(self, pixel, hold=0):
        self.execute(TOUCH_DOWN)
        self.execute(ABS_PRESSURE)
        self.execute(ABS_AXIS, x=pixel.x, y=pixel.y)
        self.execute(SENT_SYN)
        time.sleep(hold)
        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)
