import unittest
import os
from Selenium2Library.utils import BrowserCache
from mockito import *

class BrowserCacheTests(unittest.TestCase): 

    def test_no_current_message(self):
        cache = BrowserCache()
        try:
            self.assertRaises(RuntimeError, cache.current.anyMember())
        except RuntimeError as e:
            self.assertEqual(e.message, "No current browser")

    def test_browsers_property(self):
        cache = BrowserCache()

        browser1 = mock()
        browser2 = mock()
        browser3 = mock()

        cache.register(browser1)
        cache.register(browser2)
        cache.register(browser3)

        self.assertEqual(len(cache.browsers), 3)
        self.assertEqual(cache.browsers[0], browser1)
        self.assertEqual(cache.browsers[1], browser2)
        self.assertEqual(cache.browsers[2], browser3)

    def test_get_open_browsers(self):
        cache = BrowserCache()

        browser1 = mock()
        browser2 = mock()
        browser3 = mock()

        cache.register(browser1)
        cache.register(browser2)
        cache.register(browser3)

        browsers = cache.get_open_browsers()
        self.assertEqual(len(browsers), 3)
        self.assertEqual(browsers[0], browser1)
        self.assertEqual(browsers[1], browser2)
        self.assertEqual(browsers[2], browser3)

        cache.close()
        browsers = cache.get_open_browsers()
        self.assertEqual(len(browsers), 2)
        self.assertEqual(browsers[0], browser1)
        self.assertEqual(browsers[1], browser2)

    def test_close(self):
        cache = BrowserCache()
        browser = mock()
        cache.register(browser)

        verify(browser, times=0).quit() # sanity check
        cache.close()
        verify(browser, times=1).quit()

    def test_close_only_called_once(self):
        cache = BrowserCache()

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
