from job.change_map_view import ChangeMapView
from job.click_storage import ClickStorage


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

        JobHub._instance = self
