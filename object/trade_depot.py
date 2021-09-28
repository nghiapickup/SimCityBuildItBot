import time

from object import button
from object.button import BntFactory
from object.object import BasicObject
from service import screen_touch


class TradeDepot(BasicObject):
    def __init__(self, trade_items):
        super().__init__('trade_depot')
        self.n_sample = 1

        self.screen_touch = self.service_hub.screen_touch
        self.trade_set = set(trade_items)

        self.bnt_plus_locs = None
        self.bnt_close = BntFactory.make(button.BNT_CLOSE_BLUE)
        self.bnt_trade = BntFactory.make(button.BNT_TRADE_PUT)
        self.bnt_trade_new = BntFactory.make(button.BNT_TRADE_NEW)

    def start_trade(self):
        self.logger.info(f'{self.__class__}: start_trade {self.trade_set}')

        # Slide trade window and start trade
        end_trade_signal = BntFactory.make(button.BNT_BUY_TRADE_SLOT)

        self._trade_new_window()
        while end_trade_signal.look().action_return is None:
            self._trade_new_window()

        self.logger.info(f'{self.__class__}: All trade is done!')
        return  True

    def _trade_new_window(self):
        self._collect_done_trade()
        while len(self.trade_set) > 0:
            new_trade_action = self.bnt_trade_new.find_and_click(
                wait_time=0, sleep_time=2, loop=True,
                callback=self._trade_new_item)
            if new_trade_action.action_return is None or \
                    new_trade_action.callback_return is None:  # found slot but failed to trade
                break

        if len(self.trade_set) > 0:
            # wipe right and find trade box again
            self.service_hub.screen_touch.execute(screen_touch.ACTION_WIPE_CENTER)
            time.sleep(2)  # sleep after wipe to stablize the screen

    def _trade_new_item(self, _):
        """
        perform new trade, if all trade item is traded,
        return False to exit the loop
        :param _: callback annotator, found item info
        :param trade_list: list item to trade
        :return:
        """
        if not len(self.trade_set):
            self.bnt_close.find_and_click(wait_time=0, sleep_time=2)
            return False

        trade_item = self.trade_set.pop()
        is_trade = False
        find_trade_item = trade_item.find_and_click(wait_time=2, sleep_time=0)
        if find_trade_item.action_return is not None:
            mes = f'{self.__class__}: Start to trade {trade_item.name}!'
            self.logger.info(mes)

            # add trade item again to check can be trade one more time
            self.trade_set.add(trade_item)

            # Click plus
            if self.bnt_plus_locs is None:
                bnt_plus = BntFactory.make(button.BNT_TRADE_PLUS)
                plus_action = bnt_plus.look(get_all=True)
                if plus_action.action_return is not None:
                    self.bnt_plus_locs = [found[0] for found in plus_action.action_return]

            for found in self.bnt_plus_locs:
                self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=found, hold=2)

            trade_action = self.bnt_trade.find_and_click(wait_time=0, sleep_time=1)
            if trade_action.action_return is not None:
                is_trade = True

        # close trade window if failed to put trade
        if not is_trade:
            self.bnt_close.find_and_click(wait_time=0, sleep_time=2)

        return True

    def _collect_done_trade(self):
        self.logger.info(f'{self.__class__}: Collect all done trades')
        bnt_trade_done = BntFactory.make(button.BNT_TRADE_DONE)
        bnt_trade_done.find_and_click(wait_time=0, sleep_time=0, loop=True)