import time

from bot.job.common import AbsJob
from object.button import BntFactory
from object.opinion import Opinion, OPINION_TEMPLATE_NAME
from object import opinion, button
from service import screen_touch


class ProduceFactory(AbsJob):
    def __init__(self, device, service_hub):
        super().__init__('Produce factory', device, service_hub)
        self.screen_touch = service_hub.screen_touch
        self.screen_capture = service_hub.screen_capture
        self.screen = device.screen

    def execute(self, item):
        bnt_collect = BntFactory.get(button.BNT_COLLECT)
        bnt_empty = BntFactory.get(button.BNT_EMPTY)

        # Collect all finished item first
        # find collect button (no re-find if is not) and click all (no wait after click)
        bnt_collect.find_and_click(wait_time=0, sleep_time=0, loop=True)

        # drag metal to empty slot
        produced_item = False
        found_empty = bnt_empty.look()

        while found_empty is not None:
            found_item = item.look()
            if found_item is None:
                mes = f'{self.__class__} cannot find {item.name}!'
                raise ModuleNotFoundError(mes)

            empty_loc, _, _ = found_empty
            item_loc, _, _ = found_item
            self.screen_touch.execute(
                screen_touch.ACTION_WIPE,
                pixel_path=[item_loc, empty_loc],
                n_step=5,
                hold=0
            )
            found_empty = bnt_empty.look()
            produced_item = True

        return produced_item