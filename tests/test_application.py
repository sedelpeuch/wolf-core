import time
import unittest

from wolf_core import application


class TestApplication(application.Application):
    def __init__(self):
        super().__init__()

    def job(self):
        time.sleep(1)
        self.status = application.Status.SUCCESS



class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.test_application = TestApplication()

    def test_initialisation(self):
        self.assertEqual(self.test_application._apis, [])
        self.assertEqual(self.test_application.status, application.Status.WAITING)

    def test_status_property(self):
        self.assertEqual(self.test_application.status, application.Status.WAITING)

        # Check if the status is set to RUNNING normally not (property)
        self.test_application.__status = application.Status.RUNNING
        self.assertEqual(self.test_application.status, application.Status.WAITING)

    def test_status_setter(self):
        self.test_application.status = application.Status.WAITING
        self.assertEqual(self.test_application.status, application.Status.WAITING)

        with self.assertRaises(TypeError):
            self.test_application.status = "TEST"

    def test_empty_run(self):
        self.test_application.run()
        self.assertEqual(self.test_application.status, application.Status.SUCCESS)


if __name__ == '__main__':
    unittest.main()
