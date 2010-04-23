#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class Button(object):
    
    def select_checkbox(self, locator):
        """Selects checkbox identified by `locator`. 
        
        Does nothing if checkbox is already selected. Key attributes for 
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Selecting checkbox '%s'." % locator)
        locator = self._parse_locator(locator)
        if not self._selenium.is_checked(locator):
            self._selenium.check(locator)
            
    def unselect_checkbox(self, locator):
        """Removes selection of checkbox identified by `locator`. 
         
        Does nothing if the checkbox is not checked. Key attributes for 
        checkboxes are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Unselecting checkbox '%s'." % locator)
        locator = self._parse_locator(locator)
        if self._selenium.is_checked(locator):
            self._selenium.uncheck(locator)
             
    def checkbox_should_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is selected/checked.
        
        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._info("Verifying checkbox '%s' is selected." % locator)
        if not self._selenium.is_checked(self._parse_locator(locator)):
            raise AssertionError("Checkbox '%s' should have been selected but "
                                 "was not" % locator)
        
    def checkbox_should_not_be_selected(self, locator):
        """Verifies checkbox identified by `locator` is not selected/checked.
        
        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._info("Verifying checkbox '%s' is not selected." % locator)
        if self._selenium.is_checked(self._parse_locator(locator)):
            raise AssertionError("Checkbox '%s' should not have been selected"
                                  % locator)
        
    def select_radio_button(self, group_name, value, wait=''):
        """Sets selection of radio button group identified by `group_name` to `value`.
        
        See `introduction` for details about `wait` argument.
        """
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        xpath = "xpath=//input[@type='radio' and @name='%s' and (@value='%s' or @id='%s')]" \
                 % (group_name, value, value)
        if not self._selenium.is_checked(xpath):
            self._selenium.click(xpath)
            if wait:
                self._wait_for_page_to_load()
     
    def radio_button_should_be_set_to(self, group_name, value):
        """Verifies radio button group identified by `group_name` has its selection set to `value`."""
        self._info("Verifying radio button '%s' has selection '%s'." \
                   % (group_name, value))
        xpath = "xpath=//input[@type='radio' and @name='%s' and @value='%s']" \
                    % (group_name, value)
        if not self._selenium.is_checked(xpath):
            actual_value = self._get_value_of_selected_radio_button(group_name)
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'"  
                                  % (group_name, value, actual_value))
        
    def radio_button_should_not_be_selected(self, group_name):
        """Verifies radio button group identified by `group_name` has no selection."""
        self._info("Verifying radio button '%s' has no selection." % group_name)
        value = self._get_value_of_selected_radio_button(group_name)
        if value:
            raise AssertionError("Radio button group '%s' should not have had "
                                 "selection, but '%s' was selected" 
                                  % (group_name, value))

    def _get_number_of_radio_buttons_in_group(self, group_name):
        js = "window.document.getElementsByName('%s').length" % group_name
        return int(self._selenium.get_eval(js))
    
    def _get_value_of_selected_radio_button(self, group_name):
        num = self._get_number_of_radio_buttons_in_group(group_name)    
        for i in range(num):
            xpath = "xpath=//input[@name='%s'][%d]" % (group_name, i+1)
            if self._selenium.is_checked(xpath):
                return self._selenium.get_attribute(xpath+'@value')
        return ''

