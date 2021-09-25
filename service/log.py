import logging
from pathlib import Path
from service.config import Config
from logging.handlers import TimedRotatingFileHandler


class LogHandle:
    config = Config.get_instance().log_config
    base_log_folder = config.log_dir
    log_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')

    def __init__(self, file_name, category='', test_mode=False):
        self.test_mode = test_mode

        self.log_name = file_name
        self.log_error_name = file_name
        if self.test_mode:
            self.log_name = 'TEST_' + self.log_name
            self.log_error_name = 'TEST_' + self.log_error_name

        self.log_folder = f'{self.base_log_folder}{category}/'
        Path(self.log_folder).mkdir(parents=True, exist_ok=True)

        self.log_error_folder = f'{self.base_log_folder}error/{category}/'
        Path(self.log_error_folder).mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_folder + self.log_name
        self.log_error_file = self.log_error_folder + self.log_error_name
        self._set_new_handler()

        self.logger = None
        self.error_logger = None
        self.get_logger()
        self.get_error_logger()

    def _set_new_handler(self):
        self.my_handler = TimedRotatingFileHandler(self.log_file, when='midnight')
        self.my_handler.setFormatter(LogHandle.log_formatter)
        self.my_handler.setLevel(logging.INFO)

        self.my_error_handler = TimedRotatingFileHandler(self.log_error_file, when='midnight')
        self.my_error_handler.setFormatter(LogHandle.log_formatter)
        self.my_error_handler.setLevel(logging.INFO)

    def get_logger(self):
        if self.logger is None:
            app_log = logging.getLogger(self.log_file)
            app_log.addHandler(self.my_handler)
            app_log.setLevel(logging.INFO)
            self.logger = app_log
        return self.logger

    def get_error_logger(self):
        if self.error_logger is None:
            app_log = logging.getLogger(self.log_error_file)
            app_log.addHandler(self.my_error_handler)
            app_log.setLevel(logging.INFO)
            self.error_logger = app_log
        return self.error_logger
