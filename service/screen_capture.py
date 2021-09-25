import cv2
import numpy as np
from service.config import Config
from service.log import LogHandle

from object.display import Pixel
from service.service import AbsService

# Event service
SCREEN_SHOW = 1
SCREEN_MATCH_TEMPLATE = 3


def img_add_contrast(image, alpha=1.5, beta=50):
    return cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)


class Capture(AbsService):
    def __init__(self, device):
        super().__init__()

        self.device = device

        self.action_map = {
            SCREEN_SHOW: self._screen_show,
            SCREEN_MATCH_TEMPLATE: self._match_item_template
        }

    def execute(self, action_code, **kwargs):
        return self.action_map[action_code](**kwargs)

    def _screen_show(self, resize=True):
        processOut = self.device.adb_screen_cap()
        image_bytes = processOut.stdout
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        print(image.shape)
        if resize: image = cv2.resize(image, (960, 540))  # Resize image
        cv2.imshow("", image)
        cv2.waitKey(0)
        cv2.destroyWindow("")

    def _try_match_template(self, image, template, metric, threshold, restricted_box):
        matching_result = cv2.matchTemplate(image, template, metric)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(matching_result)

        if metric in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            select_value = 1-minVal
            select_loc = minLoc
        else:
            select_value = maxVal
            select_loc = maxLoc

        if select_value < threshold:
            self.logger.info(f'_try_match_template return None! select_value < threshold '
                             f'({select_value}<{threshold}).')
            return None

        # If the brightest one is not in the restricted box, return None, it may have mismatch matching
        res = Pixel(select_loc[0] + template.shape[0] / 2,
                    select_loc[1] + template.shape[1] / 2,
                    convert_to_xy_device=True)
        if not res.is_in(restricted_box):
            self.logger.info(f'_try_match_template return None! selected Pixel{res} '
                             f'is not in restricted_box {restricted_box}.')
            return None

        return select_value, matching_result, res

    def _match_item_template(self, item, threshold=0.9,
                             imread=cv2.IMREAD_UNCHANGED,
                             metric=cv2.TM_CCOEFF_NORMED,
                             n_sample=2, show=False):
        self.logger.info(f'_match_item_template Start matching {item.name}!')

        processOut = self.device.adb_screen_cap()
        image_bytes = processOut.stdout
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), imread)
        image = img_add_contrast(image)

        all_select_locs = []
        select_value, matching_result, return_pixel, select_template = 0, None, None, None
        for i in range(1, n_sample+1):
            template = cv2.imread(item.image_dir + f'{item.name}{i}.png', imread)
            template = img_add_contrast(template)
            res = self._try_match_template(image, template, metric, threshold, item.restricted_box)
            if res is not None:
                value, result, p = res
                if value > select_value:
                    select_value, matching_result, return_pixel, select_template = value, result, p, template
                    self.logger.info(f'_match_item_template update: select template {i}, select_value={select_value}')

                    if show:
                        # Get all locs are in restricted area
                        select_locs = []
                        locs = np.where(abs(matching_result - select_value) < 0.00001)
                        for point in zip(*locs[::-1]):
                            converted_pixel = Pixel.from_cv_point(point)
                            if converted_pixel.is_in(item.restricted_box):
                                select_locs.append(point)
                        all_select_locs.append([template, select_locs])

        if select_value == 0:
            self.logger.info('_match_item_template return None, none of templates match!')
            return None

        if show:
            self.logger.info(f'_match_item_template found {len(all_select_locs)} matches! Max_value={select_value}')

            # Draw all rectangle around the matched points.
            for select_locs in all_select_locs:
                template = select_locs[0]
                for point in select_locs[1]:
                    cv2.rectangle(image, point,
                                  (point[0] + template.shape[1], point[1] + template.shape[0]),
                                  (0, 255, 255), 3)

            # show the output image
            cv2.imshow(item.name + ' matching', image)
            cv2.waitKey(0)

        return return_pixel
