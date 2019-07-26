import unittest

from mockito import mock, unstub, when

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords.webdrivertools.sl_file_detector import SelLibLocalFileDetector


class InputTextFileDecorator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = SelLibLocalFileDetector()

    def tearDown(self):
        unstub()

    def test_running_keyword(self):
        sl = SeleniumLibrary()
        driver = mock()
        sl.register_driver(driver, 'alias1')
        self.assertEqual(sl._running_keyword, None)

        when(driver).find_elements_by_xpath('//div').thenReturn([mock()])
        sl.run_keyword('page_should_contain_element', ['xpath://div'], {})
        self.assertEqual(sl._running_keyword, None)

    def test_file_decorator_not_file(self):
        when(self.file).choose_file().thenReturn(False)
        self.assertEqual(self.file.is_local_file('some string'), None)

    def test_file_decodator_is_file_choose_file(self):
        when(self.file).choose_file().thenReturn(True)
        self.assertEqual(self.file.is_local_file('some_file'), None)
