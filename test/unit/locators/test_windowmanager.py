import unittest
import os
from Selenium2Library.locators import WindowManager
from mockito import *
import uuid
from selenium.common.exceptions import NoSuchWindowException

class WindowManagerTests(unittest.TestCase):

    def test_select_with_invalid_prefix(self):
        manager = WindowManager()
        browser = mock()
        try:
            self.assertRaises(ValueError, manager.select, browser, "something=test1")
        except ValueError as e:
            self.assertEqual(e.message, "Window locator with prefix 'something' is not supported")

    def test_select_with_null_browser(self):
        manager = WindowManager()
        self.assertRaises(AssertionError,
            manager.select, None, "name=test1")

    def test_select_by_title(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "title=Title 2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_title_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "title= tItLe 2  ")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_title_with_multiple_matches(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2a', 'title': "Title 2", 'url': 'http://localhost/page2a.html' },
            { 'name': 'win2b', 'title': "Title 2", 'url': 'http://localhost/page2b.html' })

        manager.select(browser, "title=Title 2")
        self.assertEqual(browser.current_window.name, 'win2a')

    def test_select_by_title_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        try:
            self.assertRaises(ValueError, manager.select, browser, "title=Title -1")
        except ValueError as e:
            self.assertEqual(e.message, "Unable to locate window with title 'Title -1'")

    def test_select_by_name(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_name_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name= win2  ")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_name_with_bad_case(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=Win2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_name_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        try:
            self.assertRaises(ValueError, manager.select, browser, "name=win-1")
        except ValueError as e:
            self.assertEqual(e.message, "Unable to locate window with name 'win-1'")

    def test_select_by_url(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_url_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "url=   http://LOCALHOST/page2.html  ")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_url_with_multiple_matches(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2a', 'title': "Title 2a", 'url': 'http://localhost/page2.html' },
            { 'name': 'win2b', 'title': "Title 2b", 'url': 'http://localhost/page2.html' })

        manager.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.current_window.name, 'win2a')

    def test_select_by_url_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        try:
            self.assertRaises(ValueError, manager.select, browser, "url=http://localhost/page-1.html")
        except ValueError as e:
            self.assertEqual(e.message, "Unable to locate window with URL 'http://localhost/page-1.html'")

    def test_select_with_null_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, None)
        self.assertEqual(browser.current_window.name, 'win1')

    def test_select_with_null_string_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "null")
        self.assertEqual(browser.current_window.name, 'win1')

    def test_select_with_empty_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "")
        self.assertEqual(browser.current_window.name, 'win1')

    def test_select_with_main_constant_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "main")
        self.assertEqual(browser.current_window.name, 'win1')

    def test_select_by_default_with_name(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "win2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_default_with_title(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "Title 2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_select_by_default_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        try:
            self.assertRaises(ValueError, manager.select, browser, "win-1")
        except ValueError as e:
            self.assertEqual(context.exception.message, "Unable to locate window with name or title 'win-1'")

    def test_select_with_sloppy_prefix(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "nAmE=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, " name  =win2")
        self.assertEqual(browser.current_window.name, 'win2')

    def test_get_window_ids(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'id': 'win1', 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'id': 'win2', 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        self.assertEqual(
            manager.get_window_ids(browser),
            [ 'win1', 'win2', 'undefined' ])

    def test_get_window_names(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        self.assertEqual(
            manager.get_window_names(browser),
            [ 'win1', 'win2', 'win3' ])

    def test_get_window_titles(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        self.assertEqual(
            manager.get_window_titles(browser),
            [ 'Title 1', 'Title 2', 'Title 3' ])

    def _make_mock_browser(self, *window_specs):
        browser = mock()

        windows = []
        window_handles = []
        first_window = None
        for window_spec in window_specs:
            window = mock()
            window.handle = uuid.uuid4().hex
            window.id = window_spec.get('id')
            if window.id is None:
                window.id = 'undefined'
            window.name = window_spec['name']
            window.title = window_spec['title']
            window.url = window_spec['url']

            windows.append(window)
            window_handles.append(window.handle)

            if first_window is None:
                first_window = window

        def switch_to_window(handle_or_name):
            if handle_or_name == '':
                browser.current_window = first_window
                return
            for window in windows:
                if window.handle == handle_or_name or window.name == handle_or_name:
                    browser.current_window = window
                    return
            raise NoSuchWindowException(u'Unable to locate window "' + handle_or_name + '"')

        browser.current_window = first_window
        browser.get_current_window_handle = lambda: browser.current_window.handle
        browser.get_title = lambda: browser.current_window.title
        browser.get_current_url = lambda: browser.current_window.url
        browser.get_window_handles = lambda: window_handles
        browser.switch_to_window = switch_to_window
        browser.get_current_window_info = lambda: (
            browser.current_window.handle, browser.current_window.id, browser.current_window.name,
            browser.current_window.title, browser.current_window.url)

        return browser
