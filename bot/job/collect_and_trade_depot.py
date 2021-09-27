from bot.job.common import AbsJob
from object.button import BntTradeDone, BntTradeNew, BntCloseBlue, BntTradePlus, BntTradePut
from service import screen_touch


class CollectAndTradeDepot(AbsJob):
    def __init__(self, device, service_hub):
        """
        This is intended that trade pot is already open
        (need to sleep after click trade pot before)
        and close depot when job is done
        :param device:
        :param service_hub:
        """
        super().__init__('Collect and trade depot', device, service_hub)
        self.touch = service_hub.screen_touch
        self.screen = device.screen

    def execute(self, trade_items):
        bnt_trade_done = BntTradeDone()
        bnt_trade_new = BntTradeNew()
        self.logger.info(f'{self.__class__}: Collect all done trade, no re-find and no-wait after click!')
        bnt_trade_done.find_and_click(wait_time=0, sleep_time=0, loop=True)
        # wait 2s after click trade new
        bnt_trade_new.find_and_click(wait_time=0, sleep_time=2, loop=True,
                                     callback=self._trade_new, trade_list=trade_items)
        # wipe right and find trade box again
        self.touch.execute(screen_touch.ACTION_WIPE_CENTER)
        bnt_trade_new.find_and_click(wait_time=0, sleep_time=2, loop=True,
                                     callback=self._trade_new, trade_list=trade_items)

        self.logger.info(f'{self.__class__}: All trade is done!')

    def _trade_new(self, _, trade_list):
        """
        perform new trade, if all trade item is traded,
        return False to exit the loop
        :param _: callback annotator, found item info
        :param trade_list: list item to trade
        :return:
        """
        bnt_plus = BntTradePlus()
        bnt_close = BntCloseBlue()
        bnt_trade = BntTradePut()

        is_trade = False
        for item in trade_list:
            found_item = item.find_and_click(wait_time=2)
            if found_item is not None:
                mes = f'{self.__class__}: Start to trade {item.name}!'
                self.logger.info(mes)

                # Click plus
                found_plus = bnt_plus.look(all=True)
                if found_plus is not None:
                    for found in found_plus:
                        plus_loc, _, _ = found
                        self.touch.execute(screen_touch.ACTION_CLICK, pixel=plus_loc, hold=3)

                # close trade item window if cannot find put trade button
                if bnt_trade.find_and_click(wait_time=0, sleep_time=1) is not None:
                    is_trade = True
                    # trade is done, break to find new trade window
                    break

        # close trade window if cannot trade
        if not is_trade:
            bnt_close.find_and_click(wait_time=0, sleep_time=1)
        return is_trade
