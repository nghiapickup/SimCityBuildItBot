from utils.display import Pixel
from bot.job.common import AbsJob
from bot.hub import *


class ChangeMapView(AbsJob):
    def __init__(self, device, service_hub):
        super().__init__('Change Map View', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self):
        self._change_view()
        self._zoom_out()

    def _change_view(self):
        x_max = self.screen.x_size
        y_max = self.screen.y_size
        x_shift = 0.6 / 2 * x_max
        y_shist = 0.1 * y_max

        top_left = self.screen.center + Pixel(+x_shift, -y_shist)
        top_right = self.screen.center + Pixel(+x_shift, +y_shist)
        bottom_left = self.screen.center + Pixel(-x_shift, -y_shist)

        self.touch.execute(TOUCH_DOWN)
        self.touch.execute(ABS_PRESSURE)

        n_step = 5
        move_step = top_left.diff_range(bottom_left, n_step)
        for i in range(0, n_step):
            self.touch.execute(ABS_AXIS, x=top_left.x + move_step.x * i, y=top_left.y + move_step.y * i)
            self.touch.execute(SENT_MT_SYN)
            self.touch.execute(ABS_AXIS, x=top_right.x + move_step.x * i, y=top_right.y + move_step.y * i)
            self.touch.execute(SENT_SYN)

        self.touch.execute(TOUCH_UP)
        self.touch.execute(SENT_SYN)

    def _zoom_out(self):
        center = self.screen.center
        y_max = self.screen.y_size
        y_shist = 0.5*y_max/2

        left = center + Pixel(0, -y_shist)
        right = center + Pixel(0, +y_shist)

        self.touch.execute(TOUCH_DOWN)
        self.touch.execute(ABS_PRESSURE)

        n_step = 5
        move_step = left.diff_range(center, n_step)
        for i in range(0, n_step):
            self.touch.execute(ABS_AXIS, x=center.x, y=left.y + move_step.y * i)
            self.touch.execute(SENT_MT_SYN)
            self.touch.execute(ABS_AXIS, x=center.x, y=right.y - move_step.y * i)
            self.touch.execute(SENT_SYN)

        self.touch.execute(TOUCH_UP)
        self.touch.execute(SENT_SYN)
