import unittest
from Selenium2Library.keywords._browsermanagement import _BrowserManagementKeywords
from selenium import webdriver

class BrowserManagementTests(unittest.TestCase): 

    
    def test_create_firefox_browser(self):
        test_browsers = ((webdriver.Firefox, "ff"), (webdriver.Firefox, "firEfOx"))

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)
    
    def mock_createProfile(self, profile_directory=None):
        self.ff_profile_dir = profile_directory
        return self.old_profile_init(profile_directory)

    def test_create_ie_browser(self):
        test_browsers = ((webdriver.Ie, "ie"), (webdriver.Ie, "Internet Explorer"))

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)

    def test_create_chrome_browser(self):
        test_browsers = ((webdriver.Chrome, "gOOglEchrOmE"),(webdriver.Chrome,"gc"),
                          (webdriver.Chrome, "chrome"))

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)

    def test_create_opera_browser(self):
        self.verify_browser(webdriver.Opera, "OPERA")

    def test_create_remote_browser(self):
        self.verify_browser(webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub")

    def test_create_htmlunit_browser(self):
        self.verify_browser(webdriver.Remote, "htmlunit")

    def test_create_htmlunitwihtjs_browser(self):
        self.verify_browser(webdriver.Remote, "htmlunitwithjs")

    def test_create_desired_capabilities(self):
        bm = _BrowserManagementKeywords()
        expected_caps = "key1:val1,key2:val2"
        capabilities = bm._create_desired_capabilities(webdriver.DesiredCapabilities.CHROME, expected_caps)
        self.assertTrue(type(capabilities), webdriver.DesiredCapabilities.CHROME)
        self.assertTrue("val1", capabilities["key1"])
        self.assertTrue("val2", capabilities["key2"])
        self.assertTrue(2, len(capabilities))

    def test_create_remote_browser_with_desired_prefs(self):
        expected_caps = "key1:val1,key2:val2"
        self.verify_browser(webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub",
            desired_capabilities=expected_caps)


    def verify_browser(self , webdriver_type , browser_name, **kw):
        #todo try lambda *x: was_called = true
        bm = _BrowserManagementKeywords()
        old_init = webdriver_type.__init__
        webdriver_type.__init__ = self.mock_init
        
        try:
            self.was_called = False
            bm._make_browser(browser_name, **kw)
        except AttributeError:
            pass #kinda dangerous but I'm too lazy to mock out all the set_timeout calls
        finally:
            webdriver_type.__init__ = old_init
            self.assertTrue(self.was_called)
            
    def mock_init(self, *args, **kw):
        self.was_called = True



