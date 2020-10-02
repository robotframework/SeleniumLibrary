import unittest

from mockito import mock, verify, when, unstub
from robot.utils.connectioncache import NoConnection
from selenium.common.exceptions import TimeoutException, RemoteDriverServerException

from SeleniumLibrary.keywords import WebDriverCache


class WebDriverCacheTests(unittest.TestCase):
    def tearDown(self):
        unstub()

    def test_no_current_message(self):
        cache = WebDriverCache()
        try:
            self.assertRaises(RuntimeError, cache.current.anyMember())
        except RuntimeError as e:
            self.assertEqual(str(e), "No current browser")

    def test_browsers_property(self):
        cache = WebDriverCache()

        driver1 = mock()
        driver2 = mock()
        driver3 = mock()

        index1 = cache.register(driver1)
        index2 = cache.register(driver2)
        index3 = cache.register(driver3)

        self.assertEqual(len(cache.drivers), 3)
        self.assertEqual(cache.drivers[0], driver1)
        self.assertEqual(cache.drivers[1], driver2)
        self.assertEqual(cache.drivers[2], driver3)
        self.assertEqual(index1, 1)
        self.assertEqual(index2, 2)
        self.assertEqual(index3, 3)

    def test_get_open_browsers(self):
        cache = WebDriverCache()

        driver1 = mock()
        driver2 = mock()
        driver3 = mock()

        cache.register(driver1)
        cache.register(driver2)
        cache.register(driver3)

        drivers = cache.active_drivers
        self.assertEqual(len(drivers), 3)
        self.assertEqual(drivers[0], driver1)
        self.assertEqual(drivers[1], driver2)
        self.assertEqual(drivers[2], driver3)

        cache.close()
        drivers = cache.active_drivers
        self.assertEqual(len(drivers), 2)
        self.assertEqual(drivers[0], driver1)
        self.assertEqual(drivers[1], driver2)

    def test_close(self):
        cache = WebDriverCache()
        browser = mock()
        cache.register(browser)

        verify(browser, times=0).quit()  # sanity check
        cache.close()
        verify(browser, times=1).quit()

    def test_close_only_called_once(self):
        cache = WebDriverCache()

        browser1 = mock()
        browser2 = mock()
        browser3 = mock()

        cache.register(browser1)
        cache.register(browser2)
        cache.register(browser3)

        cache.close()
        verify(browser3, times=1).quit()

        cache.close_all()
        verify(browser1, times=1).quit()
        verify(browser2, times=1).quit()
        verify(browser3, times=1).quit()

    def test_resolve_alias_or_index(self):
        cache = WebDriverCache()

        cache.register(mock(), "foo")
        cache.register(mock())
        cache.register(mock())

        index = cache.get_index("foo")
        self.assertEqual(index, 1)

        index = cache.get_index(1)
        self.assertEqual(index, 1)

        index = cache.get_index(3)
        self.assertEqual(index, 3)

        index = cache.get_index(None)
        self.assertEqual(index, None)

        index = cache.get_index("None")
        self.assertEqual(index, None)

    def test_resolve_alias_or_index_with_none(self):
        cache = WebDriverCache()

        cache.register(mock(), "foo")
        cache.register(mock(), "None")

        index = cache.get_index("foo")
        self.assertEqual(index, 1)

        index = cache.get_index(1)
        self.assertEqual(index, 1)

        index = cache.get_index(None)
        self.assertEqual(index, None)

    def test_resolve_alias_or_index_error(self):
        cache = WebDriverCache()

        cache.register(mock(), "foo")
        cache.register(mock())

        index = cache.get_index("bar")
        self.assertEqual(index, None)

        index = cache.get_index(12)
        self.assertEqual(index, None)

        index = cache.get_index(-1)
        self.assertEqual(index, None)

    def test_close_and_same_alias(self):
        cache = WebDriverCache()

        cache.register(mock(), "foo")
        cache.register(mock(), "bar")
        cache.close()
        index = cache.get_index("bar")
        self.assertEqual(index, None)

    def test_same_alias_new_browser(self):
        cache = WebDriverCache()
        cache.close()
        index = cache.get_index("bar")
        self.assertEqual(index, None)

    def test_close_all_cache_first_quite_fails(self):
        cache = WebDriverCache()
        driver = mock()
        when(driver).quit().thenRaise(TimeoutException("timeout."))
        cache.register(driver, "bar")
        with self.assertRaises(TimeoutException):
            cache.close_all()
        self.verify_cache(cache)

    def test_close_all_cache_middle_quite_fails(self):
        cache = WebDriverCache()
        driver0, driver1, driver2 = mock(), mock(), mock()
        when(driver0).quit().thenReturn(None)
        when(driver1).quit().thenRaise(TimeoutException("timeout."))
        when(driver2).quit().thenReturn(None)
        cache.register(driver0, "bar0")
        cache.register(driver1, "bar1")
        cache.register(driver2, "bar2")
        with self.assertRaises(TimeoutException):
            cache.close_all()
        self.verify_cache(cache)

    def test_close_all_cache_all_quite_fails(self):
        cache = WebDriverCache()
        driver0, driver1, driver2 = mock(), mock(), mock()
        when(driver0).quit().thenRaise(RemoteDriverServerException("stuff."))
        when(driver1).quit().thenRaise(RemoteDriverServerException("stuff."))
        when(driver2).quit().thenRaise(TimeoutException("timeout."))
        cache.register(driver0, "bar0")
        cache.register(driver1, "bar1")
        cache.register(driver2, "bar2")
        with self.assertRaises(TimeoutException):
            cache.close_all()
        self.verify_cache(cache)

    def test_close_all_cache_not_selenium_error(self):
        cache = WebDriverCache()
        driver0, driver1, driver2 = mock(), mock(), mock()
        when(driver0).quit().thenRaise(RemoteDriverServerException("stuff."))
        when(driver1).quit().thenRaise(ValueError("stuff."))
        when(driver2).quit().thenRaise(TimeoutException("timeout."))
        cache.register(driver0, "bar0")
        cache.register(driver1, "bar1")
        cache.register(driver2, "bar2")
        with self.assertRaises(TimeoutException):
            cache.close_all()
        self.verify_cache(cache)

    def test_close_all_no_error(self):
        cache = WebDriverCache()
        driver0, driver1, driver2 = mock(), mock(), mock()
        when(driver0).quit().thenReturn(None)
        when(driver1).quit().thenReturn(None)
        when(driver2).quit().thenReturn(None)
        cache.close_all()
        self.verify_cache(cache)

    def test_close_quite_fails(self):
        cache = WebDriverCache()
        driver = mock()
        when(driver).quit().thenRaise(TimeoutException("timeout."))
        cache.register(driver, "bar")
        with self.assertRaises(TimeoutException):
            cache.close()
        self.assertTrue(isinstance(cache.current, NoConnection))
        self.assertTrue(driver in cache._closed)

    def test_close_no_error(self):
        cache = WebDriverCache()
        driver = mock()
        when(driver).quit().thenReturn(None)
        cache.register(driver, "bar")
        cache.close()
        self.assertTrue(isinstance(cache.current, NoConnection))
        self.assertTrue(driver in cache._closed)

    def verify_cache(self, cache):
        self.assertEqual(cache._connections, [])
        self.assertEqual(cache._aliases, {})
        self.assertTrue(isinstance(cache.current, NoConnection))
