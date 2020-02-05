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
import ast
import importlib
import inspect
import os
import token
import warnings
from tokenize import generate_tokens

from robot.api import logger
from robot.utils import ConnectionCache, StringIO
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from SeleniumLibrary.utils import is_falsy, is_truthy, is_noney, is_string, PY3
from SeleniumLibrary.keywords.webdrivertools.sl_file_detector import SelLibLocalFileDetector
from SeleniumLibrary.utils.path_formatter import _format_path

if not PY3:
    FileNotFoundError = object


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
        self.selenium_options = SeleniumOptions()

    def create_driver(self, browser, desired_capabilities, remote_url, profile_dir=None,
                      options=None, service_log_path=None, executable_path=None):
        executable_path = None if is_falsy(executable_path) else executable_path
        browser = self._normalise_browser_name(browser)
        creation_method = self._get_creator_method(browser)
        desired_capabilities = self._parse_capabilities(desired_capabilities, browser)
        service_log_path = self._get_log_path(service_log_path)
        options = self.selenium_options.create(self.browser_names.get(browser), options)
        if service_log_path:
            logger.info('Browser driver log file created to: %s' % service_log_path)
            self._create_directory(service_log_path)
        if creation_method == self.create_firefox or creation_method == self.create_headless_firefox:
            return creation_method(desired_capabilities, remote_url, profile_dir, options=options,
                                   service_log_path=service_log_path, executable_path=executable_path)
        return creation_method(desired_capabilities, remote_url, options=options,
                               service_log_path=service_log_path, executable_path=executable_path)

    def _get_creator_method(self, browser):
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

    def create_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                      executable_path='chromedriver'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.CHROME.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url, options=options)
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Chrome)
        return webdriver.Chrome(options=options, service_log_path=service_log_path, executable_path=executable_path,
                                **desired_capabilities)

    def create_headless_chrome(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                               executable_path='chromedriver'):
        if not options:
            options = webdriver.ChromeOptions()
        options.headless = True
        return self.create_chrome(desired_capabilities, remote_url, options, service_log_path, executable_path)

    def _get_executable_path(self, webdriver):
        if PY3:
            signature = inspect.signature(webdriver.__init__)
            parameters = signature.parameters
            executable_path = parameters.get('executable_path')
            if not executable_path:
                return None
            return executable_path.default
        else:  # TODO: Remove else when Python 2 is dropped.
            signature = inspect.getargspec(webdriver.__init__)
            if 'executable_path' in signature.args:
                index = signature.args.index('executable_path')
                return signature.defaults[index - 1]

    def create_firefox(self, desired_capabilities, remote_url, ff_profile_dir, options=None, service_log_path=None,
                       executable_path='geckodriver'):
        profile = self._get_ff_profile(ff_profile_dir)
        if is_truthy(remote_url):
            default_caps = webdriver.DesiredCapabilities.FIREFOX.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, default_caps)
            return self._remote(desired_capabilities, remote_url,
                                profile, options)
        service_log_path = service_log_path if service_log_path else self._geckodriver_log
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Firefox)
        return webdriver.Firefox(options=options, firefox_profile=profile,
                                 service_log_path=service_log_path, executable_path=executable_path,
                                 **desired_capabilities)

    def _get_ff_profile(self, ff_profile_dir):
        if isinstance(ff_profile_dir, FirefoxProfile):
            return ff_profile_dir
        if is_falsy(ff_profile_dir):
            return webdriver.FirefoxProfile()
        try:
            return webdriver.FirefoxProfile(ff_profile_dir)
        except (OSError, FileNotFoundError):
            ff_options = self.selenium_options._parse(ff_profile_dir)
            ff_profile = webdriver.FirefoxProfile()
            for option in ff_options:
                for key in option:
                    attr = getattr(ff_profile, key)
                    if callable(attr):
                        attr(*option[key])
                    else:
                        setattr(ff_profile, key, *option[key])
            return ff_profile

    @property
    def _geckodriver_log(self):
        log_file = self._get_log_path(os.path.join(self.log_dir, 'geckodriver-{index}.log'))
        logger.info('Firefox driver log is always forced to to: %s' % log_file)
        return log_file

    def create_headless_firefox(self, desired_capabilities, remote_url, ff_profile_dir, options=None,
                                service_log_path=None, executable_path='geckodriver'):
        if not options:
            options = webdriver.FirefoxOptions()
        options.headless = True
        return self.create_firefox(desired_capabilities, remote_url, ff_profile_dir, options, service_log_path,
                                   executable_path)

    def create_ie(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                  executable_path='IEDriverServer.exe'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url, options=options)
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Ie)
        return webdriver.Ie(options=options, service_log_path=service_log_path, executable_path=executable_path,
                            **desired_capabilities)

    def _has_options(self, web_driver):
        signature = inspect.getargspec(web_driver.__init__)
        return 'options' in signature.args

    def create_edge(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                    executable_path='MicrosoftWebDriver.exe'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.EDGE.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Edge)
        if self._has_options(webdriver.Edge):
            # options is supported from Selenium 4.0 onwards
            # If can be removed when minimum Selenium version is 4.0 or greater
            return webdriver.Edge(options=options, service_log_path=service_log_path, executable_path=executable_path,
                                  **desired_capabilities)
        return webdriver.Edge(service_log_path=service_log_path, executable_path=executable_path, **desired_capabilities)

    def create_opera(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                     executable_path='operadriver'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.OPERA.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url, options=options)
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Opera)
        return webdriver.Opera(options=options, service_log_path=service_log_path, executable_path=executable_path,
                               **desired_capabilities)

    def create_safari(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                      executable_path='/usr/bin/safaridriver'):
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.SAFARI.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        if options or service_log_path:
            logger.warn('Safari browser does not support Selenium options or service_log_path.')
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.Safari)
        return webdriver.Safari(executable_path=executable_path, **desired_capabilities)

    def create_phantomjs(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                         executable_path='phantomjs'):
        warnings.warn('SeleniumLibrary support for PhantomJS has been deprecated, '
                      'please use headlesschrome or headlessfirefox instead.')
        if is_truthy(remote_url):
            defaul_caps = webdriver.DesiredCapabilities.PHANTOMJS.copy()
            desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
            return self._remote(desired_capabilities, remote_url)
        if options:
            logger.warn('PhantomJS browser does not support Selenium options.')
        if is_falsy(executable_path):
            executable_path = self._get_executable_path(webdriver.PhantomJS)
        return webdriver.PhantomJS(service_log_path=service_log_path, executable_path=executable_path,
                                   **desired_capabilities)

    def create_htmlunit(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                        executable_path=None):
        if service_log_path or options or executable_path:
            logger.warn('Htmlunit does not support Selenium options, service_log_path or executable_path argument.')
        defaul_caps = webdriver.DesiredCapabilities.HTMLUNIT.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url, options=options)

    def create_htmlunit_with_js(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                                executable_path=None):
        if service_log_path or options or executable_path:
            logger.warn('Htmlunit with JS does not support Selenium options, service_log_path or executable_path argument.')
        defaul_caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url, options=options)

    def create_android(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                       executable_path=None):
        if service_log_path or executable_path:
            logger.warn('Android does not support Selenium options or executable_path argument.')
        defaul_caps = webdriver.DesiredCapabilities.ANDROID.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url, options=options)

    def create_iphone(self, desired_capabilities, remote_url, options=None, service_log_path=None,
                      executable_path=None):
        if service_log_path or executable_path:
            logger.warn('iPhone does not support service_log_path or executable_path argument.')
        defaul_caps = webdriver.DesiredCapabilities.IPHONE.copy()
        desired_capabilities = self._remote_capabilities_resolver(desired_capabilities, defaul_caps)
        return self._remote(desired_capabilities, remote_url, options=options)

    def _remote(self, desired_capabilities, remote_url,
                profile_dir=None, options=None):
        remote_url = str(remote_url)
        file_detector = self._get_sl_file_detector()
        return webdriver.Remote(command_executor=remote_url,
                                browser_profile=profile_dir, options=options,
                                file_detector=file_detector,
                                **desired_capabilities)

    def _get_sl_file_detector(self):
        # To ease unit testing.
        return SelLibLocalFileDetector()

    def _get_log_path(self, log_file):
        if is_noney(log_file):
            return None
        index = 1
        while True:
            formatted = _format_path(log_file, index)
            path = os.path.join(self.log_dir, formatted)
            # filename didn't contain {index} or unique path was found
            if formatted == log_file or not os.path.exists(path):
                return path
            index += 1

    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    def _normalise_browser_name(self, browser):
        return browser.lower().replace(' ', '')


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

    @property
    def active_driver_ids(self):
        open_driver_ids = []
        for index, driver in enumerate(self._connections):
            if driver not in self._closed:
                open_driver_ids.append(index + 1)
        return open_driver_ids

    @property
    def active_aliases(self):
        return self._aliases

    def close(self):
        if self.current:
            driver = self.current
            error = self._quit(driver, None)
            for alias in self._aliases:
                if self._aliases[alias] == self.current_index:
                    del self._aliases[alias]
            self.current = self._no_current
            self._closed.add(driver)
            if error:
                raise error

    def close_all(self):
        error = None
        for driver in self._connections:
            if driver not in self._closed:
                error = self._quit(driver, error)
        self.empty_cache()
        if error:
            raise error
        return self.current

    def _quit(self, driver, error):
        try:
            driver.quit()
        except Exception as exception:
            logger.error('When closing browser, received exception: %s' % exception)
            error = exception
        return error

    def get_index(self, alias_or_index):
        index = self._get_index(alias_or_index)
        try:
            driver = self.get_connection(index)
        except RuntimeError:
            return None
        return None if driver in self._closed else index

    def _get_index(self, alias_or_index):
        alias_or_index = None if is_noney(alias_or_index) else alias_or_index
        try:
            return self.resolve_alias_or_index(alias_or_index)
        except AttributeError:
            pass
        except ValueError:
            return None
        # TODO: This try/except block can be removed when minimum
        #  required Robot Framework version is 3.3 or greater.
        try:
            return self._resolve_alias_or_index(alias_or_index)
        except ValueError:
            return None


class SeleniumOptions(object):

    def create(self, browser, options):
        if is_falsy(options):
            return None
        selenium_options = self._import_options(browser)
        if not is_string(options):
            return options
        options = self._parse(options)
        selenium_options = selenium_options()
        for option in options:
            for key in option:
                attr = getattr(selenium_options, key)
                if callable(attr):
                    attr(*option[key])
                else:
                    setattr(selenium_options, key, *option[key])
        return selenium_options

    def _import_options(self, browser):
        if browser == 'android':
            browser = 'chrome'  # Android uses ChromeOptions()
        browser = browser.replace('headless_', '', 1)
        options = importlib.import_module('selenium.webdriver.%s.options' % browser)
        return options.Options

    def _parse(self, options):
        result = []
        for item in self._split(options):
            try:
                result.append(self._parse_to_tokens(item))
            except (ValueError, SyntaxError):
                raise ValueError('Unable to parse option: "%s"' % item)
        return result

    def _parse_to_tokens(self, item):
        result = {}
        index, method = self._get_arument_index(item)
        if index == -1:
            result[item] = []
            return result
        if method:
            args_as_string = item[index + 1:-1].strip()
            if args_as_string:
                args = ast.literal_eval(args_as_string)
            else:
                args = args_as_string
            is_tuple = args_as_string.startswith('(')
        else:
            args_as_string = item[index + 1:].strip()
            args = ast.literal_eval(args_as_string)
            is_tuple = args_as_string.startswith('(')
        method_or_attribute = item[:index].strip()
        result[method_or_attribute] = self._parse_arguments(args, is_tuple)
        return result

    def _parse_arguments(self, argument, is_tuple=False):
        if argument == '':
            return []
        if is_tuple:
            return [argument]
        if not is_tuple and isinstance(argument, tuple):
            return list(argument)
        return [argument]

    def _get_arument_index(self, item):
        if '=' not in item:
            return item.find('('), True
        if '(' not in item:
            return item.find('='), False
        index = min(item.find('('), item.find('='))
        return index, item.find('(') == index

    def _split(self, options):
        split_options = []
        start_position = 0
        tokens = generate_tokens(StringIO(options).readline)
        for toknum, tokval, tokpos, _, _ in tokens:
            if toknum == token.OP and tokval == ';':
                split_options.append(options[start_position:tokpos[1]].strip())
                start_position = tokpos[1] + 1
        split_options.append(options[start_position:])
        return split_options
