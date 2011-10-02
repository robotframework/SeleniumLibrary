import unittest
import os
from Selenium2Library.windowselector import WindowSelector
from mockito import *

class WindowSelectorTests(unittest.TestCase):

    def test_select_with_invalid_prefix(self):
        selector = WindowSelector()
        browser = mock()
        with self.assertRaises(ValueError) as context:
            selector.select(browser, "something=test1")
        self.assertEqual(context.exception.message, "Window locator with prefix 'something' is not supported")

    def test_select_with_null_browser(self):
        selector = WindowSelector()
        with self.assertRaises(AssertionError):
            selector.select(None, "name=test1")

    def test_select_by_title(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "title=Title 2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_title_sloppy_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "title= tItLe 2  ")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_title_with_multiple_matches(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2a', 'title': "Title 2", 'url': 'http://localhost/page2a.html' },
            { 'name': 'win2b', 'title': "Title 2", 'url': 'http://localhost/page2b.html' })

        selector.select(browser, "title=Title 2")
        self.assertEqual(browser.get_current_window_handle(), 'win2a')

    def test_select_by_title_no_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        with self.assertRaises(ValueError) as context:
            selector.select(browser, "title=Title -1")
        self.assertEqual(context.exception.message, "Could not find window with title 'Title -1'")

    def test_select_by_name(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_name_sloppy_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name= win2  ")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_name_with_bad_case(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        with self.assertRaises(ValueError) as context:
            selector.select(browser, "name=Win2")
        self.assertEqual(context.exception.message, "Could not find window with name 'Win2'")

    def test_select_by_name_no_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        with self.assertRaises(ValueError) as context:
            selector.select(browser, "name=win-1")
        self.assertEqual(context.exception.message, "Could not find window with name 'win-1'")

    def test_select_by_url(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_url_sloppy_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "url=   http://LOCALHOST/page2.html  ")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_url_with_multiple_matches(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2a', 'title': "Title 2a", 'url': 'http://localhost/page2.html' },
            { 'name': 'win2b', 'title': "Title 2b", 'url': 'http://localhost/page2.html' })

        selector.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.get_current_window_handle(), 'win2a')

    def test_select_by_url_no_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        with self.assertRaises(ValueError) as context:
            selector.select(browser, "url=http://localhost/page-1.html")
        self.assertEqual(context.exception.message, "Could not find window with URL 'http://localhost/page-1.html'")

    def test_select_with_null_locator(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')
        selector.select(browser, None)
        self.assertEqual(browser.get_current_window_handle(), 'win1')

    def test_select_with_null_string_locator(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')
        selector.select(browser, "null")
        self.assertEqual(browser.get_current_window_handle(), 'win1')

    def test_select_with_empty_locator(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')
        selector.select(browser, "")
        self.assertEqual(browser.get_current_window_handle(), 'win1')

    def test_select_by_default_with_name(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_default_with_title(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "Title 2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def test_select_by_default_no_match(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        with self.assertRaises(ValueError) as context:
            selector.select(browser, "win-1")
        self.assertEqual(context.exception.message, "Could not find window with name or title 'win-1'")

    def test_select_with_sloppy_prefix(self):
        selector = WindowSelector()
        browser = self._make_mock_browser(
            { 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html' },
            { 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html' },
            { 'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html' })

        selector.select(browser, "name=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')
        selector.select(browser, "nAmE=win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')
        selector.select(browser, " name  =win2")
        self.assertEqual(browser.get_current_window_handle(), 'win2')

    def _make_mock_browser(self, *window_specs):
        browser = mock()

        windows = {}
        window_handles = []
        first_window = None
        for window_spec in window_specs:
            window_handle = window_spec['name']
            window = mock()
            window.name = window_handle
            window.title = window_spec['title']
            window.url = window_spec['url']

            window_handles.append(window_handle)
            windows[window_handle] = window
            if first_window is None:
                first_window = window

        def switch_to_window(handle):
            if handle is None:
                browser.current_window = first_window
                return
            if handle in window_handles:
                browser.current_window = windows[handle]
                return   
            raise ValueError("No window called " + handle)

        browser.current_window = first_window
        browser.get_current_window_handle = lambda: browser.current_window.name
        browser.get_title = lambda: browser.current_window.title
        browser.get_current_url = lambda: browser.current_window.url
        browser.get_window_handles = lambda: window_handles
        browser.switch_to_window = switch_to_window

        return browser

if __name__ == "__main__":
    unittest.main()
