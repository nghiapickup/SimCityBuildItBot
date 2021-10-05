import time
from bot.basicbot import BasicBot
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


class ProduceFactoryBot(BasicBot):
    def __init__(self):
        super().__init__('Running Factory')
        self.touch_service = self.service_hub.screen_touch
        self._setup_factory()

        self.trade_depot = TradeDepot(trade_items=[])

    def _setup_factory(self):
        building_config = Config.get_instance().building_config
        self.factory_num = building_config.manufacturer['num_factory']

        produce_list_name = building_config.factory['produce_list']
        assert len(produce_list_name) == self.factory_num,\
            f'Factory number is different from produce_list size({produce_list_name} != {self.factory_num})'
        self.factory_list = [Factory(ItemFactory.from_str(name)) for name in produce_list_name]
        self.factory_ad_list = building_config.factory['ad_item_list']

    def _get_factories_status(self):
        current_time = time.time()
        status = [f.next_release_time-current_time for f in self.factory_list]
        return min(status), status

    def run(self):
        self.job_hub.change_map_view.execute()
        self.touch_service.execute(screen_touch.ACTION_CLICK_CENTER, sleep_in=1)

        # process always start and end at factory
        while True:
            self.logger.info(f'{self.__class__}Check factory status and sleep if none of them are free')
            # Check factory status and sleep if none of them are free
            time_left, factory_status = self._get_factories_status()
            while time_left > 0:
                self.logger.info(f'{self.__class__}: None of factory is done. '
                                 f'Free in next {time_left+1} second(s)!')
                time.sleep(time_left+1)
                time_left, factory_status = self._get_factories_status()

            # Start production line
            self.logger.info(f'{self.__class__}: Start production line')
            for fid, fac in enumerate(self.factory_list):
                self.logger.info(f'Check factory {fid}, {fac.product_item.name} product!')
                if factory_status[fid] > 0:
                    if fid == 0: fac.click(wait_open_window=True) # first factory
                    self.logger.info(f'{fac.product_item.name} is not ready, go to next factory!')
                    check_ad = fac.product_item.name in self.factory_ad_list
                    if fac.click_next(check_ad=check_ad):
                        continue
                produce_status = fac.start_produce()
                fac.sleep(1, 'Sleep after start_produce')
                if produce_status: # sell what we produce
                    self.trade_depot.trade_list.append(fac.product_item)
                fac.click_next()

            if self.trade_depot.can_trade():
                self.open_trade_depot()
                self.trade_depot.start_trade()
                self.trade_depot.close()

    def open_trade_depot(self):
        self.logger.info(f'{self.__class__}: click_trade_depot')
        self.trade_depot.click(wait_open_window=True)
        if not self.trade_depot.look_and_wait(wait_time=1, try_time=1).ok:
            banner_ad = BannerAd()
            if banner_ad.look().ok:
                banner_ad.watch()
            self.trade_depot.click(wait_open_window=True)