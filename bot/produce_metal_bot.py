import time
from bot.bot import Bot
from object.buttons import BntCollect, BntEmpty, BntCloseBlue
from object.display import Pixel
from object.items import Metal
from service import screen_touch


class ProduceMetalBot(Bot):
    def __init__(self):
        super().__init__('Produce and sale metal')
        self.touch_service = self.service_hub.screen_touch

    def run(self):
        self.job_hub.change_map_view.execute()


        metal = Metal()
        bnt_collect = BntCollect()
        bnt_empty = BntEmpty()
        bnt_close = BntCloseBlue()

        # process always start and end at factory
        while True:
            # open factory
            self.job_hub.click_center.execute()

            # Collect all item first
            bnt_collect.find_and_click(wait_time=2, loop=True)

            # drag metal to empty slot
            produce_metal = False
            found_empty = bnt_empty.look()
            while found_empty is not None:
                found_metal = metal.look()
                if found_metal is None:
                    mes = f'{self.__class__} cannot find metal item!'
                    raise ModuleNotFoundError(mes)

                empty_loc, _, _ = found_empty
                metal_loc, _, _ = found_metal
                self.touch_service.execute(
                    screen_touch.ACTION_WIPE,
                    pixel_path=[metal_loc, empty_loc],
                    n_step=10,
                    hold=1
                )
                found_empty = bnt_empty.look()
                produce_metal = True

            if produce_metal:
                time.sleep(60)
                found_collect = bnt_collect.find_and_click(wait_time=5, loop=True)
                if found_collect is not None:
                    self.touch_service.execute(screen_touch.ACTION_CLICK, pixel=Pixel(60, 550))
                    self.job_hub.collect_trade_depot.execute()
                    bnt_close.find_and_click()
