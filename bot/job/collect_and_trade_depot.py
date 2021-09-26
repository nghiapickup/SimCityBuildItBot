from bot.job.common import AbsJob
from object.buttons import BntTradeDone, BntTradeNew, BntCloseBlue, BntTradePlus, BntTradePut
from object.items import Metal
from service import screen_touch
from service.hub import *


class CollectAndTradeDepot(AbsJob):
    trade_list = [Metal()]

    def __init__(self, device, service_hub):
        super().__init__('Collect and trade depot', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self):
        bnt_trade_done = BntTradeDone()
        bnt_trade_new = BntTradeNew()
        # Collect all done trade
        bnt_trade_done.find_and_click(wait_time=1, loop=True)
        bnt_trade_new.find_and_click(wait_time=2, loop=True, callback=self._trade_new)

    def _trade_new(self, _):
        """
        perform new trade, if all trade item do no exist, return false
        :param _:
        :return:
        """
        bnt_plus = BntTradePlus()
        bnt_close = BntCloseBlue()
        bnt_trade = BntTradePut()

        is_found = False
        for item in CollectAndTradeDepot.trade_list:
            found_item = item.find_and_click(wait_time=2)
            if found_item is not None:
                is_found = True
                mes = f'{self.__class__} found {item.name}!'
                self.logger.info(mes)

                # Click plus
                found_plus = bnt_plus.look(all=True)
                if found_plus is not None:
                    for found in found_plus:
                        plus_loc, _, _ = found
                        self.touch.execute(screen_touch.ACTION_CLICK, pixel=plus_loc, hold=2)

                # close trade window if cannot find put trade button
                if bnt_trade.find_and_click() is None:
                    bnt_close.find_and_click()

        # close trade depot if can not found any trade item
        if not is_found: bnt_close.find_and_click()
        return is_found
