import unittest

from mockito import mock, unstub, when

from SeleniumLibrary.keywords import FormElementKeywords


FALSES = ['False', False, '', None, 'NONE']


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.form = FormElementKeywords(ctx)
        self.ctx = ctx

    def tearDown(self):
        unstub()

    def test_submit_form_false(self):
        element = mock()
        when(self.form).find_element('xpath=//form',
                                     tag='form').thenReturn(element)
        for false in FALSES:
            self.form.submit_form()
        self.form.submit_form()

    def test_submit_form_true(self):
        element = mock()
        when(self.form).find_element('//form', tag='form').thenReturn(element)
        self.form.submit_form('//form')

    def test_textfield_should_contain(self):
        locator = '//input'
        self.ctx.element_finder = mock()
        when(self.ctx.element_finder).get_value(locator,
                                                'text field').thenReturn('no')
        with self.assertRaisesRegexp(AssertionError, 'should have contained'):
            self.form.textfield_should_contain(locator, 'text')

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.form.textfield_should_contain(locator, 'text', 'foobar')

    def test_textfield_value_should_be(self):
        locator = '//input'
        element = mock()
        when(self.form).find_element(locator, tag='text field',
                                     required=False).thenReturn(element)
        when(element).get_attribute('value').thenReturn('no')
        with self.assertRaisesRegexp(AssertionError, 'text field'):
            self.form.textfield_value_should_be(locator, 'value')
        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.form.textfield_value_should_be(locator, 'value', 'foobar err')

    def test_textarea_should_contain(self):
        locator = '//input'
        self.ctx.element_finder = mock()
        when(self.ctx.element_finder).get_value(locator,
                                                'text area').thenReturn('no')
        with self.assertRaisesRegexp(AssertionError, 'should have contained'):
            self.form.textarea_should_contain(locator, 'value')
        with self.assertRaisesRegexp(AssertionError, 'foobar error'):
            self.form.textarea_should_contain(locator, 'value', 'foobar error')

    def test_textarea_value_should_be(self):
        locator = '//input'
        self.ctx.element_finder = mock()
        when(self.ctx.element_finder).get_value(locator,
                                                'text area').thenReturn('no')
        with self.assertRaisesRegexp(AssertionError, 'should have been'):
            self.form.textfield_value_should_be(locator, 'value')
        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.form.textfield_value_should_be(locator, 'value', 'foobar')
