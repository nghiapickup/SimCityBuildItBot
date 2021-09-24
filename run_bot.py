from utils.config import Config
from bot.device import Device
from bot.action.screen_touch import Touch
from bot.action.screen_touch import *
import sys
if __name__ == '__main__':
    new_device = Device()

    touch = Touch(new_device)
    touch.execute(TOUCH_DOWN)
    touch.execute(ABS_AXIS, x=65, y=1838)
    touch.execute(SENT_SYN)
    touch.execute(TOUCH_UP)
    touch.execute(SENT_SYN)

    # new_device.abd_sendevents([(1, 330, 1), (3, 58, 1), (3, 53, 71), (3, 54, 1740), (0, 2, 0), (0, 0, 0)])
    # new_device.abd_sendevents([(3, 53, 1048), (3, 54, 92), (0, 2, 0), (0, 0, 0), (1, 330, 0), (0, 2, 0), (0, 0, 0)])
    # click_event.execute(571,811)
