#! /usr/bin/env python3

"""
This module contains the API interface.
"""

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

    def __init__(self, url, test_url, token, test=False):
        """
        This is the constructor of the class.
        """
        self._url = test_url if test else url
        self._token = token

    @abstractmethod
    def get(self, resource):
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
