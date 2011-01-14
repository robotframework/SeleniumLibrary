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


class Flex(RunOnFailure):

    def select_flex_application(self, locator, alias=None):
        """Select flex application to work with.

        All further Flex-keywords will operate on the selected application.

        `locator` is the value `id` or `name` attribute of the movie in HTML.

        Return index if this application that can be used with `Switch Flex
        Application`
        """
        self.page_should_contain_element(locator)
        self._wait_for_flex_ready(locator)
        return self._flex_apps.register(locator, alias)

    def _wait_for_flex_ready(self, locator, timeout=5000):
        # It seems that selenium timeout is always used so this timeout has
        # no effect, event though it's mandatory. Go figure.
        self._selenium.do_command("waitForFlexReady", [locator, timeout])

    def unselect_flex_applications(self):
        """Unselects current Flex application and empties the register.

        After this keyword, Flex application indices returned by `Select
        Flex Application start at 1.
        """
        self._flex_apps.empty_cache()

    def flex_element_should_exist(self, locator):
        """Verifies that Flex component identified by `locator` exists.

        `locator` if interpreted with following rules:
          * `someIdentifier` => matched against `id` attribute of the Flex
             component
          * `name='somename` => `somename` is matched against name attribute
            of the Flex component
          * `id:someId/name:someName`  => searches for component with name
            `someName` which must be a child of component with id `someId`
        """
        self._flex_command('flexAssertDisplayObject',
                           self._flex_locator(locator))

    def click_flex_element(self, locator):
        """Clicks Flex element identified by `locator`.

        TODO: backlink
        """
        self._flex_command('flexClick', self._flex_locator(locator))

    def input_into_flex_textfield(self, locator, value):
        """Input `value` in text field identified by `locator`.

        TODO: backlink
        """
        locator = self._flex_locator(locator)
        self._flex_command('flexType', '%s, text=%s' % (locator, value))

    def flex_textfield_value_should_be(self, locator, expected):
        """Verifies that value of text field identified by `locator` is `expected` .
        """
        locator = self._flex_locator(locator)
        self._flex_command('flexAssertText',
                           '%s,validator=%s' % (locator, expected))

    def _flex_locator(self, locator):
        locator = locator.strip()
        if '=' in locator:
          return locator
        if '/' in locator:
          return 'chain=%s' % locator
        return 'id=%s' % locator

    def _flex_command(self, command, options):
        # TODO: Howto handle commas in option values??
        app = self._flex_apps.current
        if not app:
            raise RuntimeError('No Flex application selected.')
        self._selenium.do_command(command, [app, options])

