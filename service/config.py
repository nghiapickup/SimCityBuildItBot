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


class Config:
    _instance = None

    @staticmethod
    def get_instance():
        if Config._instance is None:
            Config()
        return Config._instance

    def __init__(self):
        with open("config.yaml", "r") as stream:
            try:
                self._loaded_yaml = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                raise IOError(f'Cannot load config file! {e}')

        try:
            self.device_config = DeviceConfig(self._loaded_yaml['device'])
            self.resource_config = ResourceConfig(self._loaded_yaml['resources'])
        except Exception as e:
            raise IOError(f'Cannot load config value! {e}')

        Config._instance = self
