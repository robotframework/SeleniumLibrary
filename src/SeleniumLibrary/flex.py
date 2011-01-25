#  Copyright 2008-2011 Nokia Siemens Networks Oyj
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

import time

from runonfailure import RunOnFailure


class NoFlexApplicationSelected(Exception):
    pass


class Flex(RunOnFailure):
    _flex_app = None
    # First locator is the default
    _flex_element_locators = ['id=', 'name=', 'automationName=', 'label=',
                              'text=', 'htmlText=', 'chain=']
    _flex_select_locators = ['label=', 'index=', 'text=', 'data=', 'value=']


    def select_flex_application(self, locator):
        """Selects Flex application to work with and waits until it is active.

        All further Flex keywords will operate on the selected application and
        thus you *must always* use this keyword before them. You must also use
        this keyword when you want to operate another Flex application.

        Because this keyword waits until the selected application is active,
        it is recommended to use this if the page where the application is
        located is reloaded. The timeout used is the same Selenium timeout that
        can be set in `importing` and with `Set Selenium Timeout` keyword.

        The application is found using `locator` that must be either `id` or
        `name` of the application in HTML. Notice that if you have different
        elements for different browsers (<object> vs. <embed>), you need to
        use different attributes depending on the browser.

        Example:
        | Select Flex Application     | exampleFlexApp |
        | Click Flex Element          | myButton       |
        | Select Flex Application     | secondFlexApp  |
        | Flex Element Text Should Be | Hello, Flex!   |
        """
        self.page_should_contain_element(locator)
        # It seems that Selenium timeout is used regardless what's given here
        self._selenium.do_command("waitForFlexReady", [locator, self._timeout])
        self._flex_app = locator

    def wait_for_flex_element(self, locator, timeout=None):
        """Waits until an element is found by `locator` or `timeout` expires.

        See `introduction` for more information about locating Flex elements
        and timeouts.
        """
        error = "Element '%s' did not appear in %%(timeout)s" % locator
        self._wait_until(lambda: self._flex_element_exists(locator), error, timeout)

    def _flex_element_exists(self, locator):
        try:
            self._flex_command('flexAssertDisplayObject', locator)
        except NoFlexApplicationSelected:
            raise
        except Exception:
            return False
        else:
            return True

    def flex_element_should_exist(self, locator):
        """Verifies that an element can be found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexAssertDisplayObject', locator)

    def flex_element_should_not_exist(self, locator):
        """Verifies that an element is not found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        try:
            self.flex_element_should_exist(locator)
        except Exception:
            pass
        else:
            raise AssertionError("Element '%s' exists" % locator)

    def click_flex_element(self, locator):
        """Clicks an element found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexClick', locator)

    def double_click_flex_element(self, locator):
        """Double clicks an element found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexDoubleClick', locator)

    def flex_element_text_should_be(self, locator, expected):
        """Verifies that an element found by `locator` has text `expected`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command_with_retry('flexAssertText', locator,
                                      'validator='+expected)

    def flex_element_property_should_be(self, locator, property, expected):
        """Verifies than an element found by `locator` has correct property.

        `property` is the name of the property and `expected` is the expected
        value.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command_with_retry('flexAssertProperty', locator,
                                      'validator=%s|%s' % (property, expected))

    def input_text_into_flex_element(self, locator, text):
        """Inputs `text` into an element found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexType', locator, 'text='+text)

    def select_from_flex_element(self, locator, value):
        """Selects `value` from an element found by `locator`.

        `locator` is used for finding the correct Flex element as explained
        in `introduction`.

        `value` specifies the value to select. By default the value is selected
        by `label` attribute (i.e. visible text). Other supported value
        locators are `index`, `text`, `data` and `value`. To use them, you need
        to prefix the value with the locator type like `index=1`.

        Examples:
        | Select From Flex Element | Text          | # Select by visible text |
        | Select From Flex Element | index=1       | # Select by index |
        | Select From Flex Element | data=someData | # Select by associated data |

        *NOTE:* This keyword only generates `mx.events.ListEvent.CHANGE` event.
        Event handlers associated with open or close events are thus not executed.
        """
        self._flex_command('flexSelect', locator,
                           self._flex_locator(value, self._flex_select_locators))

    def _flex_command_with_retry(self, command, locator, opts, timeout=1.0):
        """Retry running `_flex_command` if it fails until `timeout`.

        Retrying is needed because Flex Pilot's asserts sometime fail when done
        immediately after updating components, most often after flexSelect.
        This seems to be the cleanest workaround.
        """
        maxtime = time.time() + timeout
        while True:
            try:
                self._flex_command(command, locator, opts)
            except Exception:
                if time.time() > maxtime:
                    raise
                self._debug("Command '%s' failed. Retrying in 0.1s." % command)
                time.sleep(0.1)
            else:
                break

    def _flex_command(self, command, locator, option=None):
        if not self._flex_app:
            raise NoFlexApplicationSelected
        opts = self._get_options(locator, option)
        self._debug("Executing command '%s' for application '%s' with options '%s'"
                    % (command, self._flex_app, opts))
        self._selenium.do_command(command, [self._flex_app, opts])

    def _get_options(self, locator, option):
        # TODO: Cleanup
        loctype, locval = self._flex_locator(locator).split('=', 1)
        if option:
            opttype, optvalue = option.split('=', 1)
            for spec_char, escape in [('&', '&amp;'), ("'", '&apos;'), ('"', '&quot;'),
                                      ('<', '&lt;'), ('>', '&gt;')]:
                optvalue = optvalue.replace(spec_char, escape)
            return "{'%s': '%s', '%s': '%s'}" % (loctype, locval, opttype, optvalue)
        return "{'%s': '%s'}" % (loctype, locval)

    def _flex_locator(self, locator, prefixes=_flex_element_locators):
        locator = locator.strip()
        for prefix in prefixes:
            if locator.startswith(prefix):
                return locator
        return prefixes[0] + locator
