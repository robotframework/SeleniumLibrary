from Selenium2Library.base import LibraryComponent, keyword
from Selenium2Library.utils import is_truthy


class CookieKeywords(LibraryComponent):

    @keyword
    def delete_all_cookies(self):
        """Deletes all cookies."""
        self.browser.delete_all_cookies()

    @keyword
    def delete_cookie(self, name):
        """Deletes cookie matching `name`.

        If the cookie is not found, nothing happens.
        """
        self.browser.delete_cookie(name)

    @keyword
    def get_cookies(self):
        """Returns all cookies of the current page."""
        pairs = []
        for cookie in self.browser.get_cookies():
            pairs.append(cookie['name'] + "=" + cookie['value'])
        return '; '.join(pairs)

    @keyword
    def get_cookie_value(self, name):
        """Returns value of cookie found with `name`.

        If no cookie is found with `name`, this keyword fails.
        """
        cookie = self.browser.get_cookie(name)
        if cookie is not None:
            return cookie['value']
        raise ValueError("Cookie with name %s not found." % name)

    @keyword
    def add_cookie(self, name, value, path=None, domain=None, secure=None):
        """Adds a cookie to your current session.

        "name" and "value" are required, "path", "domain" and "secure" are
        optional
        """
        new_cookie = {'name': name, 'value': value}
        if is_truthy(path):
            new_cookie['path'] = path
        if is_truthy(domain):
            new_cookie['domain'] = domain
        # Secure should be True or False
        if is_truthy(secure):
            new_cookie['secure'] = secure
        self.browser.add_cookie(new_cookie)
