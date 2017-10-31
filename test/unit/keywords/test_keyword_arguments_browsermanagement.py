import unittest

from mockito import mock, unstub, when

from SeleniumLibrary.keywords import BrowserManagementKeywords


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.brorser = BrowserManagementKeywords(ctx)

    def tearDown(self):
        unstub()

    def test_open_browser(self):
        url = 'https://github.com/robotframework'
        remote_url = '"http://localhost:4444/wd/hub"'
        browser = mock()
        when(self.brorser)._make_driver('firefox', None,
                                        None, False).thenReturn(browser)
        alias = self.brorser.open_browser(url)
        self.assertEqual(alias, None)

        when(self.brorser)._make_driver('firefox', None,
                                        None, remote_url).thenReturn(browser)
        alias = self.brorser.open_browser(url, alias='None',
                                          remote_url=remote_url)
        self.assertEqual(alias, None)
