import cv2
import numpy as np

from object.display import Pixel
from service.service import BasicService

# Event service
SCREEN_SHOT = 1
GET_RECENT_IMAGE = 2
SCREEN_MATCH_TEMPLATE = 3


def img_add_contrast(image, alpha=1.5, beta=50):
    return cv2.addWeighted(image, alpha, np.zeros(image.shape, image.dtype), 0, beta)


class Capture(BasicService):
    def __init__(self, device):
        super().__init__()
        self.device = device
        self.action_map = {
            SCREEN_SHOT: self._screen_shot,
            GET_RECENT_IMAGE: self._get_screen_capture,
            SCREEN_MATCH_TEMPLATE: self._match_item_template
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

    def _try_match_template(self, image, template, metric, threshold, restricted_box):
        matching_result = cv2.matchTemplate(image, template, metric)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(matching_result)

        if metric in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            select_value = 1 - minVal
            select_loc = minLoc
        else:
            select_value = maxVal
            select_loc = maxLoc

        if select_value < threshold:
            self.logger.info(f'{self.__class__}: return None! select_value < threshold '
                             f'({select_value}<{threshold}).')
            return None

        # Check the brightest one is not in the restricted box, if not, it may have matching wrong object
        return_pixel = Pixel(select_loc[0] + template.shape[1] / 2,
                             select_loc[1] + template.shape[0] / 2,
                             convert_to_xy_device=True)
        if not return_pixel.is_in(restricted_box):
            self.logger.info(f'{self.__class__}: return None! selected Pixel{return_pixel} '
                             f'is not in restricted_box {restricted_box}.')
            return None

        self.logger.info(f'{self.__class__}: found match at Pixel{return_pixel}, match value={select_value} ')
        return select_value, matching_result, return_pixel

    def _match_item_template(self, obj, threshold,
                             image=None,
                             imread=cv2.IMREAD_UNCHANGED,
                             metric=cv2.TM_CCOEFF_NORMED,
                             return_all=False,
                             show=False):
        self.logger.info(f'{self.__class__}: Start matching {obj.name}!')

        if image is None:
            image = self._screen_shot(imread=imread)

        all_select_locs = []
        return_pixel, template_id, select_template, select_value, matching_result = None, None, None, 0, None
        for i in range(1, obj.n_sample + 1):
            template = cv2.imread(obj.image_dir + f'{obj.name}{i}.png', imread)
            return_match = self._try_match_template(image, template, metric, threshold, obj.restricted_box)
            if return_match is not None:
                score, match_score, p = return_match
                # Update max matching
                if score > select_value:
                    return_pixel, template_id, select_template, select_value, matching_result = \
                        p, i, template, score, match_score

                # Show all matching
                if show or return_all:
                    # Get all locs are in restricted area
                    locs = np.where(match_score >= threshold)
                    for point in zip(*locs[::-1]):
                        converted_pixel = Pixel(point[0] + template.shape[1]/2,
                                                point[1] + template.shape[0]/2,
                                                convert_to_xy_device=True)
                        if converted_pixel.is_in(obj.restricted_box):
                            # check whether new point is found !
                            min_distance = 100
                            if len(all_select_locs) > 0:
                                min_distance = min(map(lambda p: converted_pixel.distance(p[0]), all_select_locs))
                            if min_distance > 50: # size of minimum box is ~50x50
                                all_select_locs.append([converted_pixel ,
                                                        match_score[point[1], point[0]],
                                                        template])

        if select_value == 0:
            self.logger.info(f'{self.__class__}: return None, none of teamplate matched!')
            return None

        if show:
            self.logger.info(f'{self.__class__}: {len(all_select_locs)} matches! Max_value={select_value}')
            # Draw all rectangle around the matched points.
            for select_locs in all_select_locs:
                px, py = select_locs[0].get_cv_point()
                score = select_locs[1]
                t = select_locs[2]

                # return to origin brightest point, since (px, py) is moved to center before
                px = round(px - t.shape[1]/2)
                py = round(py - t.shape[0]/2)
                cv2.rectangle(image, (px, py), (px + t.shape[1], py + t.shape[0]), (255, 255, 0), 3)
                front_scale = 2
                cv2.putText(image, f'{obj.name}{score}:{round(score, 2)}',
                            (px, py + t.shape[0] + front_scale * 10 + 2),
                            cv2.FONT_HERSHEY_PLAIN, front_scale, (255, 255, 0), 2, cv2.LINE_AA)

            # show the output image
            cv2.imshow(obj.name + ' matching', image)
            cv2.waitKey(0)

        if return_all:
            return all_select_locs
        else:
            return [(return_pixel, template_id, select_value)]
