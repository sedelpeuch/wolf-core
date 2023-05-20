#! /usr/bin/env python3
import datetime
import logging
import os

from wolf_core import application


class Runner:
    """
    This class is the main class of the core module.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, debug=False):
        """
        This is the constructor of the class.
        """
        self._applications = []
        self.__debug = debug
        self.__status = {}
        self.__setup_logger()

    def __setup_logger(self):
        """
        This method sets up the logger. It creates a file handler and a console handler. The file handler logs all messages with level WARNING
        """
        log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(os.path.join(file_path, 'log'), exist_ok=True)
        file_handler = logging.FileHandler(file_path + "/log" + '/wolf_core_' + log_name + '.log')
        file_handler.setLevel(logging.WARNING)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def __load_applications(self):
        """
        This method loads the applications, by creating an instance of each application. The instances are re It also sets the logger of each
        application.
        """
        for app in application.Application.__subclasses__():
            self._applications.append(app())
            self.logger.debug("Application " + app.__name__ + " loaded.")
        for app in self._applications:
            app.logger = self.logger

    def __get_all_status(self):
        """
        This method gets the status of all applications and stores it in the _status dictionary.
        """
        for app in self._applications:
            self.__status[app.__class__.__name__] = app.status

    def run(self):
        """
        This method runs the core module by calling the job method of each application. If the debug flag is set, the job method is called only
        once immediately. If the debug flag is not set, the job method is scheduled to run at the frequency of the application.
        """
        self.__load_applications()
        if self.__debug:
            for app in self._applications:
                self.logger.debug("Application" + app.__class__.__name__ + " running.")
                app.job()
        else:
            for app in self._applications:
                app.frequency.do(app.run)
                self.logger.debug("Application " + app.__class__.__name__ + " scheduled to run every " + str(
                        app.frequency.interval) + " " + app.frequency.unit + ".")

    def shutdown(self):
        """
        This method shuts down the core module.
        """
        pass
