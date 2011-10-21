from keywordgroup import KeywordGroup

class _CookieKeywords(KeywordGroup):

    def delete_all_cookies(self):
        """Deletes all cookies."""
        self._current_browser().delete_all_cookies()

    def delete_cookie(self, name):
        """Deletes cookie matching `name`.

        If the cookie is not found, nothing happens.
        """
        self._current_browser().delete_cookie(name)

    def get_cookies(self):
        """Returns all cookies of the current page."""
        pairs = []
        for cookie in self._current_browser().get_cookies():
            pairs.append(cookie['name'] + "=" + cookie['value'])
        return '; '.join(pairs)

    def get_cookie_value(self, name):
        """Returns value of cookie found with `name`.

        If no cookie is found with `name`, this keyword fails.
        """
        cookie = self._current_browser().get_cookie(name)
        if cookie is not None:
            return cookie['value']
        raise ValueError("Cookie with name %s not found." % name)
