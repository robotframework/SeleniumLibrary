import unittest

from mockito import mock, when, unstub

from SeleniumLibrary.locators.windowmanager import WindowManager
from selenium.common.exceptions import WebDriverException

SCRIPT = "return [ window.id, window.name ];"
HANDLE = "17c3dc18-0443-478b-aec6-ed7e2a5da7e1"


class GetCurrentWindowInfoTest(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.driver = mock()
        self.ctx.driver = self.driver
        self.manager = WindowManager(self.ctx)
        self.driver.current_window_handle = HANDLE

    def tearDown(self):
        unstub()

    def mock_window_info(self, id_, name, title, url):
        when(self.driver).execute_script(SCRIPT).thenReturn([id_, name])
        self.driver.title = title
        self.driver.current_url = url

    def test_window_info_values_are_strings(self):
        self.mock_window_info('id', 'name', 'title', 'url')
        info = self.manager._get_current_window_info()
        self.assertEqual(info, (HANDLE, 'id', 'name', 'title', 'url'))

    def test_window_info_values_are_none(self):
        self.mock_window_info(None, None, None, None)
        info = self.manager._get_current_window_info()
        self.assertEqual(
            info, (HANDLE, 'undefined', 'undefined', 'undefined', 'undefined')
        )

    def test_window_info_values_are_empty_strings(self):
        self.mock_window_info('', '', '', '')
        info = self.manager._get_current_window_info()
        self.assertEqual(
            info, (HANDLE, '', 'undefined', 'undefined', 'undefined')
        )

    def test_window_id_is_bool(self):
        self.mock_window_info(True, '', '', '')
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], True)
        self.mock_window_info(False, '', '', '')
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], False)

    def test_window_id_is_web_element(self):
        elem = mock()
        self.mock_window_info(*[elem, '', '', ''])
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], elem)

    def test_window_id_is_container(self):
        self.mock_window_info(*[['1'], '', '', ''])
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], ['1'])

        self.mock_window_info(*[{'a': 2}, '', '', ''])
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], {'a': 2})

    def test_window_id_is_empty_container(self):
        self.mock_window_info(*[[], '', '', ''])
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], [])
        self.mock_window_info(*[{}, '', '', ''])
        info = self.manager._get_current_window_info()
        self.assertEqual(info[1], {})

    def test_no_javascript_support(self):
        when(self.driver).execute_script(SCRIPT).thenRaise(WebDriverException)
        self.driver.title = 'title'
        self.driver.current_url = 'url'
        self.driver.current_window_handle = HANDLE
        info = self.manager._get_current_window_info()
        self.assertEqual(
            info, (HANDLE, 'undefined', 'undefined', 'title', 'url')
        )
