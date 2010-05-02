import unittest
import os

from SeleniumLibrary import SeleniumLibrary


class TestGetBrowser(unittest.TestCase):

    def setUp(self):
        self.lib = SeleniumLibrary()

    def test_ie_aliases(self):
        for alias in ['ie', 'IE', 'Internet Explorer', 'INTernETexplOrEr']:
            self.assertEquals(self.lib._get_browser(alias), '*iexplore')

    def test_firefox_aliases(self):
        for alias in ['ff', 'FF', 'firefox', 'FireFox']:
            self.assertEquals(self.lib._get_browser(alias), '*firefox')

    def test_non_alias_is_not_modified(self):
        for non_alias in ['FIREFUX', 'i e 8', 'C:\\Program Files\\mybrowser\\brow.exe',
                          '{"username": "user", "access-key": "7A9cea40-84f7-4d3b-8748-0e94fCd4dX4f"}']:
            self.assertEquals(self.lib._get_browser(non_alias), non_alias)

    def test_patched_remote_control(self):
        rc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src',
                               'SeleniumLibrary', 'selenium.py')
        self.assertTrue('conn.close()' in open(rc_path).read())

    def test_patched_open_browser(self):
        rc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src',
                               'SeleniumLibrary', 'selenium.py')
        self.assertTrue('self.do_command("open", [url,"true"])' in open(rc_path).read(),
                        "Patch for Firefox 3.6 compatibility required. See issue 114: "+
                        "http://code.google.com/p/robotframework-seleniumlibrary/issues/detail?id=114")


if __name__ == "__main__":
    unittest.main()
