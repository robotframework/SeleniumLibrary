# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime

from robot.libraries.DateTime import convert_date
from robot.utils import DotDict

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.errors import CookieNotFound
from SeleniumLibrary.utils import is_truthy, is_noney, is_falsy


class CookieKeywords(LibraryComponent):

    @keyword
    def delete_all_cookies(self):
        """Deletes all cookies."""
        self.driver.delete_all_cookies()

    @keyword
    def delete_cookie(self, name):
        """Deletes the cookie matching ``name``.

        If the cookie is not found, nothing happens.
        """
        self.driver.delete_cookie(name)

    @keyword
    def get_cookies(self, as_dict=False):
        """Returns all cookies of the current page.

        If ``as_dict`` argument evaluates as false, see `Boolean arguments`
        for more details, then cookie information is returned as
        a single string in format ``name1=value1; name2=value2; name3=value3``.
        When ``as_dict`` argument evaluates as true, cookie information
        is returned as Robot Framework dictionary format. The string format
        can be used, for example, for logging purposes or in headers when
        sending HTTP requests. The dictionary format is helpful when
        the result can be passed to requests library's Create Session
        keyword's optional cookies parameter.

        The `` as_dict`` argument is new in SeleniumLibrary 3.3
        """
        if is_falsy(as_dict):
            pairs = []
            for cookie in self.driver.get_cookies():
                pairs.append(cookie['name'] + "=" + cookie['value'])
            return '; '.join(pairs)
        else:
            pairs = DotDict()
            for cookie in self.driver.get_cookies():
                pairs[cookie['name']] = cookie['value']
            return pairs

    @keyword
    def get_cookie(self, name):
        """Returns information of cookie with ``name`` as an object.

        If no cookie is found with ``name``, keyword fails. The cookie object
        contains details about the cookie. Attributes available in the object
        are documented in the table below.

        | = Attribute = |             = Explanation =                                |
        | name          | The name of a cookie.                                      |
        | value         | Value of the cookie.                                       |
        | path          | Indicates a URL path, for example ``/``.                   |
        | domain        | The domain, the cookie is visible to.                      |
        | secure        | When true, the cookie is only used with HTTPS connections. |
        | httpOnly      | When true, the cookie is not accessible via JavaScript.    |
        | expiry        | Python datetime object indicating when the cookie expires. |
        | extra         | Possible attributes outside of the WebDriver specification |

        See the
        [https://w3c.github.io/webdriver/#cookies|WebDriver specification]
        for details about the cookie information.
        Notice that ``expiry`` is specified as a
        [https://docs.python.org/3/library/datetime.html#datetime.datetime|datetime object],
        not as seconds since Unix Epoch like WebDriver natively does.

        In some cases, example when running a browser in the cloud, it is possible that
        the cookie contains other attributes than is defined in the
        [https://w3c.github.io/webdriver/#cookies|WebDriver specification].
        These other attributes are available in an ``extra`` attribute in the cookie
        object and it contains a dictionary of the other attributes. The ``extra``
        attribute is new in SeleniumLibrary 4.0.

        Example:
        | `Add Cookie`      | foo             | bar |
        | ${cookie} =       | `Get Cookie`    | foo |
        | `Should Be Equal` | ${cookie.name}  | bar |
        | `Should Be Equal` | ${cookie.value} | foo |
        | `Should Be True`  | ${cookie.expiry.year} > 2017 |

        New in SeleniumLibrary 3.0.
        """
        cookie = self.driver.get_cookie(name)
        if not cookie:
            raise CookieNotFound("Cookie with name '%s' not found." % name)
        return CookieInformation(**cookie)

    @keyword
    def add_cookie(self, name, value, path=None, domain=None, secure=None,
                   expiry=None):
        """Adds a cookie to your current session.

        ``name`` and ``value`` are required, ``path``, ``domain``, ``secure``
        and ``expiry`` are optional.  Expiry supports the same formats as
        the [http://robotframework.org/robotframework/latest/libraries/DateTime.html|DateTime]
        library or an epoch timestamp.

        Example:
        | `Add Cookie` | foo | bar |                            |
        | `Add Cookie` | foo | bar | domain=example.com         |
        | `Add Cookie` | foo | bar | expiry=2027-09-28 16:21:35 | # Expiry as timestamp.     |
        | `Add Cookie` | foo | bar | expiry=1822137695          | # Expiry as epoch seconds. |

        Prior to SeleniumLibrary 3.0 setting expiry did not work.
        """
        new_cookie = {'name': name, 'value': value}
        if not is_noney(path):
            new_cookie['path'] = path
        if not is_noney(domain):
            new_cookie['domain'] = domain
        # Secure must be True or False
        if not is_noney(secure):
            new_cookie['secure'] = is_truthy(secure)
        if not is_noney(expiry):
            new_cookie['expiry'] = self._expiry(expiry)
        self.driver.add_cookie(new_cookie)

    def _expiry(self, expiry):
        try:
            return int(expiry)
        except ValueError:
            return int(convert_date(expiry, result_format='epoch'))


class CookieInformation(object):

    def __init__(self, name, value, path=None, domain=None, secure=False,
                 httpOnly=False, expiry=None, **extra):
        self.name = name
        self.value = value
        self.path = path
        self.domain = domain
        self.secure = secure
        self.httpOnly = httpOnly
        self.expiry = datetime.fromtimestamp(expiry) if expiry else None
        self.extra = extra

    def __str__(self):
        items = 'name value path domain secure httpOnly expiry'.split()
        string = '\n'.join('%s=%s' % (item, getattr(self, item))
                           for item in items)
        if self.extra:
            string = '%s\n%s=%s\n' % (string, 'extra', self.extra)
        return string
