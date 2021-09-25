import os, subprocess
from service.service import AbsService
from service.config import Config
from object.display import Screen

# Device type
GENYMOTION = 1
ANDROID_STUDIO = 2


class Device(AbsService):
    def __init__(self, serial=None, type=GENYMOTION):
        """
        Init connection to a device. By default the device is loaded from genymotion emulator
        :param serial: device serial, it None, the first in adb devices list will be chosen
        :param type: adb to to execute
        """
        super().__init__()
        self.config = Config.get_instance().device_config
        self.adbDir = {
            GENYMOTION: self.config.adb_genymotion,
            ANDROID_STUDIO: self.config.adb_android_studio
        }[type]

        self.serial = self._get_device_serial(0) if serial is None else serial
        self.touch_device = self._get_touchscreen_device()
        self.screen = Screen(self.config.screen_x, self.config.screen_y)

    def _get_device_serial(self, index=0):
        """
        Get running device by index return from command [adb devices]. Default is 0
        :param index: device index to get
        :return: running device string
        """
        return [str(dev, 'utf-8').split('\t')[0]
                for dev in subprocess.check_output([self.adbDir, 'devices']).splitlines()
                if dev.endswith(str.encode('\tdevice'))][index]

    def _get_touchscreen_device(self):
        """
        Get touch screen device by execute adb getevent -il
        * only get the first one
        :return:
        """
        return [dev.splitlines()[0].split()[-1]
                for dev in self.adb_shell('getevent -il').split('add device ')
                if dev.find('ABS_MT_POSITION_X') > -1][0]

    def adb_shell(self, command):
        args = [self.adbDir, '-s', self.serial, 'shell', command]
        return os.linesep.join([str(dev, 'utf-8') for dev in subprocess.check_output(args).splitlines()])

    def abd_sendevents(self, event_tuples):
        template = f'sendevent {self.touch_device }' + ' {} {} {}'
        cmd = str.join(';', [template.format(e_type, e_code, e_vaulue) for (e_type, e_code, e_vaulue) in event_tuples])
        return self.adb_shell(cmd)

    def adb_screen_cap(self, save_dir=None):
        """
        Capture screen shot and save to save_dir, return bitmap stdout if save_dir is not provided
        :param save_dir: dir to save, if not provided, capture_output is True
        :return:
        """
        args = [self.adbDir, '-s', self.serial, 'exec-out', 'screencap -p']

        if save_dir is not None:
            with open(save_dir, 'w') as f:
                return subprocess.run(args, stdout=f)

        return subprocess.run(args, capture_output=True)

