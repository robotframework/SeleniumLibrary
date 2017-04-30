from robot.utils import ConnectionCache
from robot.api.logger import debug


class BrowserCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current browser')
        self._closed = set()

    @property
    def browsers(self):
        return self._connections

    def get_open_browsers(self):
        open_browsers = []
        for browser in self._connections:
            if browser not in self._closed:
                open_browsers.append(browser)
        return open_browsers

    def close(self):
        if self.current:
            browser = self.current
            browser.quit()
            self.current = self._no_current
            self._closed.add(browser)

    def close_all(self):
        for browser in self._connections:
            if browser not in self._closed:
                browser.quit()
        self.empty_cache()
        return self.current

    def register(self, connection, alias=None):
        for browser in self._connections:
            if browser.session_id == connection.session_id: # and connection.command_executor._url == browser.command_executor._url:
                debug('Browser with session %s already registered. Marking previous one as obsolete'
                            % connection.session_id)
                self._closed.add(browser)
        return super(BrowserCache, self).register(connection, alias)
