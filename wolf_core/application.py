#! /usr/bin/env python3
"""
This module contains the Application Interface of the core module. All applications must implement this interface if they want to be run by the
runner.
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import List

import schedule

from wolf_core import api


class Status(Enum):
    """
    This class is an enum for the status of an application.
    """
    WAITING = 2
    RUNNING = 1
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

    :ivar _frequency: The frequency of the application.
    :see: :class:`schedule.Job`
    :type _frequency: schedule.Job
    """

    def __init__(self):
        self._apis: List[api.API] = []
        self.frequency: schedule.Job = schedule.every(1).day
        self.logger = None
        self._status = Status.WAITING

    @property
    def status(self) -> Status:
        """
        This property returns the status of the application.
        """
        return self._status

    @status.setter
    def status(self, value: Status):
        """
        This property sets the status of the application.
        """
        if not isinstance(value, Status):
            raise TypeError("The status must be a Status.")
        self._status = value

    def run(self):
        """
        This method is called by the runner. It loads the APIs, sets the frequency and schedules the job.
        """
        self.logger.debug("Application " + self.__class__.__name__ + " started.")
        self.job()
        self.logger.warning("Application " + self.__class__.__name__ + " finished with status " + str(self._status))

    @abstractmethod
    def job(self):
        """
        This method is called by the runner. It must contain all the work of the application.
        It must update the status of the application (RUNNING, ERROR, SUCCESS).
        """
        pass
