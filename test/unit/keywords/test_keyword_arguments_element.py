import unittest

from mockito import mock, unstub, when

from SeleniumLibrary.keywords import ElementKeywords


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.element = ElementKeywords(ctx)

    def tearDown(self):
        unstub()

    def test_element_should_contain(self):
        locator = '//div'
        actual = 'bar'
        expected = 'foo'
        when(self.element)._get_text(locator).thenReturn(actual)
        message = ("Element '%s' should have contained text '%s' but "
                   "its text was '%s'." % (locator, expected, actual))
        with self.assertRaises(AssertionError) as error:
            self.element.element_should_contain('//div', expected)
            self.assertEqual(str(error), message)

        with self.assertRaises(AssertionError) as error:
            self.element.element_should_contain('//div', expected, 'foobar')
            self.assertEqual(str(error), 'foobar')

    def test_element_should_not_contain(self):
        locator = '//div'
        actual = 'bar'
        when(self.element)._get_text(locator).thenReturn(actual)
        message = ("Element '%s' should not contain text '%s' but "
                   "it did." % (locator, actual))
        with self.assertRaises(AssertionError) as error:
            self.element.element_should_not_contain('//div', actual)
            self.assertEqual(str(error), message)

        with self.assertRaises(AssertionError) as error:
            self.element.element_should_not_contain('//div', actual, 'foobar')
            self.assertEqual(str(error), 'foobar')

    def test_locator_should_match_x_times(self):
        locator = '//div'
        when(self.element).find_element(locator, required=False,
                                        first_only=False).thenReturn([])
        with self.assertRaisesRegexp(AssertionError, 'should have matched'):
            self.element.locator_should_match_x_times(locator, 1)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.locator_should_match_x_times(locator, 1, 'foobar')

    def test_element_should_be_visible(self):
        locator = '//div'
        when(self.element).is_visible(locator).thenReturn(None)
        with self.assertRaisesRegexp(AssertionError, 'should be visible'):
            self.element.element_should_be_visible(locator)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.element_should_be_visible(locator, 'foobar')

    def test_element_should_not_be_visible(self):
        locator = '//div'
        when(self.element).is_visible(locator).thenReturn(True)
        with self.assertRaisesRegexp(AssertionError, 'should not be visible'):
            self.element.element_should_not_be_visible(locator)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.element_should_not_be_visible(locator, 'foobar')

    def test_element_text_should_be(self):
        locator = '//div'
        element = mock()
        element.text = 'text'
        when(self.element).find_element(locator).thenReturn(element)
        with self.assertRaisesRegexp(AssertionError, 'should have been'):
            self.element.element_text_should_be(locator, 'not text')

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.element_text_should_be(locator, 'not text', 'foobar')

    def test_get_element_attribute(self):
        locator = '//div'
        attrib = 'id'
        element = mock()
        when(self.element).find_element(locator,
                                        required=False).thenReturn(element)
        when(element).get_attribute(attrib).thenReturn('value')
        value = self.element.get_element_attribute(locator, attrib)
        self.assertEqual(value, 'value')

        locator = '//div@id'
        value = self.element.get_element_attribute(locator, 'None')
        self.assertEqual(value, 'value')

    def test_get_matching_xpath_count(self):
        locator = '//div'
        when(self.element).find_element(
            'xpath={}'.format(locator), first_only=False,
            required=False).thenReturn([])
        count = self.element.get_matching_xpath_count(locator)
        self.assertEqual(count, '0')
        count = self.element.get_matching_xpath_count(locator, 'True')
        self.assertEqual(count, '0')

        count = self.element.get_matching_xpath_count(locator, 'False')
        self.assertEqual(count, 0)

    def test_xpath_should_match_x_times(self):
        locator = '//div'
        when(self.element).find_element(
            'xpath={}'.format(locator), first_only=False,
            required=False).thenReturn([])
        with self.assertRaisesRegexp(AssertionError, 'should have matched'):
            self.element.xpath_should_match_x_times(locator, 1)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.xpath_should_match_x_times(locator, 1, 'foobar')
