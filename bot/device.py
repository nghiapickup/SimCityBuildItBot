import os, subprocess
from utils.config import Config

# Device type
GENYMOTION = 1
ANDROID_STUDIO = 2


class Device:
    def __init__(self, serial=None, type=GENYMOTION):
        """
        Init connection to a device. By default the device is loaded from genymotion emulator
        :param serial: device serial, it None, the first in adb devices list will be chosen
        :param type: adb to to execute
        """
        self.config = Config.get_instance()
        self.adbDir = {
            GENYMOTION: self.config.device.adb_genymotion,
            ANDROID_STUDIO: self.config.device.adb_android_studio
        }[type]

        self.serial = self._get_device_serial(0) if serial is None else serial
        self.touch_device = self._get_touchscreen_device()

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


if __name__ == '__main__':
    new_device = Device()
    # click on bottom right
    events = [(1, 330, 1), (3, 58, 1), (3, 53, 80), (3, 54, 1833), (0, 2, 0), (0, 0, 0), (1, 330, 0), (0, 2, 0), (0, 0, 0)]
    print(new_device.abd_sendevents(events))

    # tap(touchdev, 100, 100, serial)

