import unittest

from mockito import mock, unstub, when, verify

from SeleniumLibrary.locators.elementfinder import ElementFinder


class FindElementAndElementsTests(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.find = ElementFinder(self.ctx)

    def tearDown(self):
        unstub()

    def test_find_element_single(self):
        element1 = mock()
        when(self.find).find(locator='xpath://div', tag=None, required=True,
                             parent=None).thenReturn([element1])
        element = self.find.find_element('xpath://div')
        verify(self.find, times=1).find(locator='xpath://div', tag=None,
                                        required=True, parent=None)
        self.assertEqual(element, element1)

    def test_find_element_multiple(self):
        element1, element2 = mock(), mock()
        when(self.find).find(locator='xpath://td', tag=None, required=True,
                             parent=None).thenReturn([element1, element2])
        message = ('Multiple elements found with locator "xpath://td", '
                   'but only one should have been found.')
        when(self.find)._warn(message).thenReturn(None)
        element = self.find.find_element('xpath://td')
        self.assertEqual(element, element1)
        verify(self.find, times=1)._warn(message)

    def test_find_elements_single(self):
        element1 = mock()
        when(self.find).find(locator='xpath://div', tag=None, first_only=False,
                             parent=None, required=False).thenReturn([element1])
        element = self.find.find_elements('xpath://div')
        verify(self.find, times=1).find(locator='xpath://div', tag=None,
                                        first_only=False, parent=None,
                                        required=False)
        self.assertEqual(element, [element1])

    def test_find_elements_multiple(self):
        element1, element2 = mock(), mock()
        when(self.find).find(locator='xpath://div', tag=None, first_only=False,
                             parent=None, required=False).thenReturn([element1,
                                                                      element2])
        message = ('Multiple elements found with locator "xpath://div", '
                   'but only one should have been found.')
        when(self.find)._warn(message).thenReturn(None)
        element = self.find.find_elements('xpath://div')
        verify(self.find, times=1).find(locator='xpath://div', tag=None,
                                        first_only=False, parent=None,
                                        required=False)
        self.assertEqual(element, [element1, element2])
        verify(self.find, times=0)._warn(message)
