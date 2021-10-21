from bot.basicbot import BasicBot
from object import special_item, button
from object.button import BntFactory
from object.special_item import SpecialItemFactory
from object.trade_depot import TradeDepot
from object.trade_hq import TradeHq
from service import screen_capture
from utils.config import Config


class SearchSpecialItem(BasicBot):
    def __init__(self):
        super().__init__('Search Special Item in Trade HQ Bot')
        self.screen_touch = self.service_hub.screen_touch
        self.screen_capture = self.service_hub.screen_capture

        config = Config.get_instance().building_config
        search_item_names = config.trade_hq['search_items']
        self.search_items = [SpecialItemFactory.from_str(id) for id in search_item_names]

        self.trade_hq = TradeHq()
        self.trade_depot = TradeDepot([])
        self.bnt_home = BntFactory.make(button.BNT_HOME)

    def run(self):
        while True:
            self.trade_hq.click(wait_open_window=True)
            assert self.trade_hq.look_and_wait(wait_time=2, try_time=2).ok, 'Cannot open Trade HQ'

            found_item = None
            while found_item is None:
                self.trade_hq.look()
                image = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)
                for item in self.search_items:
                    if item.find_and_click(image=image, try_time=0).ok:
                        found_item = item
                        break
                if found_item is None:
                    if not self.trade_hq.bnt_refresh.find_and_click().ok:
                        self.trade_hq.sleep(1, 'No item found')

            if found_item is not None:
                # After clicked on trade hq
                found_depot = self.trade_depot.find_and_click(wait_time=0.5, try_time=20)

                if found_depot:
                    found_item.find_and_click(
                        wait_time=0.5,
                        try_time=20,
                        sleep_time=1,
                    )
                    # search for other item
                    for item in self.search_items:
                        item.find_and_click(try_time=0, sleep_time=1)

                # finally close and come back home
                self.trade_depot.close()
                self.bnt_home.find_and_click(try_time=2, wait_time=2, sleep_time=3, loop=True)

            self.trade_hq.sleep(5, 'Sleep after a round!')