import cv2
import numpy as np
import pytesseract

from object.display import Pixel
from service.service import BasicService

# Event service
SCREEN_SHOT = 1
GET_RECENT_IMAGE = 2
SCREEN_MATCH_TEMPLATE = 3
EXTRACT_STRING = 4


def img_add_contrast(image, alpha=1.5, beta=50):
    return cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)


class Capture(BasicService):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.action_map = {
            SCREEN_SHOT: self._screen_shot,
            GET_RECENT_IMAGE: self._get_screen_capture,
            SCREEN_MATCH_TEMPLATE: self._match_item_template,
            EXTRACT_STRING: self._extract_string
        }

        self.recent_screen = None

    def execute(self, action_code, **kwargs):
        return self.action_map[action_code](**kwargs)

    def _screen_shot(self, imread=cv2.IMREAD_UNCHANGED, resize=False, show=False, save_file=None):
        self.logger.info(f'{self.__class__}:_screen_shot: ({imread} {save_file})')
        image_bytes = self.device.adb_screen_cap()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), imread)
        self.recent_screen = image

        if save_file is not None:
            cv2.imwrite(save_file, image)
        if resize:
            image = cv2.resize(image, (image.shape[0] / 2, image.shape[1] / 2))  # Resize image
        if show:
            cv2.imshow("", image)
            cv2.waitKey(0)
            cv2.destroyWindow("")
        return image

    def _get_screen_capture(self):
        return self.recent_screen

    def _try_match_template(self, image, template, metric, threshold):
        matching_matrix = cv2.matchTemplate(image, template, metric)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(matching_matrix)

        if metric in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            max_value = 1 - minVal
            select_loc = minLoc
        else:
            max_value = maxVal
            select_loc = maxLoc

        if max_value < threshold:
            self.logger.info(f'{self.__class__}: return None! select_value < threshold '
                             f'({max_value}<{threshold}).')
            return None

        # Check the brightest one is not in the restricted box, if not, it may have matching wrong object
        max_match_pixel = Pixel(select_loc[0] + template.shape[1] / 2,
                                select_loc[1] + template.shape[0] / 2,
                                convert_to_xy_device=True,
                                image_shape=image.shape)

        self.logger.info(f'{self.__class__}: found match at Pixel{max_match_pixel}, max value={max_value} ')
        return max_value, max_match_pixel, matching_matrix

    def _match_item_template(self, obj,
                             image=None,
                             imread=cv2.IMREAD_GRAYSCALE,
                             metric=cv2.TM_CCOEFF_NORMED,
                             return_all=False,
                             show=False):
        self.logger.info(f'{self.__class__}: Start matching {obj.name}!')

        if image is None:
            image = self._screen_shot(imread=imread)

        all_select_locs = []
        return_pixel, select_template, select_value, matching_result = None, None, 0, None
        for i in range(1, obj.n_sample + 1):
            template = cv2.imread(obj.image_dir + f'{obj.name}{i}.png', imread)
            return_match = self._try_match_template(image, template, metric, obj.threshold)
            if return_match is not None:
                max_value, max_pixel, match_matrix = return_match
                # Update max matching
                if max_value > select_value:
                    return_pixel, select_template, select_value, matching_result = \
                        max_pixel, template, max_value, match_matrix

                # Show all matching
                if show or return_all:
                    # Get all locs are in restricted area
                    locs = np.where(match_matrix >= obj.threshold)
                    for point in zip(*locs[::-1]):
                        converted_pixel = Pixel(point[0] + template.shape[1]/2,
                                                point[1] + template.shape[0]/2,
                                                convert_to_xy_device=True,
                                                image_shape=image.shape)
                        if converted_pixel.is_in(obj.restricted_box):
                            # check whether new point overlapped with previous template!
                            min_distance = 100
                            if len(all_select_locs) > 0:
                                min_distance = min(map(lambda p: converted_pixel.distance(p[0]), all_select_locs))
                            if min_distance > 50: # size of minimum box is ~50x50
                                all_select_locs.append([converted_pixel ,
                                                        match_matrix[point[1], point[0]],
                                                        template])

        if select_value == 0:
            self.logger.info(f'{self.__class__}: return None, none of teamplate matched!')
            return None

        if show:
            self.logger.info(f'{self.__class__}: {len(all_select_locs)} matches! Max_value={select_value}')
            show_image = image.copy()
            # Draw all rectangle around the matched points.
            for select_locs in all_select_locs:
                px, py = select_locs[0].get_cv_point()
                max_value = select_locs[1]
                t = select_locs[2]

                # return to origin brightest point, since (px, py) is moved to center before
                px = round(px - t.shape[1]/2)
                py = round(py - t.shape[0]/2)
                cv2.rectangle(show_image, (px, py), (px + t.shape[1], py + t.shape[0]), (255, 255, 0), 3)
                front_scale = 2
                cv2.putText(show_image, f'{obj.name}{max_value}:{round(max_value, 2)}',
                            (px, py + t.shape[0] + front_scale * 10 + 2),
                            cv2.FONT_HERSHEY_PLAIN, front_scale, (255, 255, 0), 2, cv2.LINE_AA)

            # show the output image
            cv2.imshow(obj.name + ' matching', show_image)
            cv2.waitKey(0)

        if return_all:
            return all_select_locs
        else:
            return [(return_pixel, select_value, select_template)]

    def _extract_string(self, image):
        config = '-l eng --oem 1 --psm 7'
        return pytesseract.image_to_string(image, config=config)
