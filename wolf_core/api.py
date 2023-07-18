#! /usr/bin/env python3

"""
This module contains the API interface.
"""
import logging
from abc import ABC

import jsonschema


def type_check(*type_args, **type_kwargs):
    """Decorator that checks the types of the arguments passed to a function.

    :param type_args: Positional arguments representing the types of the function arguments.
    :param type_kwargs: Keyword arguments representing the types of the function keyword arguments.
    :return: Decorator function that performs the type checking.
    """

    def decorator(func):
        """
        This decorator ensures that the arguments passed to the decorated function match the specified types.

        The decorator takes a function as an input and returns a wrapped function.
        The wrapped function performs argument type checking before calling the original function.
        If the argument types do not match the specified types, a TypeError is raised with an appropriate error message.

        The decorator supports both positional arguments and keyword arguments.
        It checks the types of positional arguments based on their order and the types of
        keyword arguments based on their names.

        Note: The decorator assumes that the specified types are imported and available in the decorator's scope.

        :param func: The function to be decorated.
        :return: The decorated function.
        """

        def wrapper(*args, **kwargs):
            """
            Wrap the given function with type checking for positional arguments and keyword arguments.

            :param args: Positional arguments to be passed to the function.
            :param kwargs: Keyword arguments to be passed to the function.

            :return: The return value of the function.

            :raises TypeError: If there are too many or too few positional arguments,
                                or if any argument or keyword argument does not match its expected type.
            """
            args_list = list(args)
            if len(type_args) > 1:
                type_args_list = type_args[0]
            else:
                type_args_list = type_args
            if len(args_list) > len(type_args_list):
                raise TypeError('Too many positional arguments')
            if len(args_list) < len(type_args_list):
                raise TypeError('Too few positional arguments')

            for i, (arg, type_arg) in enumerate(zip(args_list, type_args_list)):
                if not isinstance(arg, type_arg):
                    raise TypeError(f'Argument {i + 1} must be {type_arg}')

            for key, type_value in type_kwargs.items():
                try:
                    value = kwargs[key]
                except KeyError:
                    continue
                if not isinstance(value, type_value):
                    raise TypeError(f'Argument {key} must be {type_value}')

            return func(*args, **kwargs)

        return wrapper

    return decorator


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
    :param ressources: The dictionary of resources and their corresponding methods and parameters. ressources must follow the following schema:
        {
            "ressource_name": {
                "verb": "GET" | "POST" | "PUT" | "DELETE",
                "method": method_name,
                "params": [str, int, float, list, dict, bool, None]
            }
        }
    :type ressources: dict

    """

    instances = []

    def __init__(self, url=None, test_url=None, token=None, test=False, ressources=None):
        self._url = test_url if test else url
        self._token = token
        self.__class__.instances.append(self)
        self.logger = logging.getLogger(__name__)

        # Create the get, post, put and delete classes to store methods
        # Allow to use self.get.method_name() instead of self.get_method_name()
        # Perform type checking and validation schema
        self.get = type("get", (), {})
        self.post = type("post", (), {})
        self.put = type("put", (), {})
        self.delete = type("delete", (), {})

        self.ressources_schema = {
            "verb": {"enum": ["GET", "POST", "PUT", "DELETE"]},
            "method": {"type": "function"},
            "params": {"enum": [str, int, float, list, dict, bool, None]}
        }
        self.ressources = ressources
        for ressource in self.ressources:
            try:
                jsonschema.validate(self.ressources[ressource], self.ressources_schema)
            except jsonschema.exceptions.ValidationError as e:
                self.logger.error(f"Invalid ressource {ressource}: {e.message}")
        self.set_method()

    def set_method(self):
        """
        Set the appropriate method for each resource in the API.

        :return: None
        """
        for resource in self.ressources:
            try:
                method = self.ressources[resource]["method"]
            except KeyError:
                raise ValueError(f"Invalid resource: {resource}")
            type_wrap = self.get if self.ressources[resource]["verb"] == "GET" else self.post if \
                self.ressources[resource]["verb"] == "POST" else self.put if self.ressources[resource][
                                                                                 "verb"] == "PUT" else self.delete
            setattr(type_wrap, resource, method)
            setattr(type_wrap, resource, type_check(self.ressources[resource]["params"])(getattr(type_wrap, resource)))


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
            raise TypeError("`status_code` must be an integer")
        if not isinstance(data, dict):
            raise TypeError("`data` must be a dictionary")
        self._status_code = status_code
        self._data = data

    @property
    def status_code(self):
        """
        This is the status code property.
        """
        return self._status_code

    @property
    def data(self):
        """
        This is the data property.
        """
        return self._data

    def __eq__(self, other):
        if not isinstance(other, RequestResponse):
            return False
        return self.status_code == other.status_code and self.data == other.data
