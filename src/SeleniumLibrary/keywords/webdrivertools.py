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
import warnings

from robot.utils import ConnectionCache
from selenium import webdriver

from SeleniumLibrary.utils import is_falsy, is_truthy


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
        desired_capabilities = self._parse_capabilities(desired_capabilities, browser)
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

    def _parse_capabilities(self, capabilities, browser=None):
        if is_falsy(capabilities):
            return {}
        if not isinstance(capabilities, dict):
            capabilities = self._string_to_dict(capabilities)
        browser = self.browser_names.get(browser, browser)
        if browser in ['ie', 'firefox', 'edge']:
            return {'capabilities': capabilities}
        return {'desired_capabilities': capabilities}

    def _string_to_dict(self, capabilities):
        desired_capabilities = {}
        for part in capabilities.split(','):
            key, value = part.split(':')
            desired_capabilities[key.strip()] = value.strip()
        return desired_capabilities

    def _remote_capabilities_resolver(self, set_capabilities, default_capabilities):
        if not set_capabilities:
            return {'desired_capabilities': default_capabilities}
        if 'capabilities' in set_capabilities:
            caps = set_capabilities['capabilities']
        else:
            caps = set_capabilities['desired_capabilities']
        if 'browserName' not in caps:
            caps['browserName'] = default_capabilities['browserName']
        return {'desired_capabilities': caps}

    def create_chrome(self, desired_capabilities, remote_url, options=None):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.CHROME.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url, options=options)
        return webdriver.Chrome(options=options, **desired_capabilities)

    def create_headless_chrome(self, desired_capabilities, remote_url):
        options = webdriver.ChromeOptions()
        # Can be changed to options.headless = True when minimum Selenium version is 3.12.0 or greater.
        options.set_headless()
        return self.create_chrome(desired_capabilities, remote_url, options)

    def create_firefox(self, desired_capabilities, remote_url, ff_profile_dir,
                       options=None):
        profile = self._get_ff_profile(ff_profile_dir)
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.FIREFOX.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url,
                                profile, options)
        desired_capabilities.update(self._geckodriver_log)
        return webdriver.Firefox(options=options, firefox_profile=profile,
                                 **desired_capabilities)

    def _get_ff_profile(self, ff_profile_dir):
        if is_falsy(ff_profile_dir):
            return webdriver.FirefoxProfile()
        return webdriver.FirefoxProfile(ff_profile_dir)

    @property
    def _geckodriver_log(self):
        return {'log_path': os.path.join(self.log_dir, 'geckodriver.log')}

    def create_headless_firefox(self, desired_capabilities, remote_url,
                                ff_profile_dir):
        options = webdriver.FirefoxOptions()
        # Can be changed to options.headless = True when minimum Selenium version is 3.12.0 or greater.
        options.set_headless()
        return self.create_firefox(desired_capabilities, remote_url,
                                   ff_profile_dir, options)

    def create_ie(self, desired_capabilities, remote_url):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        return webdriver.Ie(**desired_capabilities)

    def create_edge(self, desired_capabilities, remote_url):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.EDGE.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        return webdriver.Edge(**desired_capabilities)

    def create_opera(self, desired_capabilities, remote_url):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.OPERA.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        return webdriver.Opera(**desired_capabilities)

    def create_safari(self, desired_capabilities, remote_url):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.SAFARI.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        return webdriver.Safari(**desired_capabilities)

    def create_phantomjs(self, desired_capabilities, remote_url):
        warnings.warn('SeleniumLibrary support for PhantomJS has been deprecated, '
                      'please use headlesschrome or headlessfirefox instead.')
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        return webdriver.PhantomJS(**desired_capabilities)

    def create_htmlunit(self, desired_capabilities, remote_url):
        defaul_caps = webdriver.DesiredCapabilities.HTMLUNIT.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url)

    def create_htmlunit_with_js(self, desired_capabilities, remote_url):
        defaul_caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url)

    def create_android(self, desired_capabilities, remote_url):
        defaul_caps = webdriver.DesiredCapabilities.ANDROID.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url)

    def create_iphone(self, desired_capabilities, remote_url):
        defaul_caps = webdriver.DesiredCapabilities.IPHONE.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url)

    def _remote(self, desired_capabilities, remote_url,
                profile_dir=None, options=None):
        remote_url = str(remote_url)
        return webdriver.Remote(command_executor=remote_url,
                                browser_profile=profile_dir, options=options,
                                **desired_capabilities)


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
