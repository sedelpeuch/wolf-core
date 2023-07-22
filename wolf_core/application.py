#! /usr/bin/env python3
"""
This module contains the Application Interface of the core module. All applications must implement this interface if they want to be run by the runner.
"""
import logging
import threading
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import schedule

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
    Application Interface of the core module. All applications must implement this interface if they want to be run by the runner.

    An application can use one or more APIs to work. The APIs are stored in a list. The frequency of the application is stored in a schedule.Job.

    The job method is the method that is called by the runner. It must be implemented by the application. This method must contain all the work of
    the application.

    :ivar _apis: The list of APIs used by the application.
    :see: :class:`api.API`
    :type _apis: List[api.API]

    :ivar frequency: The frequency of the application.
    :see: :class:`schedule.Job`
    :type frequency: schedule.Job
    """

    def __init__(self):
        self._apis: List[api.API] = api.API.instances
        self.frequency: schedule.Job = schedule.every().day
        self.logger = logging.getLogger(__name__)
        self.status_lock = threading.Lock()
        self.__status = Status.WAITING
        self.message_lock = threading.Lock()
        self.__message = "OK"
        self.last_execution_lock = threading.Lock()
        self.__last_execution = Status.NEVER

        self.app_lock = threading.Lock()
        self.__debug = False

    @property
    def status(self) -> Status:
        """
        This property returns the status of the application.
        """
        return self.__status

    @status.setter
    def status(self, value: Status):
        """
        This property sets the status of the application.
        """
        if not isinstance(value, Status):
            raise TypeError("The status must be a Status.")
        with self.status_lock:
            self.__status = value

    @property
    def message(self) -> str:
        """
        This property returns the message of the application.
        """
        return self.__message

    @message.setter
    def message(self, value: str):
        """
        This property sets the message of the application.
        """
        if not isinstance(value, str):
            raise TypeError("The message must be a string.")
        with self.message_lock:
            self.__message = value

    @property
    def debug(self) -> bool:
        """
        This property returns the debug mode of the application.
        """
        return self.__debug

    @debug.setter
    def debug(self, value: bool):
        """
        This property sets the debug mode of the application.
        """
        if not isinstance(value, bool):
            raise TypeError("The debug mode must be a boolean.")
        self.__debug = value

    @property
    def last_execution(self) -> Status:
        """
        This property returns the last execution of the application.
        """
        return self.__last_execution

    @last_execution.setter
    def last_execution(self, value: Status):
        """
        This property sets the last execution of the application.
        """
        if not isinstance(value, Status):
            raise TypeError("The last execution must be a Status.")
        with self.last_execution_lock:
            self.__last_execution = value

    def api(self, name):
        """
        This property returns the API with the given name.
        """
        for api in self._apis:
            if api.__class__.__name__ == name:
                return api
        raise ValueError("The API with name {} does not exist.".format(name))

    def run(self):
        """
        This method is called by the runner. It loads the APIs, sets the frequency and schedules the job.

        This method must not be overridden.
        """
        # get unique int to identify the run
        self.app_lock.acquire()
        self.status = Status.RUNNING
        try:
            self.job()
        except Exception as e:
            self.status = Status.ERROR
            self.message = str(e)
            self.logger.error("An error occurred while running the application: {} - {}".format(type(e).__name__, e))
            if self.__debug:
                raise e
        finally:
            self.last_execution = self.status
        self.status = Status.WAITING
        self.app_lock.release()
        time.sleep(1)

    @abstractmethod
    def job(self):
        """
        This method is called by the runner. It must contain all the work of the application.
        It must update the status of the application (RUNNING, ERROR, SUCCESS).
        """
        pass

    def shutdown(self):
        """
        This method is called by the runner when the application is stopped. It must stop all the work of the application.
        """
        pass
