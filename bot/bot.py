from object import items, buttons
from service import screen_touch
from service.hub import JobHub, ServiceHub
from object.city import City
from service.log import LogHandle


class Bot:
    def __init__(self, name):
        self.logger = LogHandle('bot').get_logger()
        self.name = name
        self.service_hub = ServiceHub.get_instance()
        self.job_hub = JobHub(self.service_hub)

    def run(self):
        capitol = City("Capitol City")

        # Change View
        # self.job_hub.change_map_view.execute()
        # self.job_hub.click_center.execute()

        metal = items.Metal()
        bnt_empty = buttons.BntEmpty()

        empty_loc = bnt_empty.find_one(show=True)
        # while empty_loc is not None:
        #     print(f'Has empty slot at {empty_loc}!')
        #     metal_loc = metal.find_one()
        #     path = [metal_loc, empty_loc]
        #     self.service_hub.screen_touch.execute(screen_touch.ACTION_WIPE, is_sleep=1, pixel_path = path, n_step=8)
        #     empty_loc = bnt_empty.find_one()