import unittest
import uuid

from mockito import mock, unstub

from Selenium2Library.locators import WindowManager


class WindowManagerTests(unittest.TestCase):

    def test_select_with_invalid_prefix(self):
        manager = WindowManager()
        browser = mock()
        with self.assertRaises(ValueError) as err:
            manager.select(browser, "something=test1")
            self.assertEqual(
                str(err),
                "Window locator with prefix 'something' is not supported"
            )
        unstub()

    def test_select_with_null_browser(self):
        manager = WindowManager()
        with self.assertRaises(AssertionError):
            manager.select(None, "name=test1")
        unstub()

    def test_select_by_title(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "title=Title 2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_title_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "title= tItLe 2  ")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_title_with_multiple_matches(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2", 'url': 'http://localhost/page2a.html'},
            {'name': 'win2b', 'title': "Title 2", 'url': 'http://localhost/page2b.html'})

        manager.select(browser, "title=Title 2")
        self.assertEqual(browser.current_window.name, 'win2a')
        unstub()

    def test_select_by_title_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        with self.assertRaises(ValueError) as err:
            manager.select(browser, "title=Title -1")
            self.assertEqual(
                str(err),
                "Unable to locate window with title 'Title -1'"
            )
        unstub()

    def test_select_by_name(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_name_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name= win2  ")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_name_with_bad_case(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=Win2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_name_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        with self.assertRaises(ValueError) as err:
            manager.select(browser, "name=win-1")
            self.assertEqual(str(err), "Unable to locate window with name 'win-1'")
        unstub()

    def test_select_by_url(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_url_sloppy_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "url=   http://LOCALHOST/page2.html  ")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_url_with_multiple_matches(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2a", 'url': 'http://localhost/page2.html'},
            {'name': 'win2b', 'title': "Title 2b", 'url': 'http://localhost/page2.html'})

        manager.select(browser, "url=http://localhost/page2.html")
        self.assertEqual(browser.current_window.name, 'win2a')
        unstub()

    def test_select_by_url_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )

        with self.assertRaises(ValueError) as err:
            manager.select(browser, "url=http://localhost/page-1.html")
            self.assertEqual(
                str(err),
                (
                    "Unable to locate window with URL "
                    "'http://localhost/page-1.html'"
                )
            )
        unstub()

    def test_select_with_null_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, None)
        self.assertEqual(browser.current_window.name, 'win1')
        unstub()

    def test_select_with_null_string_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "null")
        self.assertEqual(browser.current_window.name, 'win1')
        unstub()

    def test_select_with_empty_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "")
        self.assertEqual(browser.current_window.name, 'win1')
        unstub()

    def test_select_with_main_constant_locator(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "main")
        self.assertEqual(browser.current_window.name, 'win1')
        unstub()

    def test_select_by_default_with_name(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "win2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_default_with_title(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "Title 2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_select_by_default_no_match(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})
        self.assertRaises(ValueError, manager.select, browser, "win-1")
        unstub()

    def test_select_with_sloppy_prefix(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        manager.select(browser, "name=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, "nAmE=win2")
        self.assertEqual(browser.current_window.name, 'win2')
        manager.select(browser, " name  =win2")
        self.assertEqual(browser.current_window.name, 'win2')
        unstub()

    def test_get_window_ids(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'id': 'win_id1', 'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'id': 'win_id2', 'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        self.assertEqual(
            manager.get_window_ids(browser),
            ['win_id1', 'win_id2', 'undefined']
        )
        unstub()

    def test_get_window_names(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        self.assertEqual(
            manager.get_window_names(browser),
            ['win1', 'win2', 'win3']
        )
        unstub()

    def test_get_window_titles(self):
        manager = WindowManager()
        browser = self._make_mock_browser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'})

        self.assertEqual(
            manager.get_window_titles(browser),
            ['Title 1', 'Title 2', 'Title 3']
        )
        unstub()

    def _make_mock_browser(self, *window_specs):
        browser = mock()
        current_window = mock()
        browser.window_handles = []
        browser.window_handles = []
        window_infos = {}
        for window_spec in window_specs:
            handle = uuid.uuid4().hex
            browser.window_handles.append(handle)
            id_ = window_spec.get('id')
            if not id_:
                id_ = 'undefined'
            window_info = [
                id_,
                window_spec.get('name'),
                window_spec.get('title'),
                window_spec.get('url')
            ]
            window_infos[handle] = window_info

        def switch_to_window(handle_):
            if handle_ in browser.window_handles:
                browser.session_id = handle_
                current_window.name = window_infos[handle_][1]
                browser.current_window = current_window
        browser.switch_to_window = switch_to_window

        def execute_script(script):
            handle_ = browser.session_id
            if handle_ in browser.window_handles:
                return window_infos[handle_]
        browser.execute_script = execute_script
        return browser
