import unittest
import os
from Selenium2Library.browsercache import BrowserCache

class MyTests(unittest.TestCase):

    def test_no_current_message(self):
        cache = BrowserCache()
        with self.assertRaises(RuntimeError) as context:
            cache.current.anyMember()
        self.assertEqual(context.exception.message, "No current browser")

    def test_close_only_called_once(self):
        cache = BrowserCache()

        browser1 = FakeBrowser()
        browser2 = FakeBrowser()
        browser3 = FakeBrowser()

        cache.register(browser1)
        cache.register(browser2)
        cache.register(browser3)

        self.assertIs(cache.current, browser3) # sanity check
        cache.close() # called on browser3
        self.assertEquals(browser3.close_count, 1) # ensure close called

        cache.close_all()
        self.assertEquals(browser1.close_count, 1)
        self.assertEquals(browser2.close_count, 1)
        self.assertEquals(browser3.close_count, 1)

class FakeBrowser:

    def __init__(self):
        self.close_count = 0

    def close(self):
        self.close_count = self.close_count + 1

if __name__ == "__main__":
    unittest.main()
