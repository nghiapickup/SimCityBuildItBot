from bot.job.change_map_view import ChangeMapView
from bot.job.click_center import ClickCenter
from bot.job.click_storage import ClickStorage
from bot.job.click_opinion import ClickOpinion
from bot.job.collect_and_trade_depot import CollectAndTradeDepot


class JobHub:
    def __init__(self, service_hub):
        self.service_hub = service_hub
        self.device = self.service_hub.device

        self.change_map_view = ChangeMapView(self.device, service_hub)
        self.click_center = ClickCenter(self.device, service_hub)
        self.click_storage = ClickStorage(self.device, service_hub)
        self.click_opinion = ClickOpinion(self.device, service_hub)
        self.collect_trade_depot = CollectAndTradeDepot(self.device, service_hub)