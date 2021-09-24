from bot.action.abs_action import AbsAction

# Action list
TOUCH_DOWN = 1
TOUCH_UP = 2
ABS_AXIS = 3
SENT_SYN = 4


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


class Touch(AbsAction):
    def __init__(self, device):
        super().__init__("Click on (x, y)", device)
        self.action_map = {
            TOUCH_DOWN: self._touch_down,
            TOUCH_UP: self._touch_up,
            ABS_AXIS: self._set_axis,
            SENT_SYN: self._send_syn
        }

    def execute(self, action_code, **kwargs):
        self.action_map[action_code](**kwargs)

    def _touch_down(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 1)]
        self.device.abd_sendevents(events)

    def _touch_up(self):
        events = [(EV_KEY.type, EV_KEY.BTN_TOUCH, 0)]
        self.device.abd_sendevents(events)

    def _set_axis(self, x, y):
        events = [(EV_ABS.type, EV_ABS.ABS_MT_PRESSURE, 1),
                  (EV_ABS.type, EV_ABS.ABS_MT_POSITION_X, x),
                  (EV_ABS.type, EV_ABS.ABS_MT_POSITION_Y, y)]
        self.device.abd_sendevents(events)

    def _send_syn(self):
        events = [(EV_SYN.type, EV_SYN.SYN_MT_REPORT, 0),
                  (EV_SYN.type, EV_SYN.SYN_REPORT, 0)]
        self.device.abd_sendevents(events)