import unittest

from mockito import mock, when, unstub

from Selenium2Library.locators.windowmanager import WindowManager
from selenium.common.exceptions import WebDriverException

SCRIPT = "return [ window.id, window.name ];"
HANDLE = "17c3dc18-0443-478b-aec6-ed7e2a5da7e1"


class GetCurrentWindowInfoTest(unittest.TestCase):

    def mock_window_info(self, driver, id_, name, title, url):
        when(driver).execute_script(SCRIPT).thenReturn([id_, name])
        driver.title = title
        driver.current_url = url

    def test_window_info_values_are_strings(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, 'id', 'name', 'title', 'url')
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info, (HANDLE, 'id', 'name', 'title', 'url'))
        unstub()

    def test_window_info_values_are_none(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, None, None, None, None)
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(
            info, (HANDLE, 'undefined', 'undefined', 'undefined', 'undefined')
        )
        unstub()

    def test_window_info_values_are_empty_strings(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, '', '', '', '')
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(
            info, (HANDLE, '', 'undefined', 'undefined', 'undefined')
        )
        unstub()

    def test_window_id_is_bool(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, True, '', '', '')
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], True)
        self.mock_window_info(driver, False, '', '', '')
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], False)
        unstub()

    def test_window_id_is_web_element(self):
        manager = WindowManager()
        driver = mock()
        elem = mock()
        self.mock_window_info(driver, *[elem, '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], elem)
        unstub()

    def test_window_id_is_container(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, *[['1'], '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], ['1'])

        self.mock_window_info(driver, *[{'a': 2}, '', '', ''])
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], {'a': 2})
        unstub()

    def test_window_id_is_empty_container(self):
        manager = WindowManager()
        driver = mock()
        self.mock_window_info(driver, *[[], '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], [])
        self.mock_window_info(driver, *[{}, '', '', ''])
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], {})
        unstub()

    def test_no_javascript_support(self):
        manager = WindowManager()
        driver = mock()
        elem = mock()
        when(driver).execute_script(SCRIPT).thenRaise(WebDriverException)
        driver.title = 'title'
        driver.current_url = 'url'
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(
            info, (HANDLE, 'undefined', 'undefined', 'title', 'url')
        )
        unstub()
