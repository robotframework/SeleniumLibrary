import unittest
import os
from Selenium2Library.browsercache import BrowserCache
from mockito import *

class BrowserCacheTests(unittest.TestCase): 

    def test_no_current_message(self):
        cache = BrowserCache()
        with self.assertRaises(RuntimeError) as context:
            cache.current.anyMember()
        self.assertEqual(context.exception.message, "No current browser")

    def test_close(self):
        cache = BrowserCache()
        browser = mock()
        cache.register(browser)

        verify(browser, times=0).close() # sanity check
        cache.close()
        verify(browser, times=1).close()

    def test_close_only_called_once(self):
        cache = BrowserCache()

        browser1 = mock()
        browser2 = mock()
        browser3 = mock()

        cache.register(browser1)
        cache.register(browser2)
        cache.register(browser3)

        cache.close()
        verify(browser3, times=1).close()

        cache.close_all()
        verify(browser1, times=1).close()
        verify(browser2, times=1).close()
        verify(browser3, times=1).close()

if __name__ == "__main__":
    unittest.main()
