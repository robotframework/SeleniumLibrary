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


from selenium import webdriver

from types import is_noney


class WebDriverFactory(object):

    def __init__(self, browser):
        self.browser = browser

    def parse_browser(self):
        browser = self.browser.strip().upper().replace('_', '').replace(' ', '')
        headless, browser = self._headless(browser)
        if browser in ['CHROME', 'GOOGLECHROME', 'GC', 'HEADLESSCHROME']:
            return headless, CreateChrome
        if browser in ['FF', 'FIREFOX']:
            return headless, CreateFirefox
        if browser in ['IE', 'INTERNETEXPLORER'] and not headless:
            return headless, CreateIe
        if browser == 'OPERA' and not headless:
            return headless, CreateOpera
        if browser == 'PHANTOMJS' and not headless:
            return headless, CreatePhantomJS
        if browser == 'EDGE' and not headless:
            return headless, CreateEdge
        if browser == 'SAFARI' and not headless:
            return headless, CreateSafari
        if browser == 'ANDROID' and not headless:
            return headless, CreateAndroid
        if browser == 'HTMLUNIT' and not headless:
            return headless, CreateHtmlUnit
        if browser == 'HTMLUNITWITHJS' and not headless:
            return headless, CreateHtmlUnitWithJS
        if browser == 'IPHONE' and not headless:
            return headless, CreateiPhone
        raise ValueError('{} is not a supported browser.'.format(self.browser))

    def _headless(self, browser):
        if browser.startswith('HEADLESS'):
            return True, browser.replace('HEADLESS', '')
        return False, browser

    def create(self, remote_url, desired_capabilities, ff_profile_dir):
        headless, driver_creator = self.parse_browser()
        if driver_creator is CreateFirefox:
            return driver_creator.create(headless, remote_url, desired_capabilities,
                                         ff_profile_dir)
        return driver_creator.create(headless, remote_url, desired_capabilities)


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
        desired_capabilities = self.parse_desired_capabilities(desired_capabilities)
        desired_capabilities.update(webdriver.DesiredCapabilities.CHROME)
        if headless:
            options = webdriver.ChromeOptions()
            options.set_headless()
        else:
            options = None
        if not is_noney(remote_url):
            return self.create_remote(command_executor=remote_url,
                                      desired_capabilities=desired_capabilities)
        return webdriver.Chrome(desired_capabilities=desired_capabilities,
                                options=options)


class CreateFirefox(CreateBase):

    @classmethod
    def create(self, headless, remote_url, desired_capabilities, ff_profile_dir):
        desired_capabilities = self.parse_desired_capabilities(desired_capabilities)
        desired_capabilities.update(webdriver.DesiredCapabilities.FIREFOX)
        if headless:
            options = webdriver.FirefoxOptions()
            options.set_headless()
        else:
            options = None
        if not is_noney(remote_url):
            return self.create_remote(command_executor=remote_url,
                                      desired_capabilities=desired_capabilities,
                                      browser_profile=ff_profile_dir)
        return webdriver.Firefox(firefox_profile=ff_profile_dir,
                                 capabilities=desired_capabilities,
                                 options=options)


class CreateIe(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'


class CreateEdge(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'


class CreateOpera(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'


class CreatePhantomJS(CreateBase):

    @classmethod
    def create(self, headless):
        webdriver.PhantomJS
        return 'Foobar'


class CreateSafari(CreateBase):

    @classmethod
    def create(self, headless):
        webdriver.Safari
        return 'Foobar'


class CreateAndroid(CreateBase):

    @classmethod
    def create(self, headless):
        webdriver.Android
        return 'Foobar'


class CreateHtmlUnit(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'


class CreateHtmlUnitWithJS(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'


class CreateiPhone(CreateBase):

    @classmethod
    def create(self, headless):
        return 'Foobar'
