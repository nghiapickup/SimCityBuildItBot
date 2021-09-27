import logging
from pathlib import Path
from utils.config import Config
from logging.handlers import TimedRotatingFileHandler
from multiprocessing_logging import install_mp_handler


class LogHandle:
    """
    How to use:
        new_log = LogHandle(name, cat_name, test_mode=?)
        log = new_log.logger
        err_log = newlog.error_log
    """
    config = Config.get_instance().log_config
    base_log_folder = config.log_dir
    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    def __init__(self, name, category='', test_mode=False):
        self.test_mode = test_mode

        self.log_name = name
        self.log_error_name = name
        if self.test_mode:
            self.log_name = 'TEST_' + self.log_name
            self.log_error_name = 'TEST_' + self.log_error_name

        self.log_folder = f'{self.base_log_folder}{category}/'
        Path(self.log_folder).mkdir(parents=True, exist_ok=True)
        self.log_error_folder = f'{self.base_log_folder}error/{category}/'
        Path(self.log_error_folder).mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_folder + self.log_name
        self.log_error_file = self.log_error_folder + self.log_error_name

        install_mp_handler()

        self._set_new_handler(self.log_file)
        self.logger = self._get_logger(self.log_file)
        self._set_new_handler(self.log_error_file)
        self.error_logger = self._get_logger(self.log_error_file)

    def _set_new_handler(self, filename, trigger_period='midnight',
                         backup_count=1, log_level = logging.INFO):
        self.my_handler = TimedRotatingFileHandler(filename, when=trigger_period, backupCount=backup_count)
        self.my_handler.setFormatter(LogHandle.log_formatter)
        self.my_handler.setLevel(log_level)

    def _get_logger(self, filename):
        app_log = logging.getLogger(filename)
        # check to don't re-add handler to the same log, it creates duplication
        if not len(app_log.handlers):
            app_log.addHandler(self.my_handler)
            app_log.setLevel(logging.INFO)
        return app_log