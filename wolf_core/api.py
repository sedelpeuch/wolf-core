#! /usr/bin/env python3

"""
This module contains the API interface.
"""
import logging
from abc import ABC, abstractmethod


class API(ABC):
    """
    This class is the main class of the core module.

    :param url: The main url for the API.
    :type url: str
    :param test_url: The test url for the API.
    :type test_url: str
    :param token: The token used for authentication.
    :type token: str
    :param test: Optional flag to indicate whether to use the test url or the main url. Defaults to False.
    :type test: bool, optional
    """

    instances = []

    def __init__(self, url=None, test_url=None, token=None, test=False):
        """
        This is the constructor of the class.
        """
        self._url = test_url if test else url
        self._token = token
        self.__class__.instances.append(self)
        self.logger = logging.getLogger(__name__)

    @abstractmethod
    def get(self, resource, params=None):
        """
        This method is intended to submit GET requests to the API.

        :param resource: The specific resource in the API that the GET request is made to.
        :type resource: str
        """
        pass

    @abstractmethod
    def post(self, resource, data):
        """
        This method is intended to submit POST requests to the API.

        :param resource: The specific resource in the API that the POST request is made to.
        :type resource: str
        :param data: The data to send in the POST request.
        :type data: dict
        """
        pass

    @abstractmethod
    def put(self, resource, data):
        """
        This method is intended to submit PUT requests to the API.

        :param resource: The specific resource in the API that the PUT request is made to.
        :type resource: str
        :param data: The data to send in the PUT request.
        :type data: dict
        """
        pass

    @abstractmethod
    def delete(self, resource):
        """
        This method is intended to submit DELETE requests to the API.

        :param resource: The specific resource in the API that the DELETE request is made to.
        :type resource: str
        """
        pass


class RequestResponse:
    """
    This class is used to store the response from an API request.

    :param status_code: The status code of the response.
    :type status_code: int
    :param data: The data in the response.
    :type data: dict
    """

    def __init__(self, status_code, data):
        """
        This is the constructor of the class.
        """
        if not isinstance(status_code, int):
            raise ValueError("`status_code` must be an integer")
        if not isinstance(data, dict):
            raise ValueError("`data` must be a dictionary")
        self.__status_code = status_code
        self.__data = data

    @property
    def status_code(self):
        """
        This is the status code property.
        """
        return self.__status_code

    @property
    def data(self):
        """
        This is the data property.
        """
        return self.__data
