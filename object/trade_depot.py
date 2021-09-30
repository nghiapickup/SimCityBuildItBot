import time

from object import button
from object.button import BntFactory
from object.object import BasicObject
from service import screen_touch, screen_capture


class SaleItemWindow(BasicObject):
    def __init__(self):
        super(SaleItemWindow, self).__init__('sale_item_window')
        self.n_sample = 1
        self.plus_buttons = [BntFactory.make(button.BNT_TRADE_PUT), BntFactory.make(button.BNT_TRADE_PUT)]
        self.bnt_put_trade = BntFactory.make(button.BNT_TRADE_PUT)
        self.bnt_close = BntFactory.make(button.BNT_CLOSE_BLUE)


class TradeDepot(BasicObject):
    def __init__(self, trade_items):
        super().__init__('trade_depot')
        self.n_sample = 1

        self.screen_touch = self.service_hub.screen_touch
        self.screen_capture = self.service_hub.screen_capture
        self.sale_window = SaleItemWindow()
        self.trade_set = set(trade_items)
        self.bnt_trade_new = BntFactory.make(button.BNT_TRADE_NEW)
        self.bnt_trade_done = BntFactory.make(button.BNT_TRADE_DONE)
        self.end_trade_bnt = BntFactory.make(button.BNT_BUY_TRADE_SLOT)

    def can_trade(self):
        return len(self.trade_set) # have sth to sell

    def start_trade(self):
        self.logger.info(f'{self.__class__}: Start trading')

        # Slide trade window and start trade
        is_end = False
        while self.can_trade() and not is_end:
            find_trade_depot = self.look_and_wait(wait_time=1, try_time=1)
            if not find_trade_depot.ok:
                raise ModuleNotFoundError(f'{self.__class__}: Trade depot window is not open')
            # Save time by using previous screen shot
            screen_image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
            is_end = self.end_trade_bnt.look(image=screen_image).ok
            self._trade_new_window(screen_image)

        self.logger.info(f'{self.__class__}: All trade is done!')
        return True

    def _trade_new_window(self, screen_image):
        self.logger.info(f'{self.__class__}: Trade on new window')
        trade_slot = []

        self.logger.info(f'{self.__class__}: Check done trade')
        find_done_trade = self.bnt_trade_done.find_all_and_click(image=screen_image, sleep_time=0.2)
        if find_done_trade.ok:
            trade_slot.extend(find_done_trade.action_return)

        self.logger.info(f'{self.__class__}: Check free trade slot')
        find_free_box = self.bnt_trade_new.look(image=screen_image, get_all=True)
        if find_free_box.ok:
            trade_slot.extend(find_free_box.action_return)

        for free_trade_slot in trade_slot:
            if not self.can_trade(): break
            self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=free_trade_slot[0])
            self._sale_item_window()

        if self.can_trade():
            # sleep after wipe makes sure the window is fully changed
            self.logger.info(f'{self.__class__}:_trade_new_window: wipe right & force to sleep')
            self.service_hub.screen_touch.execute(screen_touch.ACTION_WIPE_CENTER, sleep_in=1)

    def _sale_item_window(self):
        """
        perform new trade, if all trade item is traded,
        return False to exit the loop
        :param _: callback annotator, found item info
        :param trade_list: list item to trade
        :return:
        """
        is_done = False
        if self.sale_window.look_and_wait(wait_time=1, try_time=1).ok:
            # Save time by using previous screen shot
            screen_image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
            while self.can_trade(): # Make sure you are in sale window
                trade_item = self.trade_set.pop()
                find_trade_item = trade_item.find_and_click(
                    image=screen_image, wait_time=0,
                    try_time=0, sleep_time=0
                )
                if find_trade_item.ok:
                    self.logger.info(f'{self.__class__}: Start to trade {trade_item.name}!')
                    # find plus button and save loc for the next time
                    if self.sale_window.plus_buttons[0].location is None:
                        bnt_plus = BntFactory.make(button.BNT_TRADE_PLUS)
                        plus_action = bnt_plus.look(image=screen_image, get_all=True)
                        assert len(plus_action.action_return) == 2, \
                            'Plus button number in sale window must be 2, ' \
                            'but {len(plus_action.action_return)} found!'
                        self.sale_window.plus_buttons[0].location = plus_action.action_return[0][0]
                        self.sale_window.plus_buttons[1].location = plus_action.action_return[1][0]
                    for plus_bnt in self.sale_window.plus_buttons:
                        self.screen_touch.execute(screen_touch.ACTION_CLICK, pixel=plus_bnt.location, hold=1.5)

                    # put sale bnt
                    if self.sale_window.bnt_put_trade.location is None:
                        found_bnt = self.sale_window.bnt_put_trade.find_and_click(
                            image=screen_image, try_time=0,
                            wait_time=0, sleep_time=1
                        )
                        self.sale_window.bnt_put_trade.location = found_bnt.action_return[0][0]
                    self.screen_touch.execute(screen_touch.ACTION_CLICK,
                                              pixel=self.sale_window.bnt_put_trade.location,
                                              sleep_in=1)

                    self.trade_set.add(trade_item)
                    is_done = True
                    break

            # close trade item window if failed to create new trade
            if not is_done:
                if not self.sale_window.bnt_close.location:
                    self.sale_window.bnt_close.look(image=screen_image, save_loc=True)
                self.sale_window.bnt_close.click(sleep_in=1.5)

        return is_done
