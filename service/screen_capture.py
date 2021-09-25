import cv2
import numpy as np
from service.config import Config

# Event List
SCREEN_SHOW = 1
SCREEN_X = 2


class Capture:
    def __init__(self, device):
        self.config = Config.get_instance().resource_config

        self.device = device
        self.action_map = {
            SCREEN_SHOW: self._screen_show
        }

    def execute(self, action_code, **kwargs):
        self.action_map[action_code](**kwargs)

    def _screen_show(self, resize=True):
        processOut = self.device.adb_screen_cap()
        image_bytes = processOut.stdout
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        if resize: image = cv2.resize(image, (960, 540))  # Resize image
        cv2.imshow("", image)
        cv2.waitKey(0)
        cv2.destroyWindow("")
