import unittest

from mockito import mock, when, unstub

from Selenium2Library.locators import WindowManager

SCRIPT = "return [ window.id, window.name, document.title, document.URL ];"
HANDLE = "17c3dc18-0443-478b-aec6-ed7e2a5da7e1"


class GetCurrentWindowInfoTest(unittest.TestCase):

    def test_window_info_values_are_strings(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn(
            ['id', 'name', 'title', 'url']
        )
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info, (HANDLE, 'id', 'name', 'title', 'url'))
        unstub()

    def test_window_info_values_are_none(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn([None] * 4)
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(
            info, (HANDLE, 'undefined', 'undefined', 'undefined', 'undefined')
        )
        unstub()

    def test_window_info_values_are_empty_strings(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn([''] * 4)
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(
            info, (HANDLE, '', 'undefined', 'undefined', 'undefined')
        )
        unstub()

    def test_window_id_is_bool(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn(
            [True, '', '', '']).thenReturn([False, '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], True)
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], False)
        unstub()

    def test_window_id_is_web_element(self):
        manager = WindowManager()
        driver = mock()
        elem = mock()
        when(driver).execute_script(SCRIPT).thenReturn([elem, '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], elem)
        unstub()

    def test_window_id_is_container(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn(
            [['1'], '', '', '']).thenReturn([{'a': 2}, '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], ['1'])
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], {'a': 2})
        unstub()

    def test_window_id_is_empty_container(self):
        manager = WindowManager()
        driver = mock()
        when(driver).execute_script(SCRIPT).thenReturn(
            [[], '', '', '']).thenReturn([{}, '', '', ''])
        driver.current_window_handle = HANDLE
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], [])
        info = manager._get_current_window_info(driver)
        self.assertEqual(info[1], {})
        unstub()
