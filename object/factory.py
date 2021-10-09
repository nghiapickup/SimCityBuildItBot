import time
from object import button, item, manufacturer
from object.item import ItemFactory
from object.manufacturer import Manufacturer, ProducingSlot
from service import screen_touch, screen_capture


class Factory(Manufacturer):
    """
    A factory produce only one product at a time
    """

    def __init__(self, item):
        super().__init__(manufacturer.FACTORY)
        self.n_sample = 2
        self.threshold = 0.75

        self.product_item = item
        self.product_item.location = self.object_location.parse_location('factory', self.product_item.name)

    def _init_producing_time(self, time_boxes):
        current_time = time.time()
        for time_box in time_boxes:
            loc, remaining_time = time_box
            distances = [loc.distance(slot.location) for slot in self.producing_slots]
            min_id = distances.index(min(distances))
            self.producing_slots[min_id].finish_time = current_time + remaining_time
        # Check again if any not-empty slot have not assigned yet
        # TODO Cannot do it!!!!!
        for slot in self.producing_slots:
            if slot.status != ProducingSlot.EMPTY and slot.finish_time is None:
                self.logger.info(f'{self.__class__} time_boxes found:{len(time_boxes)}')
                raise SystemError(f'An unknown box is found {slot.producing_item.name}')
        return True

    def start_produce(self):
        # init for the first time
        if len(self.producing_slots) == 0:
            image = self.assert_current_window()
            self.init_producing_list(image=image)

        self.logger.info(f'{self.__class__}: start_produce {self.product_item.name}')
        self.collect_finish_product()
        self.assert_current_window()
        is_produced = False
        start_time = time.time()
        for slot in self.producing_slots:
            if slot.status == ProducingSlot.EMPTY:
                self.logger.info(f'{self.__class__}: wipe {self.product_item.name} to slot')
                self.screen_touch.execute(
                    screen_touch.ACTION_WIPE_TO_CENTER,
                    from_pixel=self.product_item.location,
                    n_step=5,
                    hold=0
                )
                slot.status = ProducingSlot.IN_PROGRESS
                slot.finish_time = start_time + self.product_item.produce_time
                is_produced = True

        # update next release time by the first
        self._update_next_release_time()

        return is_produced
