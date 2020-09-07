import os
import unittest

from robot.errors import DataError
from selenium.webdriver.support.events import AbstractEventListener

from SeleniumLibrary import SeleniumLibrary


class EventFiringWebDriverSeleniumLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_dir = os.path.dirname(os.path.abspath(__file__))
        cls.listener = os.path.join(cls.root_dir, "MyListener.py")

    def test_import_event_firing_webdriver(self):
        sl = SeleniumLibrary(event_firing_webdriver=self.listener)
        isinstance(sl.event_firing_webdriver, AbstractEventListener)

    def test_no_event_firing_webdriver(self):
        sl = SeleniumLibrary()
        self.assertIsNone(sl.event_firing_webdriver)

    def test_import_event_firing_webdriver_error_module(self):
        listener = os.path.join(self.root_dir, "MyListenerWrongName.py")
        with self.assertRaises(DataError):
            SeleniumLibrary(event_firing_webdriver=listener)

    def test_too_many_event_firing_webdriver(self):
        with self.assertRaises(ValueError):
            SeleniumLibrary(event_firing_webdriver=f"{self.listener},{self.listener}")
