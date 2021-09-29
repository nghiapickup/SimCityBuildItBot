import os
import yaml

class DeviceConfig:
    def __init__(self, config_yaml):
        self.adb_genymotion = config_yaml['adb']['genymotion']
        self.adb_android_studio = config_yaml['adb']['android_studio']
        self.screen_x = config_yaml['screen_x']
        self.screen_y = config_yaml['screen_y']


class ResourceConfig:
    def __init__(self, config_yaml):
        self.screen_shot_dir = config_yaml['screen_shot_dir']
        self.object_image_dir = config_yaml['object_image_dir']


class LogConfig:
    def __init__(self, config_yaml):
        self.log_dir = config_yaml['log_dir']


class BuildingConfig:
    def __init__(self, config_yaml):
        self.factory_count = config_yaml['factory_count']
        self.factory_produce_list = config_yaml['factory_produce_list']
        self.factory_check_ad = config_yaml['factory_check_ad']


class Config:
    _instance = None

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config()
        return Config._instance

    def __init__(self):
        yaml_dir = '{os_path}/../config.yaml'.format(os_path=os.path.dirname(os.path.abspath(__file__)))
        with open(yaml_dir, "r") as stream:
            try:
                self._loaded_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                raise IOError(f'Cannot load config file! {e}')

        try:
            self.device_config = DeviceConfig(self._loaded_yaml['device'])
            self.resource_config = ResourceConfig(self._loaded_yaml['resources'])
            self.log_config = LogConfig(self._loaded_yaml['logging'])
            self.building_config = BuildingConfig(self._loaded_yaml['building'])
        except Exception as e:
            raise IOError(f'Cannot load config value! {e}')

        Config._instance = self
