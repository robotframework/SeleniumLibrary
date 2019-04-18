from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords


class BrowserKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def open_browser(self, host):
        url = 'http://{}.com/'.format(host)
        browser_management = BrowserManagementKeywords(self.ctx)
        browser_management.open_browser(url, 'chrome')


class DesiredCapabilitiesKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def get_browser_desired_capabilities(self):
        self.info('Getting currently open browser desired capabilities')
        return self.driver.desired_capabilities


class Decomposition(SeleniumLibrary):

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None):
        SeleniumLibrary.__init__(self, timeout=timeout, implicit_wait=implicit_wait,
                                 run_on_failure=run_on_failure,
                                 screenshot_root_directory=screenshot_root_directory)
        self.add_library_components([BrowserKeywords(self),
                                     DesiredCapabilitiesKeywords(self)])
