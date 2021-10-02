import time
from bot.basicbot import BasicBot
from object.banner_ad import BannerAd
from object.button import BntFactory
from object import button
from object.display import Pixel
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
        self.factory_num = building_config.factory_count

        produce_list_name = building_config.factory_produce_list
        assert (len(produce_list_name) == self.factory_num,
                f'Factory number is different from produce_list size({produce_list_name} != {self.factory_num})')
        self.factory_list = [Factory(factory.FACTORY_MASS, name) for name in produce_list_name]
        self.factory_ad_list = building_config.factory_check_ad

    def _get_factories_status(self):
        status = [f.produce_time_left() for f in self.factory_list]
        return min(status), status

    def run(self):
        self.job_hub.change_map_view.execute()

        bnt_close = BntFactory.make(button.BNT_CLOSE_BLUE)

        # process always start and end at factory
        while True:
            self.logger.info(f'{self.__class__}Check factory status and sleep if none of them are free')
            # Check factory status and sleep if none of them are free
            time_left, factory_status = self._get_factories_status()
            while time_left > 0:
                self.logger.info(f'{self.__class__}: None of factory is done. '
                                 f'Free in next {time_left} second(s)!')
                time.sleep(time_left)
                time_left, factory_status = self._get_factories_status()

            self.logger.info(f'{self.__class__} Open the first factory')
            # open the first factory, click to collect item outside
            self._click_first_factory()

            # Start production line
            self.logger.info(f'{self.__class__}: Start production line')
            for fid, fac in enumerate(self.factory_list):
                self.logger.info(f'Check factory {fid}, {fac.product_item.name} product!')
                if factory_status[fid] > 0:
                    self.logger.info(f'{fac.product_item.name} is not ready, go to next factory!')
                    check_ad = fac.product_item.name in self.factory_ad_list
                    if fac.click_next(check_ad=check_ad): # continue if clicked
                        continue
                produce_status = fac.start_produce()
                if produce_status: # sell what we produce
                    self.trade_depot.trade_list.add(fac.product_item)
                fac.click_next()

            if self.trade_depot.can_trade():
                self.open_trade_depot()
                self.trade_depot.start_trade()
                self.trade_depot.close()

    def open_trade_depot(self):
        self.logger.info(f'{self.__class__}: click_trade_depot')
        self._click_trade_depot()
        if not self.trade_depot.look_and_wait(wait_time=1, try_time=1).ok:
            banner_ad = BannerAd()
            if banner_ad.look().ok:
                banner_ad.watch()
            self._click_trade_depot()

    def _click_trade_depot(self):
        self.service_hub.screen_touch.execute(
            screen_touch.ACTION_CLICK,
            pixel=Pixel(60, 500),
            sleep_in=2)

    def _click_first_factory(self):
        first_factory = self.factory_list[0]
        first_factory.click(sleep_in=0.2)
        for _ in range(0, first_factory.num_slot+1):
            if first_factory.look().ok: break
            first_factory.click(sleep_in=0.2)