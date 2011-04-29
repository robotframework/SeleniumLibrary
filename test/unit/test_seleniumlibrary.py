import unittest
import os

from SeleniumLibrary import (SeleniumLibrary, _server_startup_command,
                             _server_startup_params,
                             FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR,
                             FIREFOX_DEFAULT_PROFILE, SELENIUM_SERVER_PATH)


class TestGetBrowser(unittest.TestCase):

    def setUp(self):
        self.lib = SeleniumLibrary()

    def test_ie_aliases(self):
        for alias in ['ie', 'IE', 'Internet Explorer', 'INTernETexplOrEr']:
            self.assertEquals(self.lib._get_browser(alias), '*iexplore')

    def test_firefox_aliases(self):
        for alias in ['ff', 'FF', 'firefox', 'FireFox']:
            self.assertEquals(self.lib._get_browser(alias), '*firefox')

    def test_non_alias_is_not_modified(self):
        for non_alias in ['FIREFUX', 'i e 8', 'C:\\Program Files\\mybrowser\\brow.exe',
                          '{"username": "user", "access-key": "7A9cea40-84f7-4d3b-8748-0e94fCd4dX4f"}']:
            self.assertEquals(self.lib._get_browser(non_alias), non_alias)

    def test_patched_remote_control(self):
        rc_path = os.path.join(os.path.dirname(__file__), '..', '..', 'src',
                               'SeleniumLibrary', 'selenium.py')
        self.assertTrue('conn.close()' in open(rc_path).read())



class TestServerArguments(unittest.TestCase):

    def test_default_jar_path_is_correctly_determined(self):
        self.assertEquals(_server_startup_command(None)[:3],
                          ['java', '-jar', SELENIUM_SERVER_PATH])

    def test_given_jar_path_is_used(self):
        self.assertEquals(_server_startup_command('/some/jar.jar')[:3],
                          ['java', '-jar', '/some/jar.jar'])

    def test_selenium_lib_default_profile_is_used_when_no_profile_given(self):
        self.assertEquals(_server_startup_params([]),
                          [FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR])

    def test_given_profile_is_not_overridden(self):
        self.assertEquals(_server_startup_params([FIREFOX_TEMPLATE_ARG, 'foo']),
                          [FIREFOX_TEMPLATE_ARG, 'foo'])

    def test_real_default_profile_can_be_used(self):
        params = [FIREFOX_TEMPLATE_ARG,FIREFOX_DEFAULT_PROFILE]
        self.assertEquals(_server_startup_params(params), [])

    def test_other_options_are_preserved(self):
        params = ['-someOpt', 'value', '-otherOpt']
        self.assertEquals(_server_startup_params(params),
                          ['-someOpt', 'value', '-otherOpt', FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR])


class TestInitialization(unittest.TestCase):

    def test_host_and_port_have_default_values(self):
        self._verify_host_and_port(SeleniumLibrary(), 'localhost', 4444)

    def test_host_and_port_can_be_given_separately(self):
        lib = SeleniumLibrary(server_host='1.2.3.4', server_port='1234')
        self._verify_host_and_port(lib, '1.2.3.4', 1234)

    def test_protocol_is_ignored_in_host(self):
        lib = SeleniumLibrary(server_host='http://1.2.3.4')
        self._verify_host_and_port(lib, '1.2.3.4', 4444)

    def test_port_can_be_given_as_part_of_host(self):
        lib = SeleniumLibrary(server_host='http://1.2.3.4:8001')
        self._verify_host_and_port(lib, '1.2.3.4', 8001)
        lib = SeleniumLibrary(server_host='127.0.0.1:1000')
        self._verify_host_and_port(lib, '127.0.0.1', 1000)

    def test_port_given_as_part_of_host_overrides_possible_port(self):
        lib = SeleniumLibrary(server_host='http://1.2.3.4:8001', server_port='1234')
        self._verify_host_and_port(lib, '1.2.3.4', 8001)

    def _verify_host_and_port(self, lib, host, port):
        self.assertEquals(lib._server_host, host)
        self.assertEquals(lib._server_port, port)


if __name__ == "__main__":
    unittest.main()
