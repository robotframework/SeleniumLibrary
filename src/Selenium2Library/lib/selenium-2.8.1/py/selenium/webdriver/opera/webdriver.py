import copy
import base64
import httplib

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command
from service import Service

class Opera(RemoteWebDriver):

    def __init__(self):
        self.service = Service(logging_level, port)
        self.service.start()
        RemoteWebDriver.__init__(self,
            command_executor=self.service.service_url,
            desired_capabilities=DesiredCapabilities.OPERA)

    def quit(self):
        """ Closes the browser and shuts down the ChromeDriver executable
            that is started when starting the ChromeDriver """
        try:
            RemoteWebDriver.quit(self)
        except httplib.BadStatusLine:
            pass
        finally:
            self.service.stop()

    def save_screenshot(self, filename):
        """
        Gets the screenshot of the current window. Returns False if there is
        any IOError, else returns True. Use full paths in your filename.
        """
        png = self._execute(Command.SCREENSHOT)['value']
        try:
            f = open(filename, 'wb')
            f.write(base64.decodestring(png))
            f.close()
        except IOError:
            return False
        finally:
            del png
        return True
