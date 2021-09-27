import time

from job.job import AbsJob
from object.button import BntTradeDone, BntTradeNew, BntCloseBlue, BntTradePlus, BntTradePut
from service import screen_touch


class CollectAndTradeDepot(AbsJob):
    def __init__(self):
        """
        This is intended that trade pot is already open
        (need to sleep after click trade pot before)
        and close depot when job is done
        :param device:
        :param service_hub:
        """
        super().__init__('Collect and trade depot')
        self.screen_touch = self.service_hub.screen_touch

    def execute(self, trade_items):
        bnt_trade_done = BntTradeDone()
        bnt_trade_new = BntTradeNew()
        self.logger.info(f'{self.__class__}: Collect all done trade, no re-find and no-wait after click!')
        bnt_trade_done.find_and_click(wait_time=0, sleep_time=0, loop=True)
        # wait 2s after click trade new

        trade_set = set(trade_items)
        while len(trade_set) > 0:
            trade_item = trade_set.pop()
            new_trade_return = bnt_trade_new.find_and_click(wait_time=0, sleep_time=2, loop=True,
                                         callback=self._trade_new, trade_item=trade_item)
            if new_trade_return is None: # found slot but failed to trade
                break

        if len(trade_set) > 0:
            # wipe right and find trade box again
            self.screen_touch.execute(screen_touch.ACTION_WIPE_CENTER)
            time.sleep(2) # sleep after wipe to stablize the screen
            bnt_trade_done.find_and_click(wait_time=0, sleep_time=0, loop=True)
            while len(trade_set) > 0:
                trade_item = trade_set.pop()
                new_trade_return = bnt_trade_new.find_and_click(wait_time=0, sleep_time=2, loop=True,
                                             callback=self._trade_new, trade_item=trade_item)
                if new_trade_return is None: # cannot find slot, trade done
                    break

        self.logger.info(f'{self.__class__}: All trade is done!')

    def _trade_new(self, _, trade_item):
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
        found_item = trade_item.find_and_click(wait_time=2)
        if found_item is not None:
            mes = f'{self.__class__}: Start to trade {trade_item.name}!'
            self.logger.info(mes)

            # Click plus
            found_plus = bnt_plus.look(get_all=True)
            if found_plus is not None:
                for found in found_plus:
                    plus_loc, _, _ = found
                    self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=plus_loc, hold=3)

            # close trade item window if cannot find put trade button
            if bnt_trade.find_and_click(wait_time=0, sleep_time=1) is not None:
                is_trade = True

        # close trade window if cannot trade
        if not is_trade:
            bnt_close.find_and_click(wait_time=0, sleep_time=1)
        return is_trade
