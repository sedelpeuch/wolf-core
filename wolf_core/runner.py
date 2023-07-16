#! /usr/bin/env python3

"""
This module contains the Runner class.
"""

import datetime
import logging
import os
import threading
import time

import schedule

from wolf_core import application

THREAD_RUN = True


class Runner:
    """
    This class is the main class of the core module.
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self, debug=False, test=False):
        """
        This is the constructor of the class.
        """
        self._applications = []
        self.__debug = debug
        self.__test = test
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
        threading.Thread(target=self.__status_thread).start()
        time.sleep(1)

    def __load_applications(self):
        """
        This method loads the applications, by creating an instance of each application. The instances are re It also sets the logger of each
        application.
        """
        if len(self._applications) != 0:
            self.logger.debug("Deleting old applications.")
            self._applications = []
        for app in application.Application.__subclasses__():
            if self.is_method_overridden(app, "run"):
                self.logger.warning(
                    "Application " + app.__name__ + " overrides the run method. This is not allowed. Skipping application.")
                continue
            if not self.is_method_overridden(app, "job"):
                self.logger.warning(
                    "Application " + app.__name__ + " does not override the job method. This is not allowed. Skipping application.")
                continue
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

    def __status_thread(self):
        """
        This method is the thread that is run by the status method. It gets the status of all applications and prints it.
        """
        while THREAD_RUN:
            self.__get_all_status()
            for app in self._applications:
                if self.__status[app.__class__.__name__] is application.Status.ERROR:
                    self.logger.error("Application " + app.__class__.__name__ + " failed.")
                    self._applications[self._applications.index(app)].status = application.Status.WAITING
                elif self.__status[app.__class__.__name__] is application.Status.SUCCESS:
                    self.logger.warning("Application " + app.__class__.__name__ + " succeeded.")
                    self._applications[self._applications.index(app)].status = application.Status.WAITING
                elif self.__status[app.__class__.__name__] is application.Status.RUNNING:
                    self.logger.debug("Application " + app.__class__.__name__ + " is running.")
            if self.__debug:
                time.sleep(0.1)
            else:
                time.sleep(5)

    @staticmethod
    def is_method_overridden(app, method):
        """
        This method checks if the given method is overridden in any of the applications.

        :param app: The application to check.
        :param method: The method to check.
        :return: True if the method is overridden by the app, False otherwise.
        """
        if app.__dict__.get(method) is not None:
            if app.__dict__.get(method).__module__ != application.Application.__module__:
                return True
        return False

    def run(self):
        """
        This method runs the core module by calling the job method of each application. If the debug flag is set, the job method is called only
        once immediately. If the debug flag is not set, the job method is scheduled to run at the frequency of the application.
        """
        global THREAD_RUN
        self.__load_applications()
        if self.__debug:
            for app in self._applications:
                app.run()
            THREAD_RUN = False
            return True
        else:
            for app in self._applications:
                app.frequency.do(app.run)
                self.logger.debug("Application " + app.__class__.__name__ + " scheduled to run every " + str(
                    app.frequency.interval) + " " + app.frequency.unit + ".")
            while True:
                schedule.run_pending()
                time.sleep(0.5)

    def shutdown(self):
        """
        This method shuts down the core module.
        """
        pass
