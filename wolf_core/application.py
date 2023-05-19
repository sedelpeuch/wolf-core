#! /usr/bin/env python3
"""
This module contains the Application Interface of the core module. All applications must implement this interface if they want to be run by the
runner.
"""

from abc import ABC, abstractmethod
from typing import List

import schedule
from wolf_core import api


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

    @abstractmethod
    def job(self):
        """
        This method is called by the runner. It must contain all the work of the application.
        """
        pass
