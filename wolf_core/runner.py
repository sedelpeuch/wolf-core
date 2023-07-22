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

from wolf_core import application, api, grafana_logger


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
        self._apis = []
        self._applications = []

        self.__test = test
        self.__debug = debug

        self.__status = {}
        self.__last_status = {}
        self.__message = {}
        self.__last_execution = {}

        self.thread_run = threading.Event()
        self.thread_run.set()
        self.thread_pool = []

        self.__setup_logger()
        self.__grafana_logger = grafana_logger.GrafanaLogger(self.logger)

    def __setup_logger(self):
        """
        This method sets up the logger. It creates a file handler and a console handler. The file handler logs all messages with level WARNING.
        :return: None
        """
        self.logger.handlers = []
        log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.dirname(os.path.realpath(__file__))
        os.makedirs(os.path.join(file_path, 'log'), exist_ok=True)
        try:
            file_handler = logging.FileHandler(file_path + "/log" + '/wolf_core_' + log_name + '.log')
        except PermissionError:
            raise PermissionError("Could not create log file. Please check permissions.")
        file_handler.setLevel(logging.DEBUG)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        time.sleep(1)

    def __load_applications(self):
        """
        This method loads the applications by creating an instance of each application.
        The instances are reset if there are existing applications.
        It also sets the log of each application.

        :return: None
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
            if self.__debug:
                app.debug = True

    def __load_apis(self):
        """
        This method loads the APIs by creating an instance of each API.
        The instances are stored in the `_apis` list attribute.
        It also sets the logs of each API.

        :return: None
        """
        if len(self._apis) != 0:
            self.logger.debug("Deleting old APIs.")
            self._apis = []
        for a in api.API.__subclasses__():
            self._apis.append(a())
            self.logger.debug("API " + a.__name__ + " loaded.")
        for a in self._apis:
            a.logger = self.logger

    def __get_status(self, app):
        """
        This method gets the status of all applications and stores it in the _status dictionary.
        """
        app.status_lock.acquire()
        self.__status[app.__class__.__name__] = app.status
        app.status_lock.release()
        app.message_lock.acquire()
        self.__message[app.__class__.__name__] = app.message
        app.message_lock.release()
        app.last_execution_lock.acquire()
        self.__last_execution[app.__class__.__name__] = app.last_execution
        app.last_execution_lock.release()

    def __status_thread(self, app):
        """
        This method is the thread that is run by the status method. It gets the status of all applications and prints it
        """
        while self.thread_run.is_set():
            self.__get_status(app)
            if app.app_lock.locked():
                continue
            if self.__status[app.__class__.__name__] is application.Status.ERROR:
                self.logger.error("Application " + app.__class__.__name__ + " failed.")
            elif self.__status[app.__class__.__name__] is application.Status.SUCCESS:
                self.logger.warning("Application " + app.__class__.__name__ + " succeeded.")
            self.__grafana_logger.post(app.__class__.__name__,
                                       self.__last_execution[app.__class__.__name__].value,
                                       self.__message[app.__class__.__name__])


    @staticmethod
    def is_method_overridden(app, method):
        """
        This method checks if the given method is overridden in any of the applications.

        :param app: The application to check.
        :param method: The method to check.
        :return: True if the app overrides the method, False otherwise.
        """
        if app.__dict__.get(method) is not None:
            if app.__dict__.get(method).__module__ != application.Application.__module__:
                return True
        return False

    def run(self):
        """
        Runs the core module by calling the job method of each application. If the debug flag is set, the job method is called only
        once immediately. If the debug flag is not set, the job method is scheduled to run at the frequency of the application.

        :return: None
        """
        self.__load_apis()
        self.__load_applications()
        if self.__debug:
            for app in self._applications:
                app.run()
            self.thread_run.clear()
            return True
        else:
            for app in self._applications:
                app.frequency.do(app.run)
                self.logger.debug("Application " + app.__class__.__name__ + " scheduled to run every " + str(
                    app.frequency.interval) + " " + app.frequency.unit + ".")
            for app in self._applications:
                self.thread_pool.append(threading.Thread(target=self.__status_thread, args=(app,)))
            for thread in self.thread_pool:
                thread.start()
            while True:
                try:
                    schedule.run_pending()
                    time.sleep(0.5)
                except KeyboardInterrupt:
                    self.shutdown()
                    return True

    def shutdown(self):
        """
        This method shuts down the core module.
        """
        self.thread_run.clear()
        schedule.clear()
        for app in self._applications:
            app.shutdown()
        for thread in self.thread_pool:
            thread.join()
        self.logger.debug("Shutting down.")
