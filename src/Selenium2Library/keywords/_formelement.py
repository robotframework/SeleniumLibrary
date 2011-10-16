import os
from keywordgroup import KeywordGroup

class _FormElementKeywords(KeywordGroup):

    # Public, form

    def submit_form(self, locator=None):
        self._info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        element = self._element_find(locator, True, True, 'form')
        element.submit()

    # Public, checkboxes

    def checkbox_should_be_selected(self, locator):
        self._info("Verifying checkbox '%s' is selected." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            raise AssertionError("Checkbox '%s' should have been selected "
                                 "but was not" % locator)

    def checkbox_should_not_be_selected(self, locator):
        self._info("Verifying checkbox '%s' is not selected." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            raise AssertionError("Checkbox '%s' should not have been selected"
                                  % locator)

    def page_should_contain_checkbox(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_not_contain_checkbox(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'checkbox', message, loglevel)

    def select_checkbox(self, locator):
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    def unselect_checkbox(self, locator):
        self._info("Unselecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            element.click()

    # Public, radio buttons

    def page_should_contain_radio_button(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'radio button', message, loglevel)

    def page_should_not_contain_radio_button(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'radio button', message, loglevel)

    def radio_button_should_be_set_to(self, group_name, value):
        self._info("Verifying radio button '%s' has selection '%s'." \
                   % (group_name, value))
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is None or actual_value != value:
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'"
                                  % (group_name, value, actual_value))

    def radio_button_should_not_be_selected(self, group_name):
        self._info("Verifying radio button '%s' has no selection." % group_name)
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is not None:
            raise AssertionError("Radio button group '%s' should not have had "
                                 "selection, but '%s' was selected"
                                  % (group_name, actual_value))

    def select_radio_button(self, group_name, value):
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    # Public, text fields

    def choose_file(self, locator, file_path):
        if not os.path.isfile(file_path):
            self._info("File '%s' does not exist on the local file system"
                        % file_path)
        self._element_find(locator, True, True).send_keys(file_path)

    def input_password(self, locator, text):
        self._info("Typing password into text field '%s'" % locator)
        self._input_text_into_text_field(locator, text)

    def input_text(self, locator, text):
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._input_text_into_text_field(locator, text)

    def page_should_contain_textfield(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'text field', message, loglevel)

    def page_should_not_contain_textfield(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'text field', message, loglevel)

    def textfield_should_contain(self, locator, expected, message=''):
        actual = self._get_value(locator, 'text field')
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def textfield_value_should_be(self, locator, expected, message=''):
        element = self._element_find(locator, True, False, 'text field')
        if element is None: element = self._element_find(locator, True, False, 'file upload')
        actual = element.get_attribute('value') if element is not None else None
        if actual != expected:
            if not message:
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Content of text field '%s' is '%s'." % (locator, expected))

    # Public, buttons

    def click_button(self, locator):
        self._info("Clicking button '%s'." % locator)
        element = self._element_find(locator, True, False, 'input')
        if element is None:
            element = self._element_find(locator, True, True, 'button')
        element.click()

    def page_should_contain_button(self, locator, message='', loglevel='INFO'):
        try:
            self._page_should_contain_element(locator, 'input', message, loglevel)
        except AssertionError:
            self._page_should_contain_element(locator, 'button', message, loglevel)

    def page_should_not_contain_button(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'button', message, loglevel)
        self._page_should_not_contain_element(locator, 'input', message, loglevel)

    # Private

    def _get_checkbox(self, locator):
        return self._element_find(locator, True, True, tag='input')

    def _get_radio_buttons(self, group_name):
        xpath = "xpath=//input[@type='radio' and @name='%s']" % group_name
        self._debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, False, True)

    def _get_radio_button_with_value(self, group_name, value):
        xpath = "xpath=//input[@type='radio' and @name='%s' and (@value='%s' or @id='%s')]" \
                 % (group_name, value, value)
        self._debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, True, True)

    def _get_value_from_radio_buttons(self, elements):
        for element in elements:
            if element.is_selected():
                return element.get_attribute('value')
        return None

    def _input_text_into_text_field(self, locator, text):
        element = self._element_find(locator, True, True)
        element.clear()
        element.send_keys(text)

    def _is_form_element(self, element):
        if element is None:
            return False
        tag = element.tag_name.lower()
        return tag == 'input' or tag == 'select' or tag == 'textarea' or tag == 'button'