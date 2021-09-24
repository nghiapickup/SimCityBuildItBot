import yaml


class DeviceConfig:
    def __init__(self, config_yaml):
        self.adb_genymotion = config_yaml['adb']['genymotion']
        self.adb_android_studio = config_yaml['adb']['android_studio']


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
            except yaml.YAMLError as exc:
                raise IOError(f'Cannot load config file! {exc}')

        try:
            self.device = DeviceConfig(self._loaded_yaml['device'])
        except Exception as e:
            raise IOError(f'Load ')

        Config._instance = self
