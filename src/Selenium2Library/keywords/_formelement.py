import os
from keywordgroup import KeywordGroup

class _FormElementKeywords(KeywordGroup):

    # Public, form

    def submit_form(self, locator=None):
        """Submits a form identified by `locator`.

        If `locator` is empty, first form in the page will be submitted.
        Key attributes for forms are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        element = self._element_find(locator, True, True, 'form')
        element.submit()

    # Public, checkboxes

    def checkbox_should_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is selected/checked.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._info("Verifying checkbox '%s' is selected." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            raise AssertionError("Checkbox '%s' should have been selected "
                                 "but was not" % locator)

    def checkbox_should_not_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is not selected/checked.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._info("Verifying checkbox '%s' is not selected." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            raise AssertionError("Checkbox '%s' should not have been selected"
                                  % locator)

    def page_should_contain_checkbox(self, locator, message='', loglevel='INFO'):
        """Verifies checkbox identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_not_contain_checkbox(self, locator, message='', loglevel='INFO'):
        """Verifies checkbox identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'checkbox', message, loglevel)

    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`.

        Does nothing if checkbox is already selected. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    def unselect_checkbox(self, locator):
        """Removes selection of checkbox identified by `locator`.

        Does nothing if the checkbox is not checked. Key attributes for
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Unselecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            element.click()

    # Public, radio buttons

    def page_should_contain_radio_button(self, locator, message='', loglevel='INFO'):
        """Verifies radio button identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'radio button', message, loglevel)

    def page_should_not_contain_radio_button(self, locator, message='', loglevel='INFO'):
        """Verifies radio button identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'radio button', message, loglevel)

    def radio_button_should_be_set_to(self, group_name, value):
        """Verifies radio button group identified by `group_name` has its selection set to `value`.

        See `Select Radio Button` for information about how radio buttons are
        located.
        """
        self._info("Verifying radio button '%s' has selection '%s'." \
                   % (group_name, value))
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is None or actual_value != value:
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'"
                                  % (group_name, value, actual_value))

    def radio_button_should_not_be_selected(self, group_name):
        """Verifies radio button group identified by `group_name` has no selection.

        See `Select Radio Button` for information about how radio buttons are
        located.
        """
        self._info("Verifying radio button '%s' has no selection." % group_name)
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is not None:
            raise AssertionError("Radio button group '%s' should not have had "
                                 "selection, but '%s' was selected"
                                  % (group_name, actual_value))

    def select_radio_button(self, group_name, value):
        """Sets selection of radio button group identified by `group_name` to `value`.

        The radio button to be selected is located by two arguments:
        - `group_name` is used as the name of the radio input
        - `value` is used for the value attribute or for the id attribute

        The XPath used to locate the correct radio button then looks like this:
        //input[@type='radio' and @name='group_name' and (@value='value' or @id='value')]

        Examples:
        | Select Radio Button | size | XL | # Matches HTML like <input type="radio" name="size" value="XL">XL</input> |
        | Select Radio Button | size | sizeXL | # Matches HTML like <input type="radio" name="size" value="XL" id="sizeXL">XL</input> |
        """
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    # Public, text fields

    def choose_file(self, locator, file_path):
        """Inputs the `file_path` into file input field found by `identifier`.

        This keyword is most often used to input files into upload forms.
        The file specified with `file_path` must be available on the same host 
        where the Selenium Server is running.

        Example:
        | Choose File | my_upload_field | /home/user/files/trades.csv |
        """
        if not os.path.isfile(file_path):
            self._info("File '%s' does not exist on the local file system"
                        % file_path)
        self._element_find(locator, True, True).send_keys(file_path)

    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        self._input_text_into_text_field(locator, text)

    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._input_text_into_text_field(locator, text)

    def page_should_contain_textfield(self, locator, message='', loglevel='INFO'):
        """Verifies text field identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'text field', message, loglevel)

    def page_should_not_contain_textfield(self, locator, message='', loglevel='INFO'):
        """Verifies text field identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'text field', message, loglevel)

    def textfield_should_contain(self, locator, expected, message=''):
        """Verifies text field identified by `locator` contains text `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self._get_value(locator, 'text field')
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def textfield_value_should_be(self, locator, expected, message=''):
        """Verifies the value in text field identified by `locator` is exactly `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
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
        """Clicks a button identified by `locator`.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking button '%s'." % locator)
        element = self._element_find(locator, True, False, 'input')
        if element is None:
            element = self._element_find(locator, True, True, 'button')
        element.click()

    def page_should_contain_button(self, locator, message='', loglevel='INFO'):
        """Verifies button identified by `locator` is found from current page.

        This keyword searches for buttons created with either `input` or `button` tag.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        try:
            self._page_should_contain_element(locator, 'input', message, loglevel)
        except AssertionError:
            self._page_should_contain_element(locator, 'button', message, loglevel)

    def page_should_not_contain_button(self, locator, message='', loglevel='INFO'):
        """Verifies button identified by `locator` is not found from current page.

        This keyword searches for buttons created with either `input` or `button` tag.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
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