import time

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


class Touch:
    def __init__(self, device):
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

    def execute(self, action_code, **kwargs):
        self.action_map[action_code](**kwargs)

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

    def _wipe(self, from_pixel, to_pixel, n_step=5):
        x_step = (to_pixel.x - from_pixel.x)/n_step
        y_step = (to_pixel.y - from_pixel.y)/n_step

        self.execute(TOUCH_DOWN)
        self.execute(ABS_PRESSURE)

        for i in range (0, n_step):
            self.execute(ABS_AXIS, x=from_pixel.x + x_step*i, y=from_pixel.y +y_step*i)
            self.execute(SENT_SYN)

        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)

    def _click_on(self, pixel):
        self.execute(TOUCH_DOWN)
        self.execute(ABS_PRESSURE)
        self.execute(ABS_AXIS, x=pixel.x, y=pixel.y)
        self.execute(SENT_SYN)
        self.execute(TOUCH_UP)
        self.execute(SENT_SYN)
