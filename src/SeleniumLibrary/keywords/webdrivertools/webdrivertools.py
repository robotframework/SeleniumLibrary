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
from io import StringIO
from tokenize import generate_tokens

from robot.api import logger
from robot.utils import ConnectionCache
from selenium import webdriver
from selenium.webdriver import FirefoxProfile

from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IeService
from selenium.webdriver.safari.service import Service as SafariService

from SeleniumLibrary.keywords.webdrivertools.sl_file_detector import (
    SelLibLocalFileDetector,
)
from SeleniumLibrary.utils.path_formatter import _format_path


class WebDriverCreator:

    browser_names = {
        "googlechrome": "chrome",
        "gc": "chrome",
        "chrome": "chrome",
        "headlesschrome": "headless_chrome",
        "ff": "firefox",
        "firefox": "firefox",
        "headlessfirefox": "headless_firefox",
        "ie": "ie",
        "internetexplorer": "ie",
        "edge": "edge",
        "safari": "safari",
    }

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.selenium_options = SeleniumOptions()
        #self.selenium_service = SeleniumService()

    def create_driver(
        self,
        browser,
        desired_capabilities,
        remote_url,
        profile_dir=None,
        options=None,
        service_log_path=None,
        executable_path=None,
    ):
        browser = self._normalise_browser_name(browser)
        creation_method = self._get_creator_method(browser)
        desired_capabilities = self._parse_capabilities(desired_capabilities, browser)
        service_log_path = self._get_log_path(service_log_path)
        options = self.selenium_options.create(self.browser_names.get(browser), options)
        if service_log_path:
            logger.info(f"Browser driver log file created to: {service_log_path}")
            self._create_directory(service_log_path)
        if (
            creation_method == self.create_firefox
            or creation_method == self.create_headless_firefox
        ):
            return creation_method(
                desired_capabilities,
                remote_url,
                profile_dir,
                options=options,
                service_log_path=service_log_path,
                executable_path=executable_path,
            )
        return creation_method(
            desired_capabilities,
            remote_url,
            options=options,
            service_log_path=service_log_path,
            executable_path=executable_path,
        )

    def _get_creator_method(self, browser):
        if browser in self.browser_names:
            return getattr(self, f"create_{self.browser_names[browser]}")
        raise ValueError(f"{browser} is not a supported browser.")

    def _parse_capabilities(self, capabilities, browser=None):
        if not capabilities:
            return {}
        if not isinstance(capabilities, dict):
            capabilities = self._string_to_dict(capabilities)
        browser = self.browser_names.get(browser, browser)
        if browser in ["ie", "firefox", "edge"]:
            return {"capabilities": capabilities}
        return {"desired_capabilities": capabilities}

    def _string_to_dict(self, capabilities):
        desired_capabilities = {}
        for part in capabilities.split(","):
            key, value = part.split(":")
            desired_capabilities[key.strip()] = value.strip()
        return desired_capabilities

    def _remote_capabilities_resolver(self, set_capabilities, default_capabilities):
        if not set_capabilities:
            return {"desired_capabilities": default_capabilities}
        if "capabilities" in set_capabilities:
            caps = set_capabilities["capabilities"]
        else:
            caps = set_capabilities["desired_capabilities"]
        if "browserName" not in caps:
            caps["browserName"] = default_capabilities["browserName"]
        return {"desired_capabilities": caps}

    def _get_log_method(self, service_cls, service_log_path):
        # -- temporary fix to transition selenium to v4.13 from v4.11 and prior
        from inspect import signature
        sig = signature(service_cls)
        if 'log_output' in str(sig):
            return {'log_output': service_log_path}
        else:
            return {'log_path': service_log_path}
        # --

    def create_chrome(
        self,
        desired_capabilities,
        remote_url,
        options=None,
        service_log_path=None,
        executable_path="chromedriver",
    ):
        if remote_url:
            if not options:
                options = webdriver.ChromeOptions()
            return self._remote(remote_url, options=options)
        if not executable_path:
            executable_path = self._get_executable_path(webdriver.chrome.service.Service)
        log_method = self._get_log_method(ChromeService, service_log_path)
        service = ChromeService(executable_path=executable_path, **log_method)
        return webdriver.Chrome(
            options=options,
            service=service,
        )

    def create_headless_chrome(
        self,
        desired_capabilities,
        remote_url,
        options=None,
        service_log_path=None,
        executable_path="chromedriver",
    ):
        if not options:
            options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        return self.create_chrome(
            desired_capabilities, remote_url, options, service_log_path, executable_path
        )

    def _get_executable_path(self, webdriver):
        signature = inspect.signature(webdriver.__init__)
        parameters = signature.parameters
        executable_path = parameters.get("executable_path")
        if not executable_path:
            return None
        return executable_path.default

    def create_firefox(
        self,
        desired_capabilities,
        remote_url,
        ff_profile_dir,
        options=None,
        service_log_path=None,
        executable_path="geckodriver",
    ):
        profile = self._get_ff_profile(ff_profile_dir)
        if not options:
            options = webdriver.FirefoxOptions()
        options.profile = profile  # <- moved to here :)

        # Something I question here is/was whether or not we should create the option, not
        # only on whether it exists, but if there is a profile provided. That is previously we just pass
        # None along as options if there were none. But now no matter what we create an Options class so
        # as to attach the profile to it. If there a scenario in which we don't want to do this???

        if remote_url:
            return self._remote(remote_url, options)
        if not executable_path:
            executable_path = self._get_executable_path(webdriver.firefox.service.Service)
        log_method = self._get_log_method(FirefoxService, service_log_path or self._geckodriver_log)
        service = FirefoxService(executable_path=executable_path, **log_method)
        return webdriver.Firefox(
            options=options,
            service=service,
        )

    def _get_ff_profile(self, ff_profile_dir):
        if isinstance(ff_profile_dir, FirefoxProfile):
            return ff_profile_dir
        if not ff_profile_dir:
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
        log_file = self._get_log_path(
            os.path.join(self.log_dir, "geckodriver-{index}.log")
        )
        logger.trace(f"Firefox driver log is always forced to to: {log_file}")
        return log_file

    def create_headless_firefox(
        self,
        desired_capabilities,
        remote_url,
        ff_profile_dir,
        options=None,
        service_log_path=None,
        executable_path="geckodriver",
    ):
        if not options:
            options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        return self.create_firefox(
            desired_capabilities,
            remote_url,
            ff_profile_dir,
            options,
            service_log_path,
            executable_path,
        )

    def create_ie(
        self,
        desired_capabilities,
        remote_url,
        options=None,
        service_log_path=None,
        executable_path="IEDriverServer.exe",
    ):
        if remote_url:
            if not options:
                options = webdriver.IeOptions()
            return self._remote(remote_url, options=options)
        if not executable_path:
            executable_path = self._get_executable_path(webdriver.ie.service.Service)
        log_method = self._get_log_method(IeService, service_log_path)
        service = IeService(executable_path=executable_path, **log_method)
        return webdriver.Ie(
            options=options,
            service=service,
            #**desired_capabilities,
        )

    def _has_options(self, web_driver):
        signature = inspect.signature(web_driver.__init__)
        return "options" in signature.parameters

    def create_edge(
        self,
        desired_capabilities,
        remote_url,
        options=None,
        service_log_path=None,
        executable_path="msedgedriver",
    ):
        if remote_url:
            if not options:
                options = webdriver.EdgeOptions()
            return self._remote(remote_url, options=options)
        if not executable_path:
            executable_path = self._get_executable_path(webdriver.edge.service.Service)
        log_method = self._get_log_method(EdgeService, service_log_path)
        service = EdgeService(executable_path=executable_path, **log_method)
        return webdriver.Edge(
            options=options,
            service=service,
            #**desired_capabilities,
        )

    def create_safari(
        self,
        desired_capabilities,
        remote_url,
        options=None,
        service_log_path=None,
        executable_path="/usr/bin/safaridriver",
    ):
        if remote_url:
            if not options:
                options = webdriver.SafariOptions()
            return self._remote(remote_url, options=options)
        if not executable_path:
            executable_path = self._get_executable_path(webdriver.Safari)
        log_method = self._get_log_method(SafariService, service_log_path)
        service = SafariService(executable_path=executable_path, **log_method)
        return webdriver.Safari(options=options, service=service)

    def _remote(self, remote_url, options):
        remote_url = str(remote_url)
        file_detector = self._get_sl_file_detector()
        return webdriver.Remote(
            command_executor=remote_url,
            options=options,
            file_detector=file_detector,
        )

    def _get_sl_file_detector(self):
        # To ease unit testing.
        return SelLibLocalFileDetector()

    def _get_log_path(self, log_file):
        if log_file is None:
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
        return browser.lower().replace(" ", "")


class WebDriverCache(ConnectionCache):
    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg="No current browser")
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
            logger.error(f"When closing browser, received exception: {exception}")
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

# Temporarily removing as not going to use with initial 4.10.0 hotfixq
# class SeleniumService:
#     """        executable_path: str = DEFAULT_EXECUTABLE_PATH,
#         port: int = 0,
#         log_path: typing.Optional[str] = None,
#         service_args: typing.Optional[typing.List[str]] = None,
#         env: typing.Optional[typing.Mapping[str, str]] = None,
#         **kwargs,

#         executable_path = None, port, service_log_path, service_args, env
#     """
#     def create(self, browser,
#         executable_path=None,
#         port=0,
#         service_log_path=None,
#         service_args=None,
#         env=None,
#         start_error_message=None,    # chromium, chrome, edge
#         quiet=False, reuse_service=False,   # safari
#     ):
#         selenium_service = self._import_service(browser)
#         # chrome, chromium, firefox, edge
#         if any(chromium_based in browser.lower() for chromium_based in ('chromium', 'chrome', 'edge')):
#             service = selenium_service(executable_path=executable_path, port=port,log_path=service_log_path,
#                                        service_args=service_args,env=env,start_error_message=start_error_message
#             )
#             return service
#         elif 'safari' in browser.lower():
#             service = selenium_service(executable_path=executable_path, port=port,log_path=service_log_path,
#                                        service_args=service_args,env=env,quiet=quiet,reuse_service=reuse_service
#             )
#             return service
#         elif 'firefox' in browser.lower():
#             service = selenium_service(executable_path=executable_path, port=port,log_path=service_log_path,
#                                        service_args=service_args,env=env
#             )
#             return service
#         else:
#             service = selenium_service(executable_path=executable_path, port=port,log_path=service_log_path,
#                                        service_args=service_args,env=env
#             )
#             return service

#     def _import_service(self, browser):
#         browser = browser.replace("headless_", "", 1)
#         service = importlib.import_module(f"selenium.webdriver.{browser}.service")
#         return service.Service

class SeleniumOptions:
    def create(self, browser, options):
        if not options:
            return None
        selenium_options = self._import_options(browser)
        if not isinstance(options, str):
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
        browser = browser.replace("headless_", "", 1)
        options = importlib.import_module(f"selenium.webdriver.{browser}.options")
        return options.Options

    def _parse(self, options):
        result = []
        for item in self._split(options):
            try:
                result.append(self._parse_to_tokens(item))
            except (ValueError, SyntaxError):
                raise ValueError(f'Unable to parse option: "{item}"')
        return result

    def _parse_to_tokens(self, item):
        result = {}
        index, method = self._get_arument_index(item)
        if index == -1:
            result[item] = []
            return result
        if method:
            args_as_string = item[index + 1 : -1].strip()
            if args_as_string:
                args = ast.literal_eval(args_as_string)
            else:
                args = args_as_string
            is_tuple = args_as_string.startswith("(")
        else:
            args_as_string = item[index + 1 :].strip()
            args = ast.literal_eval(args_as_string)
            is_tuple = args_as_string.startswith("(")
        method_or_attribute = item[:index].strip()
        result[method_or_attribute] = self._parse_arguments(args, is_tuple)
        return result

    def _parse_arguments(self, argument, is_tuple=False):
        if argument == "":
            return []
        if is_tuple:
            return [argument]
        if not is_tuple and isinstance(argument, tuple):
            return list(argument)
        return [argument]

    def _get_arument_index(self, item):
        if "=" not in item:
            return item.find("("), True
        if "(" not in item:
            return item.find("="), False
        index = min(item.find("("), item.find("="))
        return index, item.find("(") == index

    def _split(self, options):
        split_options = []
        start_position = 0
        tokens = generate_tokens(StringIO(options).readline)
        for toknum, tokval, tokpos, _, _ in tokens:
            if toknum == token.OP and tokval == ";":
                split_options.append(options[start_position : tokpos[1]].strip())
                start_position = tokpos[1] + 1
        split_options.append(options[start_position:])
        return split_options
