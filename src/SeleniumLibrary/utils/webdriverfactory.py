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

try:
    basestring
except NameError:
    basestring = str

import copy

from selenium import webdriver

from .types import is_noney, is_falsy
from .seleniumversion import SELENIUM_VERSION


class CreateBase(object):

    @classmethod
    def parse_desired_capabilities(self, desired_capabilities):
        capabilities = {}
        if is_noney(desired_capabilities):
            return capabilities
        if isinstance(desired_capabilities, dict):
            return desired_capabilities
        for pair in desired_capabilities.split(','):
            key, value = pair.split(':', 1)
            key, value = key.strip(), value.strip()
            capabilities[key] = value
        return capabilities

    @classmethod
    def create_remote(self, command_executor, desired_capabilities, browser_profile=None):
        return webdriver.Remote(command_executor=command_executor,
                                desired_capabilities=desired_capabilities,
                                browser_profile=browser_profile)


class CreateChrome(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.CHROME)
        capabilities.update(desired_capabilities)
        options = self._get_options() if headless else {}
        if is_falsy(remote_url):
            return webdriver.Chrome(desired_capabilities=capabilities, **options)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)

    @classmethod
    def _get_options(self):
        if SELENIUM_VERSION.major == '3' and SELENIUM_VERSION.minor == '8':
            options = webdriver.ChromeOptions()
            options.set_headless()
            return {'options': options}
        return {}


class CreateFirefox(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities, ff_profile_dir):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.FIREFOX)
        capabilities.update(desired_capabilities)
        options = self._get_options() if headless else {}
        if is_falsy(remote_url):
            return webdriver.Firefox(firefox_profile=ff_profile_dir,
                                     capabilities=capabilities, **options)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities,
                                  browser_profile=ff_profile_dir)

    @classmethod
    def _get_options(self):
        if SELENIUM_VERSION.major == 3 and SELENIUM_VERSION.minor == 8:
            options = webdriver.FirefoxOptions()
            options.set_headless()
            return {'options': options}
        return {}


class CreateIe(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.INTERNETEXPLORER)
        capabilities.update(desired_capabilities)
        if is_falsy(remote_url):
            return webdriver.Ie(capabilities=capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateEdge(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.EDGE)
        capabilities.update(desired_capabilities)
        if is_falsy(remote_url):
            return webdriver.Edge(capabilities=capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateOpera(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.OPERA)
        capabilities.update(desired_capabilities)
        if is_falsy(remote_url):
            return webdriver.Opera(desired_capabilities=capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreatePhantomJS(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.PHANTOMJS)
        capabilities.update(desired_capabilities)
        if is_falsy(remote_url):
            return webdriver.PhantomJS(desired_capabilities=capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateSafari(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.SAFARI)
        capabilities.update(desired_capabilities)
        if is_falsy(remote_url):
            return webdriver.Safari(desired_capabilities=capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateAndroid(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        webdriver.Android
        return 'Foobar'


class CreateHtmlUnit(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.HTMLUNIT)
        capabilities.update(desired_capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateHtmlUnitWithJS(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        capabilities = copy.deepcopy(webdriver.DesiredCapabilities.HTMLUNITWITHJS)
        capabilities.update(desired_capabilities)
        return self.create_remote(command_executor=remote_url,
                                  desired_capabilities=capabilities)


class CreateiPhone(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities):
        return 'Foobar'


class WebDriverFactory(object):

    BROWSER_NAMES = {
        'CHROME': CreateChrome,
        'GC': CreateChrome,
        'GOOGLECHROME': CreateChrome,
        'FF': CreateFirefox,
        'FIREFOX': CreateFirefox,
        'IE': CreateIe,
        'INTERNETEXPLORER': CreateIe,
        'EDGE': CreateEdge,
        'PHANTOMJS': CreatePhantomJS,
        'SAFARI': CreateSafari,
        'OPERA': CreateOpera,
        'HTMLUNIT': CreateHtmlUnit,
        'HTMLUNITWITHJS': CreateHtmlUnitWithJS,
        'ANDROID': CreateAndroid,
        'IPHONE': CreateiPhone
    }

    def __init__(self, browser):
        self.browser = browser

    def parse_browser(self):
        browser = self.browser.strip().upper().replace('_', '').replace(' ', '')
        headless, browser = self._headless(browser)
        creator = self._get_driver_creator(browser)
        self._check_headless(headless, creator)
        return headless, creator

    def _headless(self, browser):
        if browser.startswith('HEADLESS'):
            return True, browser.replace('HEADLESS', '')
        return False, browser

    def _get_driver_creator(self, browser):
        creator = self.BROWSER_NAMES.get(browser)
        if not creator:
            raise ValueError("{} is not a supported browser.".format(self.browser))
        return creator

    def _check_headless(self, headless, creator):
        if not headless:
            return True
        if creator is CreateChrome or creator is CreateFirefox:
            return True
        raise ValueError("{} is not a supported browser.".format(self.browser))

    def create(self, remote_url, desired_capabilities, ff_profile_dir):
        headless, driver_creator = self.parse_browser()
        desired_capabilities = driver_creator.parse_desired_capabilities(
            desired_capabilities)
        if driver_creator is CreateFirefox:
            return driver_creator.create(headless, remote_url, desired_capabilities,
                                         ff_profile_dir)
        return driver_creator.create(headless, remote_url, desired_capabilities)
