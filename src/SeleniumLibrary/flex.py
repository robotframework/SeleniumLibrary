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

from runonfailure import RunOnFailure


class NoFlexApplicationSelected(Exception):
    pass


class Flex(RunOnFailure):

    def select_flex_application(self, locator, alias=None):
        """Select flex application to work with.

        All further Flex-keywords will operate on the selected application.

        `locator` is the value `id` or `name` attribute of the movie in HTML.

        Return index if this application that can be used with `Switch Flex
        Application`
        """
        self.page_should_contain_element(locator)
        # It seems that selenium timeout is used instead of given timeout.
        self._selenium.do_command("waitForFlexReady", [locator, 'timeout'])
        return self._flex_apps.register(locator, alias)

    def wait_for_flex_element(self, locator, timeout=None):
        error = "Element '%s' did not appear in %%(timeout)s" % locator
        self._wait_for_flex_element(self._flex_locator(locator),
                                    timeout, error)

    def _wait_for_flex_element(self, locator, timeout, error):
        self._wait_until(lambda: self._element_exists(locator),
                         error, timeout)

    def _element_exists(self, locator):
        try:
            self._do_flex_command('flexAssertDisplayObject', locator)
        except NoFlexApplicationSelected:
            raise
        except Exception:
            return False
        else:
            return True

    def switch_flex_application(self, index_or_alias):
        """Switches between active flex applications  using index or alias.

        `index_or_alias` is got from `Select Flex Application` and alias can
        be given to it.
        """
        self._flex_apps.switch(index_or_alias)

    def flex_element_should_exist(self, locator):
        """Verifies that Flex component can be found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexAssertDisplayObject', locator)

    def flex_element_should_not_exist(self, locator):
        """Verifies that Flex component cannot be found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        try:
            self.flex_element_should_exist(locator)
        except Exception:
            pass
        else:
            raise AssertionError("Element '%s' exists" % locator)

    def click_flex_element(self, locator):
        """Click the Flex element found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexClick', locator)

    def flex_element_text_should_be(self, locator, expected):
        """Verifies the value of the text field found by `locator` is `expected`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexAssertText', locator, 'validator='+expected)

    def flex_element_property_should_be(self, locator, name, expected):
        """Verifies property value of an element found by `locator`.

        `name` is the name of the property and `expected` is the expected
        value.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexAssertProperty', locator,
                           'validator=%s|%s' % (name, expected))

    def input_text_into_flex_element(self, locator, text):
        """Input `value` in the text field found by `locator`.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexType', locator, 'text='+text)

    def select_from_flex_element(self, locator, value):
        """Select `value` from Flex element found by `locator`.

        `value` may be either an index, visible text, or associated data of
        the item to be selected.

        Examples:
        | Select From Flex Element | Text | # Select by visible text |
        | Select From Flex Element | index=1 | # Select by index |
        | Select From Flex Element | data=someData | # Select by associated data |

        *NOTE* This keyword generates mx.events.ListEvent.CHANGE event, which
        means that event handlers associated with opening or closing a drop down
        menu will not be executed.

        See `introduction` about rules for locating Flex elements.
        """
        self._flex_command('flexSelect', locator, self._choice_locator(value))

    def _choice_locator(self, locator):
        for prefix in ['index=', 'label=', 'text=', 'data=', 'value=']:
            if locator.startswith(prefix):
                return locator
        return 'label='+locator

    def _flex_command(self, command, locator, option=None):
        locator = self._flex_locator(locator)
        self._verify_flex_element_exists(locator)
        self._do_flex_command(command, locator, option)

    def _flex_locator(self, locator):
        locator = locator.strip()
        # prefixes gotten from org/flex_pilot/FPLocator.as
        for prefix in ['id=', 'automationName=', 'name=', 'chain=', 'label=',
                       'htmlText=']:
            if locator.startswith(prefix):
                return locator
        return 'id=%s' % locator

    def _verify_flex_element_exists(self, locator):
        if not self._flex_apps.current:
            raise NoFlexApplicationSelected
        error = "Element '%s' does not exist" % locator
        self._wait_for_flex_element(locator, '0.5s', error)

    def _do_flex_command(self, command, *options):
        app = self._flex_apps.current
        opts = ', '.join([o for o in options if o is not None])
        self._debug("Executing command '%s' for application '%s' with options '%s'"
                    % (command, app, opts))
        self._selenium.do_command(command, [app, opts])
