import time

from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class WebDriverMonkeyPatches:

    RemoteWebDriver._base_execute = RemoteWebDriver.execute

    def execute(self, driver_command, params=None):
        result = self._base_execute(driver_command, params)
        speed = self._get_speed()
        if speed > 0:
            time.sleep(speed)
        return result

    def current_window_is_main(self):
        return self.current_window_handle == self.window_handles[0];

    def set_speed(self, seconds):
        self._speed = seconds

    def _get_speed(self):
        if not hasattr(self, '_speed'):
            self._speed = float(0)
        return self._speed

    RemoteWebDriver.set_speed = set_speed
    RemoteWebDriver._get_speed = _get_speed
    RemoteWebDriver.execute = execute
