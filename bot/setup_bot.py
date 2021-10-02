from bot.basicbot import BasicBot
from object import factory, button
from object.button import BntFactory
from object.item import Metal, Wood, Plastic, Seed, Mineral, Chemical, Textile, Sugar
from object.trade_depot import TradeDepot, SaleItemWindow
from service import screen_capture, screen_touch
from object.factory import Factory


class SetupBot(BasicBot):
    def __init__(self):
        super().__init__('Setup Bot')
        self.screen_capture = self.service_hub.screen_capture
        self.location_service = self.service_hub.object_location
        self.screen_touch = self.service_hub.screen_touch

    def run(self):
        self.job_hub.change_map_view.execute()
        self.screen_touch.execute(screen_touch.ACTION_CLICK_CENTER, sleep_in=2)

        #
        # FACTORY
        #
        self.logger.info(f'{self.__class__}: Scan factory')
        factory_obj = Factory(factory.FACTORY_BASIC, 'metal')
        assert factory_obj.look().ok, f'{self.__class__}: Must start at the first factory'
        screen = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)

        metal_obj = Metal()
        wood_obj = Wood()
        plastic_obj = Plastic()
        seed_obj = Seed()
        mineral_obj = Mineral()
        chemical_obj = Chemical()
        textile_obj = Textile()
        sugar_obj = Sugar()
        bnt_next = BntFactory.make(button.BNT_RIGHT)

        metal_obj.look(image=screen, save_loc=True)
        wood_obj.look(image=screen, save_loc=True)
        plastic_obj.look(image=screen, save_loc=True)
        seed_obj.look(image=screen, save_loc=True)
        mineral_obj.look(image=screen, save_loc=True)
        chemical_obj.look(image=screen, save_loc=True)
        textile_obj.look(image=screen, save_loc=True)
        sugar_obj.look(image=screen, save_loc=True)
        bnt_next.look(image=screen, save_loc=True)

        self.location_service.factory.metal = metal_obj.location
        self.location_service.factory.wood = wood_obj.location
        self.location_service.factory.plastic = plastic_obj.location
        self.location_service.factory.seed = seed_obj.location
        self.location_service.factory.mineral = mineral_obj.location
        self.location_service.factory.chemical = chemical_obj.location
        self.location_service.factory.textile = textile_obj.location
        self.location_service.factory.sugar = sugar_obj.location
        self.location_service.factory.bnt_next = bnt_next.location

        #
        # Trade depot
        #
        self.logger.info(f'{self.__class__}: Scan trade_depot')
        self.screen_touch.execute(screen_touch.ACTION_CLICK,
                                  pixel=self.location_service.trade_depot.location, sleep_in=2)
        trade_depot_obj = TradeDepot([])
        assert trade_depot_obj.look().ok, f'{self.__class__}: Cannot open trade depot using given location'
        screen = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)

        bnt_close_depot = BntFactory.make(button.BNT_CLOSE_BLUE)
        bnt_new_trade = BntFactory.make(button.BNT_TRADE_NEW)  # none
        bnt_close_depot.look(image=screen, save_loc=True)
        bnt_new_trade.look(image=screen, save_loc=True)

        self.location_service.trade_depot.bnt_close_depot = bnt_close_depot.location

        # TODO make sure new trade box (empty box) is ready
        bnt_new_trade.click(sleep_in=2)
        sale_item_obj = SaleItemWindow()
        assert sale_item_obj.look().ok, f'{self.__class__}: Cannot open new sale item window'
        screen = self.screen_capture.execute(screen_capture.GET_RECENT_IMAGE)

        bnt_close_sale = BntFactory.make(button.BNT_CLOSE_BLUE)
        bnt_plus = BntFactory.make(button.BNT_TRADE_PLUS)
        bnt_put_sale = BntFactory.make(button.BNT_TRADE_PUT)
        bnt_close_sale.look(image=screen, save_loc=True)
        find_bnt_plus = bnt_plus.look(image=screen, get_all=True)
        assert len(find_bnt_plus.action_return) == 2, f'{self.__class__}: Plus button in sale window must have 2 items'
        bnt_put_sale.look(image=screen, save_loc=True)

        self.location_service.trade_depot.bnt_close_depot = bnt_close_depot.location
        self.location_service.trade_depot.bnt_sale_plus_1 = find_bnt_plus.action_return[0][0]
        self.location_service.trade_depot.bnt_sale_plus_2 = find_bnt_plus.action_return[1][0]
        self.location_service.trade_depot.bnt_put_sale = bnt_put_sale.location
        self.location_service.trade_depot.bnt_close_sale = bnt_close_sale.location

        # Close Trade depot
        bnt_close_sale.click(sleep_in=1)
        bnt_close_depot.click(sleep_in=1)

        self.logger.info(f'{self.__class__}: Scan is done, export to file')
        print(self.location_service.export(overwrite=True))