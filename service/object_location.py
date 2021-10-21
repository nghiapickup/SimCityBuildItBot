import inspect
import yaml

from object.display import Pixel
from service.service import BasicService
from utils.config import Config


class TradeHq:
    location = None


class TradeDepotLoc:
    location = None
    bnt_close_depot = None
    bnt_sale_plus_1 = None
    bnt_sale_plus_2 = None
    bnt_put_sale = None
    bnt_close_sale = None


class ManufacturerLoc:
    first_manufacturer = None
    bnt_next = None
    producing_area = None # x-axis's constraint


class FactoryLoc:
    metal = None
    wood = None
    plastic = None
    seed = None
    mineral = None
    chemical = None
    textile = None
    sugar = None


class Location(BasicService):
    def __init__(self):
        super().__init__()
        resource_config = Config.get_instance().resource_config
        self.location_file_dir = resource_config.object_loc_dir
        self._load_location_file()
        self.building_config = Config.get_instance().building_config

        self.manufacturer = ManufacturerLoc
        self.factory = FactoryLoc
        self.trade_depot = TradeDepotLoc
        self.trade_hq = TradeHq

        self._load_init_location()

    def parse_location(self, building, name):
        return Pixel.from_list(self._loaded_yaml[building][name])

    def _load_location_file(self):
        with open(self.location_file_dir, "r") as stream:
            try:
                self._loaded_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                self.logger.error(e)
                raise IOError(f'Cannot load location config file:{self.location_file_dir} ')

    def _load_init_location(self):
        # Load init location from config
        try:
            self.manufacturer.first_manufacturer = self.building_config.manufacturer['first_manufacturer_location']
            self.trade_depot.location = self.building_config.trade_depot['location']
            self.trade_hq.location = self.building_config.trade_hq['location']
        except Exception as e:
            self.logger.error(e)
            raise IOError(f'Cannot load the basic config manufacturer.first_manufacturer '
                          f'or trade_depot.location '
                          f'or trade_hq.location')

    @staticmethod
    def _export_class_attributes(inspect_class):
        attributes = inspect.getmembers(inspect_class, lambda a: not (inspect.isroutine(a)))
        attributes =  [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]

        res = {}
        for a in attributes:
            res[a[0]] = [float(a[1].x), float(a[1].y)]
        return res

    def export(self, overwrite=False):
        self.logger.info(f'{self.__class__}: Export(overwrite={overwrite})')
        factory_dict = self._export_class_attributes(self.factory)
        trade_depot_dict = self._export_class_attributes(self.trade_depot)
        manufacturer_dict = self._export_class_attributes(self.manufacturer)
        trade_hq_dict = self._export_class_attributes(self.trade_hq)

        final_export = {
            'manufacturer': manufacturer_dict,
            'factory': factory_dict,
            'trade_depot': trade_depot_dict,
            'trade_hq': trade_hq_dict
        }

        if overwrite:
            with open(self.location_file_dir, 'w') as yaml_file:
                yaml.safe_dump(final_export, yaml_file, default_flow_style = False)

        return final_export
