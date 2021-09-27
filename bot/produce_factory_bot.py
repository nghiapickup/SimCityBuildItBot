import time, timeit
from bot.bot import Bot
from object.banner_ad import BannerAd
from object.button import BntFactory
from object import button
from object.trade_depot import TradeDepot
from object.display import Pixel
from object.factory import Factory
from object import factory
from service import screen_touch


class ProduceFactoryBot(Bot):
    def __init__(self):
        super().__init__('Running Factory!')
        self.touch_service = self.service_hub.screen_touch
        self.factory = Factory(factory.FACTORY_MASS)

    def run(self):
        self.job_hub.change_map_view.execute()

        bnt_close = BntFactory.make(button.BNT_CLOSE_BLUE)
        bnt_right = BntFactory.make(button.BNT_RIGHT)

        # process always start and end at factory
        while True:
            # open the first factory
            click_count = 0
            while click_count<self.factory.max_quantity+1 and self.factory.look() is None:
                self.touch_service.execute(screen_touch.ACTION_CLICK_CENTER)
                click_count += 1

            if click_count == self.factory.max_quantity + 1:
                raise ModuleNotFoundError(f'{self.__class__}: Cannot click into {self.factory.name}!')

            is_produced = False
            start = timeit.default_timer() # Start the clock
            for _ in range (0,2): # Loop 2 times to collect item
                for produce_item in self.factory.produce_list:
                    self.logger.info(f'Check factory {produce_item.name}!')
                    produced_item = self.job_hub.produce_factory.execute(item=produce_item)
                    if produced_item and not is_produced: # Start time clock
                        is_produced=True
                        start = timeit.default_timer()

                    bnt_right.find_and_click(wait_time=0, sleep_time=2) # Sleep is needed to change the window

                # Wait 60 second from start
                time_left = max(60 - (timeit.default_timer() - start), 0)
                self.logger.info(f'{self.__class__}: Sleep to wait in {time_left} second(s).')
                time.sleep(time_left)

            if is_produced:
                trade_depot = TradeDepot()
                if trade_depot.click_from_factory():
                    self.job_hub.collect_trade_depot.execute(trade_items=self.factory.produce_list)
                    bnt_close.find_and_click(wait_time=0, sleep_time=2) # wait 2s after close trade pot
