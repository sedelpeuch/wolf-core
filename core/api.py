#! /usr/bin/env python3


from abc import ABC, abstractmethod


class API(ABC):
    """
    This class is the main class of the core module.
    """

    def __init__(self):
        """
        This is the constructor of the class.
        """
        self._url: str = ""
        self._token: str = ""

    @abstractmethod
    def get(self, resource):
        """
        This method runs the core module.
        """
        pass

    @abstractmethod
    def post(self, resource, data):
        """
        This method runs the core module.
        """
        pass
