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

import os

from robot.utils import ConnectionCache
from selenium import webdriver

from SeleniumLibrary.utils import is_falsy, is_truthy, SELENIUM_VERSION


class WebDriverCreator(object):

    browser_names = {
        'googlechrome': "chrome",
        'gc': "chrome",
        'chrome': "chrome",
        'headlesschrome': 'headless_chrome',
        'ff': 'firefox',
        'firefox': 'firefox',
        'headlessfirefox': 'headless_firefox',
        'ie': 'ie',
        'internetexplorer': 'ie',
        'edge': 'edge',
        'opera': 'opera',
        'safari': 'safari',
        'phantomjs': 'phantomjs',
        'htmlunit': 'htmlunit',
        'htmlunitwithjs': 'htmlunit_with_js',
        'android': 'android',
        'iphone': 'iphone'
    }

    def __init__(self, log_dir):
        self.log_dir = log_dir

    def create_driver(self, browser, desired_capabilities, remote_url,
                      profile_dir=None):
        creation_method = self._get_creator_method(browser)
        desired_capabilities = self._parse_capabilities(desired_capabilities)
        if (creation_method == self.create_firefox
                or creation_method == self.create_headless_firefox):
            return creation_method(desired_capabilities, remote_url,
                                   profile_dir)
        return creation_method(desired_capabilities, remote_url)

    def _get_creator_method(self, browser):
        browser = browser.lower().replace(' ', '')
        if browser in self.browser_names:
            return getattr(self, 'create_{}'.format(self.browser_names[browser]))
        raise ValueError('{} is not a supported browser.'.format(browser))

    def _parse_capabilities(self, capabilities):
        if isinstance(capabilities, dict):
            return capabilities
        desired_capabilities = {}
        if is_falsy(capabilities):
            return desired_capabilities
        for part in capabilities.split(','):
            key, value = part.split(':')
            desired_capabilities[key.strip()] = value.strip()
        return desired_capabilities

    def create_chrome(self, desired_capabilities, remote_url, options=None):
        default = webdriver.DesiredCapabilities.CHROME
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url,
                                options=options)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            return webdriver.Chrome(desired_capabilities=capabilities,
                                    options=options)
        return webdriver.Chrome(desired_capabilities=capabilities)

    def create_headless_chrome(self, desired_capabilities, remote_url):
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            options = webdriver.ChromeOptions()
            options.set_headless()
        else:
            options = None
        return self.create_chrome(desired_capabilities, remote_url, options)

    def create_firefox(self, desired_capabilities, remote_url, ff_profile_dir,
                       options=None):
        default = webdriver.DesiredCapabilities.FIREFOX
        profile = self._get_ff_profile(ff_profile_dir)
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url,
                                profile, options)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            return webdriver.Firefox(capabilities=capabilities, options=options,
                                     firefox_profile=profile,
                                     **self._geckodriver_log)
        return webdriver.Firefox(capabilities=capabilities,
                                 firefox_profile=profile,
                                 **self._geckodriver_log)

    def _get_ff_profile(self, ff_profile_dir):
        if is_falsy(ff_profile_dir):
            return webdriver.FirefoxProfile()
        return webdriver.FirefoxProfile(ff_profile_dir)

    @property
    def _geckodriver_log(self):
        if SELENIUM_VERSION.major >= 3:
            return {'log_path': os.path.join(self.log_dir, 'geckodriver.log')}
        return {}

    def create_headless_firefox(self, desired_capabilities, remote_url,
                                ff_profile_dir):
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            options = webdriver.FirefoxOptions()
            options.set_headless()
        else:
            options = None
        return self.create_firefox(desired_capabilities, remote_url,
                                   ff_profile_dir, options)

    def create_ie(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.INTERNETEXPLORER
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        return webdriver.Ie(capabilities=capabilities)

    def create_edge(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.EDGE
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        return webdriver.Edge(capabilities=capabilities)

    def create_opera(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.OPERA
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        return webdriver.Opera(desired_capabilities=capabilities)

    def create_safari(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.SAFARI
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        return webdriver.Safari(desired_capabilities=capabilities)

    def create_phantomjs(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.PHANTOMJS
        if is_truthy(remote_url):
            return self._remote(default, desired_capabilities, remote_url)
        capabilities = self._combine_capabilites(default, desired_capabilities)
        return webdriver.PhantomJS(desired_capabilities=capabilities)

    def create_htmlunit(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.HTMLUNIT
        return self._remote(default, desired_capabilities, remote_url)

    def create_htmlunit_with_js(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        return self._remote(default, desired_capabilities, remote_url)

    def create_android(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.ANDROID
        return self._remote(default, desired_capabilities, remote_url)

    def create_iphone(self, desired_capabilities, remote_url):
        default = webdriver.DesiredCapabilities.IPHONE
        return self._remote(default, desired_capabilities, remote_url)

    def _remote(self, default_capabilities, user_capabilities, remote_url,
                profile_dir=None, options=None):
        remote_url = str(remote_url)
        capabilities = self._combine_capabilites(default_capabilities,
                                                 user_capabilities)
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            return webdriver.Remote(command_executor=remote_url,
                                    desired_capabilities=capabilities,
                                    browser_profile=profile_dir, options=options)
        return webdriver.Remote(command_executor=remote_url,
                                desired_capabilities=capabilities,
                                browser_profile=profile_dir)

    def _combine_capabilites(self, default, user):
        default = default.copy()
        default.update(user)
        return default


class WebDriverCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current browser')
        self._closed = set()

    @property
    def drivers(self):
        return self._connections

    @property
    def active_drivers(self):
        open_drivers = []
        for driver in self._connections:
            if driver not in self._closed:
                open_drivers.append(driver)
        return open_drivers

    def close(self):
        if self.current:
            driver = self.current
            driver.quit()
            self.current = self._no_current
            self._closed.add(driver)

    def close_all(self):
        for driver in self._connections:
            if driver not in self._closed:
                driver.quit()
        self.empty_cache()
        return self.current
