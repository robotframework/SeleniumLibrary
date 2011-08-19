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


class Mouse(RunOnFailure):
    """Conditions keywords for simulating mouse events."""

    def mouse_over(self, locator):
        """Simulates hovering mouse over the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Over on element '%s'" % locator)
        self._selenium.mouse_over(locator);

    def mouse_out(self, locator):
        """Simulates moving mouse away from the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Out on element '%s'" % locator)
        self._selenium.mouse_out(locator)

    def mouse_down(self, locator):
        """Simulates pressing the left mouse button on the element specified by `locator`.

        The element is pressed without releasing the mouse button.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        See also the more specific keywords `Mouse Down On Image` and
        `Mouse Down On Link`.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Down on element '%s'" % locator)
        self._selenium.mouse_down(locator)

    def mouse_up(self, locator):
        """Simulates releasing the left mouse button on the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Simulating Mouse Up on element '%s'" % locator)
        self._selenium.mouse_up(locator)

    def mouse_down_on_image(self, locator):
        """Simulates a mouse down event on an image.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._selenium.mouse_down(self._parse_locator(locator, 'image'))

    def mouse_down_on_link(self, locator):
        """Simulates a mouse down event on a link.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._selenium.mouse_down(self._parse_locator(locator, 'link'))
