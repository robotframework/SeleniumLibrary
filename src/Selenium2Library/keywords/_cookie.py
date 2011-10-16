class _CookieKeywords(object):

    def delete_all_cookies(self):
        self._current_browser().delete_all_cookies()

    def get_cookies(self):
        pairs = []
        for cookie in self._current_browser().get_cookies():
            pairs.append(cookie['name'] + "=" + cookie['value'])
        return '; '.join(pairs)

    def get_cookie_value(self, name):
        cookie = self._current_browser().get_cookie(name)
        if cookie is not None:
            return cookie['value']
        return None

    def delete_cookie(self, name):
        self._current_browser().delete_cookie(name)
