import unittest
import uuid

from mockito import mock, when
from robot.api import logger

from SeleniumLibrary.errors import WindowNotFound
from SeleniumLibrary.locators import WindowManager


class WindowManagerTests(unittest.TestCase):

    def test_select_with_invalid_prefix(self):
        manager = WindowManagerWithMockBrowser()
        with self.assertRaises(WindowNotFound) as context:
            manager.select("something=test1")
        self.assertEqual(
            str(context.exception),
            "No window matching handle, name, title or URL 'something=test1' found."
        )

    def test_select_by_title(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("title=Title 2")
        self.assertEqual(manager.driver.current_window.name, 'win2')

    def test_select_by_title_with_multiple_matches(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2", 'url': 'http://localhost/page2a.html'},
            {'name': 'win2b', 'title': "Title 2", 'url': 'http://localhost/page2b.html'}
        )
        manager.select("title=Title 2")
        self.assertEqual(manager.driver.current_window.name, 'win2a')

    def test_select_by_title_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(WindowNotFound) as context:
            manager.select("title=Title -1")
        self.assertEqual(str(context.exception),
                         "Unable to locate window with title 'Title -1'.")

    def test_select_by_name(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.driver.current_window.name, 'win2')

    def test_select_by_name_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(WindowNotFound) as context:
            manager.select("name=win-1")
        self.assertEqual(str(context.exception),
                         "Unable to locate window with name 'win-1'.")

    def test_select_by_url(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("url=http://localhost/page2.html")
        self.assertEqual(manager.driver.current_window.name, 'win2')

    def test_select_by_url_with_multiple_matches(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2a', 'title': "Title 2a", 'url': 'http://localhost/page2.html'},
            {'name': 'win2b', 'title': "Title 2b", 'url': 'http://localhost/page2.html'}
        )
        manager.select("url=http://localhost/page2.html")
        self.assertEqual(manager.driver.current_window.name, 'win2a')

    def test_select_by_url_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(WindowNotFound) as context:
            manager.select("url=http://localhost/page-1.html")
        self.assertEqual(
            str(context.exception),
            "Unable to locate window with URL 'http://localhost/page-1.html'."
        )

    def test_select_main_window(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.driver.current_window.name, 'win2')
        manager.select("main")
        self.assertEqual(manager.driver.current_window.name, 'win1')
        manager.select("MAIN")
        self.assertEqual(manager.driver.current_window.name, 'win1')

    def test_select_by_default_with_name(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("win2")
        self.assertEqual(manager.driver.current_window.name, 'win2')

    def test_select_by_default_with_title(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("Title 2")
        self.assertEqual(manager.driver.current_window.name, 'win2')

    def test_select_by_default_no_match(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        with self.assertRaises(WindowNotFound) as context:
            manager.select('foobar')
        self.assertEqual(
            str(context.exception),
            "No window matching handle, name, title or URL 'foobar' found."
        )

    def test_prefix_is_case_sensitive(self):
        manager = WindowManagerWithMockBrowser(
            {'name': 'win1', 'title': "Title 1", 'url': 'http://localhost/page1.html'},
            {'name': 'win2', 'title': "Title 2", 'url': 'http://localhost/page2.html'},
            {'name': 'win3', 'title': "Title 3", 'url': 'http://localhost/page3.html'}
        )
        manager.select("name=win2")
        self.assertEqual(manager.driver.current_window.name, 'win2')
        with self.assertRaises(WindowNotFound) as context:
            manager.select("nAmE=win2")
        self.assertEqual(
            str(context.exception),
            "No window matching handle, name, title or URL 'nAmE=win2' found."
        )

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
        ctx.driver = self._make_mock_driver(*window_specs)
        WindowManager.__init__(self, ctx)

    def _make_mock_driver(self, *window_specs):
        driver = mock()
        current_window = mock()
        driver.window_handles = []
        window_infos = {}
        for window_spec in window_specs:
            handle = uuid.uuid4().hex
            driver.window_handles.append(handle)
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
            if handle_ in driver.window_handles:
                driver.session_id = handle_
                current_window.name = window_infos[handle_][1]
                driver.current_window = current_window
                driver.title = window_infos[handle_][2]
                driver.current_url = window_infos[handle_][3]

        switch_to = mock()
        switch_to.window = window
        driver.switch_to = switch_to

        def execute_script(script):
            handle_ = driver.session_id
            if handle_ in driver.window_handles:
                return window_infos[handle_][:2]

        driver.execute_script = execute_script
        return driver
