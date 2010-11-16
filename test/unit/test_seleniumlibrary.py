import unittest
import os

from SeleniumLibrary import (SeleniumLibrary, _server_startup_command,
                             _command_line_args_for_server,
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
        self.assertEquals(_command_line_args_for_server(),
                          [FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR])

    def test_given_profile_is_not_overridden(self):
        self.assertEquals(_command_line_args_for_server(FIREFOX_TEMPLATE_ARG, 'foo'),
                          [FIREFOX_TEMPLATE_ARG, 'foo'])

    def test_real_default_profile_can_be_used(self):
        self.assertEquals(_command_line_args_for_server(FIREFOX_TEMPLATE_ARG,FIREFOX_DEFAULT_PROFILE), [])

    def test_other_options_are_preserved(self):
        self.assertEquals(_command_line_args_for_server('-someOpt', 'value', '-otherOpt'),
                          ['-someOpt', 'value', '-otherOpt', FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR])


if __name__ == "__main__":
    unittest.main()
