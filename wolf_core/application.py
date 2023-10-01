#! /usr/bin/env python3
"""
This module contains the Application Interface of the core module.
All applications must implement this interface if they want to be run by the runner.
"""
import datetime
import logging
import os
import threading
import time
import uuid
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from wolf_core import api


class Status(Enum):
    """
    This class is an enum for the status of an application.
    """

    NEVER = 0
    RUNNING = 1
    WAITING = 2
    ERROR = 3
    SUCCESS = 4

    def __str__(self):
        """
        This method returns the name of the status.
        :return: The name of the status.
        """
        return self.name


class Application(ABC):
    """
    Application Interface of the core module.
    All applications must implement this interface if they want to be run by the runner.

    An application can use one or more APIs to work.
    The APIs are stored in a list.
    The frequency of the application is stored in a schedule.Job.

    The job method is the method that is called by the runner.
    It must be implemented by the application.
    This method must contain all the work of
    the application.

    :ivar _apis: The list of APIs used by the application.
    :see: :class:`api.API`
    :type _apis: List[api.API]

    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def __init__(self):

        self._apis: List[api.API] = api.API.instances

        self.app_lock = threading.Lock()
        self.__debug = False
        self.__setup_logger()
        self.__load_apis()

    def __setup_logger(self):
        """
        This method sets up the logger.
        It creates a file handler and a console handler.
        The file handler logs all messages with level WARNING.

        :return: None
        """
        self.logger.handlers = []
        log_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        file_path = os.path.expanduser("~/.cache/wolf")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        try:
            os.makedirs(os.path.join(file_path, 'log'), exist_ok=True)
            file_handler = logging.FileHandler(file_path + "/log" + '/wolf_core_' + log_name + '.log')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except PermissionError:
            self.logger.error("Could not create log file. Please check permissions.")

        time.sleep(1)

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

    @property
    def debug(self) -> bool:
        """
        This property returns the debug mode of the application.

        :return: The debug mode of the application as a boolean value.
        """
        return self.__debug

    @debug.setter
    def debug(self, value: bool):
        """
        This method sets the debug mode of the application.

        :param value: A boolean value indicating whether debug mode should be enabled or disabled.
        :return: None
        """
        if not isinstance(value, bool):
            raise TypeError("The debug mode must be a boolean.")
        self.__debug = value

    def api(self, name):
        """
        This method returns the API with the given name.

        :param name: The name of the API.
        :return: The API object corresponding to the given name.
        :raises ValueError: If the API with the given name does not exist.
        """
        for api_object in self._apis:
            if api_object.__class__.__name__ == name:
                return api_object
        raise ValueError("The API with name {} does not exist.".format(name))

    @abstractmethod
    def job(self) -> Status:
        """
        The runner calls this method.
        It must contain all the work of the application.
        It must update the status of the application (RUNNING, ERROR, SUCCESS).

        :return: None
        """
        pass

