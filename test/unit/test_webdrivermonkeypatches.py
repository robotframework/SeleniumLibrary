import unittest
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from mockito import *

SCRIPT = "return [ window.id, window.name, document.title, document.URL ];"
HANDLE = "17c3dc18-0443-478b-aec6-ed7e2a5da7e1"


class MockWebDriver(RemoteWebDriver):
    def __init__(self):
        pass

    current_window_handle = HANDLE


class WebDriverMonkeyPatchesTests(unittest.TestCase):

    def test_window_info_values_are_strings(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn(['id', 'name', 'title', 'url'])
        info = driver.get_current_window_info()
        self.assertEqual(info, (HANDLE, 'id', 'name', 'title', 'url'))

    def test_window_info_values_are_empty_strings(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn([''] * 4)
        info = driver.get_current_window_info()
        self.assertEqual(info, (HANDLE, '', 'undefined', 'undefined', 'undefined'))

    def test_window_info_values_are_none(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn([None] * 4)
        info = driver.get_current_window_info()
        self.assertEqual(info, (HANDLE, 'undefined', 'undefined', 'undefined', 'undefined'))

    def test_window_id_is_bool(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn([True, '', '', '']).thenReturn([False, '', '', ''])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], True)
        info = driver.get_current_window_info()
        self.assertEqual(info[1], False)

    def test_window_id_is_web_element(self):
        driver = MockWebDriver()
        elem = WebElement(None, '052b083c-0d6e-45ca-bda6-73ca13c42561')
        when(driver).execute_script(SCRIPT).thenReturn([elem, '', '', ''])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], elem)

    def test_window_id_is_container(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn([['1'], '', '', '']).thenReturn([{'a': 2}, '', '', ''])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], ['1'])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], {'a': 2})

    def test_window_id_is_empty_container(self):
        driver = MockWebDriver()
        when(driver).execute_script(SCRIPT).thenReturn([[], '', '', '']).thenReturn([{}, '', '', ''])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], [])
        info = driver.get_current_window_info()
        self.assertEqual(info[1], {})
