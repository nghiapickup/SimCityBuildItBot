import cv2

from bot.basicbot import BasicBot
from object import factory, button, item
from object.button import BntFactory
from object.display import Pixel
from object.item import Metal, Wood, Plastic, Seed, Mineral, Chemical, Textile, Sugar
from object.trade_depot import TradeDepot, SaleItemWindow
from service import screen_capture, screen_touch
from object.factory import Factory


class SetupBot(BasicBot):
    def __init__(self):
        super().__init__('Setup Bot')
        self.screen_capture = self.service_hub.screen_capture
        self.object_location = self.service_hub.object_location
        self.screen_touch = self.service_hub.screen_touch

    def _capture_scrren(self):
        return self.screen_capture.execute(screen_capture.SCREEN_SHOT, imread=cv2.IMREAD_GRAYSCALE)

    def _assertion(self, obj, screen):
        assert obj.look(image=screen, save_loc=True).ok, f'{obj.name} cannot be found!'

    def run(self):
        self.job_hub.change_map_view.execute()
        self.screen_touch.execute(screen_touch.ACTION_CLICK_CENTER, sleep_in=2)

        #
        # MANUFACTURER
        #
        self.logger.info(f'{self.__class__}: Scan factory')
        screen = self._capture_scrren()

        bnt_next = BntFactory.make(button.BNT_RIGHT)
        assert bnt_next.look(image=screen, save_loc=True).ok, 'mineral_obj cannot be found!'
        self.object_location.manufacturer.bnt_next = bnt_next.location
        screen_x = self.service_hub.device.screen.x_size
        self.object_location.manufacturer.producing_area = Pixel(int(3.0/4*screen_x), screen_x)

        #
        # FACTORY
        #
        metal_obj = Metal()
        wood_obj = Wood()
        plastic_obj = Plastic()
        seed_obj = Seed()
        mineral_obj = Mineral()
        chemical_obj = Chemical()
        textile_obj = Textile()
        sugar_obj = Sugar()

        self._assertion(metal_obj, screen)
        self._assertion(wood_obj, screen)
        self._assertion(plastic_obj, screen)
        self._assertion(seed_obj, screen)
        self._assertion(mineral_obj, screen)
        self._assertion(chemical_obj, screen)
        self._assertion(textile_obj, screen)
        self._assertion(sugar_obj, screen)

        self.object_location.factory.metal = metal_obj.location
        self.object_location.factory.wood = wood_obj.location
        self.object_location.factory.plastic = plastic_obj.location
        self.object_location.factory.seed = seed_obj.location
        self.object_location.factory.mineral = mineral_obj.location
        self.object_location.factory.chemical = chemical_obj.location
        self.object_location.factory.textile = textile_obj.location
        self.object_location.factory.sugar = sugar_obj.location

        #
        # Trade depot
        #
        self.logger.info(f'{self.__class__}: Scan trade_depot')
        self.screen_touch.execute(screen_touch.ACTION_CLICK,
                                  pixel=self.object_location.trade_depot.location, sleep_in=2)
        screen = self._capture_scrren()

        bnt_close_depot = BntFactory.make(button.BNT_CLOSE_BLUE)
        bnt_new_trade = BntFactory.make(button.BNT_TRADE_NEW)  # none
        self._assertion(bnt_close_depot, screen)
        self._assertion(bnt_new_trade, screen)

        self.object_location.trade_depot.bnt_close_depot = bnt_close_depot.location

        # TODO make sure new trade box (empty box) is ready
        bnt_new_trade.click(sleep_in=2)
        screen = self._capture_scrren()

        bnt_close_sale = BntFactory.make(button.BNT_CLOSE_BLUE)
        bnt_plus = BntFactory.make(button.BNT_TRADE_PLUS)
        bnt_put_sale = BntFactory.make(button.BNT_TRADE_PUT)
        self._assertion(bnt_close_sale, screen)
        find_bnt_plus = bnt_plus.look(image=screen, get_all=True)
        assert len(find_bnt_plus.action_return) == 2, f'{self.__class__}: Plus button in sale window must have 2 items'
        self._assertion(bnt_put_sale, screen)

        self.object_location.trade_depot.bnt_close_depot = bnt_close_depot.location
        self.object_location.trade_depot.bnt_sale_plus_1 = find_bnt_plus.action_return[0][0]
        self.object_location.trade_depot.bnt_sale_plus_2 = find_bnt_plus.action_return[1][0]
        self.object_location.trade_depot.bnt_put_sale = bnt_put_sale.location
        self.object_location.trade_depot.bnt_close_sale = bnt_close_sale.location

        # Close Trade depot
        bnt_close_sale.click(sleep_in=1)
        bnt_close_depot.click(sleep_in=1)

        self.logger.info(f'{self.__class__}: Scan is done, export to file')
        print(self.object_location.export(overwrite=True))