from job.change_map_view import ChangeMapView
from job.click_storage import ClickStorage
from job.click_opinion import ClickOpinion
from job.collect_and_trade_depot import CollectAndTradeDepot
from job.produce_factory import ProduceFactory


class JobHub:
    _instance = None

    @staticmethod
    def get_instance():
        if JobHub._instance is None:
            JobHub()
        return JobHub._instance

    def __init__(self):
        self.change_map_view = ChangeMapView()
        self.click_storage = ClickStorage()
        self.click_opinion = ClickOpinion()
        self.collect_trade_depot = CollectAndTradeDepot()
        self.produce_factory = ProduceFactory()

        JobHub._instance = self
