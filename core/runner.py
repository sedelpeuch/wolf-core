#! /usr/bin/env python3
from wolf_core import application


class Runner:
    """
    This class is the main class of the core module.
    """

    def __init__(self):
        """
        This is the constructor of the class.
        """
        self._applications = []

    def _load_applications(self):
        """
        This method loads the applications.
        """
        # get all subclasses of Application
        # create an instance of each subclass
        # add the instance to the list of applications
        app = application.Application()
        print(app)
        print(app.instances)

    def _get_all_status(self):
        """
        This method returns the status of all applications.
        """
        pass

    def run(self):
        """
        This method runs the core module.
        """
        print("Hello World!")
        self._load_applications()

    def shutdown(self):
        """
        This method shuts down the core module.
        """
        pass
