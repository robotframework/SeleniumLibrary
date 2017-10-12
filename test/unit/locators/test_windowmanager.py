import unittest
import uuid

from mockito import mock

from SeleniumLibrary.locators import WindowManager


class WindowManagerTests(unittest.TestCase):

    def test_select_with_invalid_prefix(self):
        manager = WindowManagerWithMockBrowser()
        with self.assertRaises(ValueError) as err:
            manager.select("something=test1")
            self.assertEqual(
                str(err),
                "Window locator with prefix 'something' is not supported"
            )

    def test_select_by_title(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("title=Title 2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_title_sloppy_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("title= tItLe 2  ")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_title_with_multiple_matches(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2", 'url': 'http://localhost/page2a.html'},
            {'name': 'win2b', 'title': "Title 2", 'url': 'http://localhost/page2b.html'}
        )
        manager.select("title=Title 2")
        self.assertEqual(manager.browser.current_window.name, 'win2a')

    def test_select_by_title_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(ValueError) as err:
            manager.select("title=Title -1")
            self.assertEqual(str(err),
                             "Unable to locate window with title 'Title -1'")

    def test_select_by_name(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_name_sloppy_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name= win2  ")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_name_with_bad_case(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=Win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_name_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(ValueError) as err:
            manager.select("name=win-1")
            self.assertEqual(str(err), "Unable to locate window with name 'win-1'")

    def test_select_by_url(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("url=http://localhost/page2.html")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_url_sloppy_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("url=   http://LOCALHOST/page2.html  ")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_url_with_multiple_matches(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2a", 'url': 'http://localhost/page2.html'},
            {'name': 'win2b', 'title': "Title 2b", 'url': 'http://localhost/page2.html'}
        )
        manager.select("url=http://localhost/page2.html")
        self.assertEqual(manager.browser.current_window.name, 'win2a')

    def test_select_by_url_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(ValueError) as err:
            manager.select("url=http://localhost/page-1.html")
            self.assertEqual(str(err), "Unable to locate window with URL "
                                       "'http://localhost/page-1.html'")

    def test_select_with_null_locator(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select(None)
        self.assertEqual(manager.browser.current_window.name, 'win1')

    def test_select_with_null_string_locator(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select("null")
        self.assertEqual(manager.browser.current_window.name, 'win1')

    def test_select_with_empty_locator(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select("")
        self.assertEqual(manager.browser.current_window.name, 'win1')

    def test_select_with_main_constant_locator(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select("main")
        self.assertEqual(manager.browser.current_window.name, 'win1')

    def test_select_by_default_with_name(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_default_with_title(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("Title 2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_select_by_default_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        self.assertRaises(ValueError, manager.select, "win-1")

    def test_select_with_sloppy_prefix(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select("nAmE=win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')
        manager.select(" name  =win2")
        self.assertEqual(manager.browser.current_window.name, 'win2')

    def test_get_window_infos(self):
        manager = WindowManagerWithMockBrowser(
            {'id': 'id1', 'name': 'win1', 'title': "Title 1", 'url': 'http://url.1'},
            {'id': 'id2', 'name': 'win2', 'title': "Title 2", 'url': 'http://url.2'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://url.3'}
        )
        self.assertEqual([info.id for info in manager.get_window_infos()],
                         ['id1', 'id2', 'undefined'])
        self.assertEqual([info.name for info in manager.get_window_infos()],
                         ['win1', 'win2', 'win3'])
        self.assertEqual([info.title for info in manager.get_window_infos()],
                         ['Title 1', 'Title 2', 'Title 3'])
        self.assertEqual([info.url for info in manager.get_window_infos()],
                         ['http://url.1', 'http://url.2', 'http://url.3'])


class WindowManagerWithMockBrowser(WindowManager):

    def __init__(self, *window_specs):
        ctx = mock()
        ctx.browser = self._make_mock_browser(*window_specs)
        WindowManager.__init__(self, ctx)

    def _make_mock_browser(self, *window_specs):
        browser = mock()
        current_window = mock()
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

        def window(handle_):
            if handle_ in browser.window_handles:
                browser.session_id = handle_
                current_window.name = window_infos[handle_][1]
                browser.current_window = current_window
                browser.title = window_infos[handle_][2]
                browser.current_url = window_infos[handle_][3]

        switch_to = mock()
        switch_to.window = window
        browser.switch_to = switch_to

        def execute_script(script):
            handle_ = browser.session_id
            if handle_ in browser.window_handles:
                return window_infos[handle_][:2]

        browser.execute_script = execute_script
        return browser
