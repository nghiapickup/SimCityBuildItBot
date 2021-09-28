import time, timeit
from bot.bot import Bot
from object.banner_ad import BannerAd
from object.button import BntFactory
from object import button
from object.display import Pixel
from object.item import ItemFactory
from object.trade_depot import TradeDepot
from object.factory import Factory
from object import factory
from service import screen_touch
from utils.config import Config


class ProduceFactoryBot(Bot):
    def __init__(self):
        super().__init__('Running Factory')
        self.touch_service = self.service_hub.screen_touch
        self._setup_factory()

    def _setup_factory(self):
        building_config = Config.get_instance().building_config
        self.factory_num = building_config.factory_count

        produce_list_name = building_config.factory_produce_list
        assert (len(produce_list_name) == self.factory_num,
                f'Factory number is different from produce_list size({produce_list_name} != {self.factory_num})')
        self.factory_list = [Factory(factory.FACTORY_MASS, name) for name in produce_list_name]
        self.trade_list = [] # todo temp

    def run(self):
        self.job_hub.change_map_view.execute()

        bnt_close = BntFactory.make(button.BNT_CLOSE_BLUE)

        # process always start and end at factory
        while True:
            # Check factory status and sleep if none of them are free
            factory_status = [f.produce_time_left() for f in self.factory_list]
            time_left = min(factory_status)
            while time_left > 0:
                self.logger.info(f'{self.__class__}: None of factory is done. '
                                 f'Free in next {time_left} second(s)!')
                time.sleep(time_left)
                factory_status = [f.produce_time_left() for f in self.factory_list]
                time_left = min(factory_status)

            # open the first factory, click to collect item outside
            click_count = 0
            first_factory = self.factory_list[0]
            while click_count<first_factory.num_slot+1 and first_factory.look().action_return is None:
                first_factory.click()
                click_count += 1
            if click_count == first_factory.num_slot+1:
                time.sleep(2)  # hold there for changing window
                if first_factory.look().action_return is None:
                    raise ModuleNotFoundError(f'{self.__class__}: Cannot click into {first_factory.name}!')

            # Start production line
            produce_status = False
            for fid, fac in enumerate(self.factory_list):
                self.logger.info(f'Check factory {fid}, {fac .product_item.name} product!')
                if factory_status[fid] > 0:
                    self.logger.info(f'{fac.product_item.name} is not ready, go to next factory!')
                    fac.click_next()
                    continue
                produce_status = fac.start_produce()
                if produce_status: # sell what we produce
                    self.trade_list.append(fac.product_item)
                fac.click_next()

            if len(self.trade_list): # have sth to sell
                if self.open_trade_depot():
                    trade_depot = TradeDepot(self.trade_list)
                    trade_depot.start_trade()
                    bnt_close.find_and_click(wait_time=0, sleep_time=2) # wait 2s after close trade pot

    def open_trade_depot(self):
        self.logger.info(f'{self.__class__}: click_trade_depot')
        self._click_trade_depot()
        trade_depot = TradeDepot([])
        if trade_depot.look().action_return is None:
            banner_ad = BannerAd()
            if banner_ad.look().action_return is not None:
                banner_ad.watch()
            self._click_trade_depot()

        return True

    def _click_trade_depot(self):
        self.service_hub.screen_touch.execute(
            screen_touch.ACTION_CLICK,
            pixel=Pixel(60, 500),
            sleep_in=2)
