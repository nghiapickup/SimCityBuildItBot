import time, timeit
from bot.bot import Bot
from object.button import BntFactory
from object import button
from object.display import Pixel
from object.factory import Factory
from object import factory
from service import screen_touch


class ProduceFactoryBot(Bot):
    def __init__(self):
        super().__init__('Produce and sale metal')
        self.touch_service = self.service_hub.screen_touch
        self.factory = Factory(factory.FACTORY_BASIC)

    def run(self):
        self.job_hub.change_map_view.execute()

        bnt_close = BntFactory.get(button.BNT_CLOSE_BLUE)
        bnt_right = BntFactory.get(button.BNT_RIGHT)
        bnt_collect = BntFactory.get(button.BNT_COLLECT)

        # process always start and end at factory
        while True:
            # open the first factory
            click_count = 0
            while click_count<self.factory.max_quantity+1 and self.factory.look() is None:
                self.touch_service.execute(screen_touch.ACTION_CLICK_CENTER)
                click_count += 1

            if click_count == self.factory.max_quantity + 1:
                raise ModuleNotFoundError(f'{self.__class__: Cannot click into factory!}')

            is_produced = False
            start = timeit.default_timer() # Start the clock
            for produce_item in self.factory.produce_list:
                self.logger.info(f'Start factory {produce_item.name}!')
                produced_item = self.job_hub.produce_factory.execute(item=produce_item)
                bnt_right.find_and_click(wait_time=0, sleep_time=2)
                if produced_item and not is_produced:
                    is_produced=True
                    start = timeit.default_timer()

            # Wait 60 second from start
            time.sleep(max(60 - (timeit.default_timer() - start), 0))

            # return again and collect
            for produce_item in self.factory.produce_list:
                self.logger.info(f'Collect factory {produce_item.name}!')
                bnt_collect.find_and_click(wait_time=1, sleep_time=0, loop=True)
                bnt_right.find_and_click(wait_time=0, sleep_time=2)

            if is_produced:
                self.touch_service.execute(screen_touch.ACTION_CLICK, pixel=Pixel(60, 550))
                time.sleep(2)
                self.job_hub.collect_trade_depot.execute(trade_items=self.factory.produce_list)
                bnt_close.find_and_click(wait_time=0, sleep_time=2) # wait 2s after close trade pot
