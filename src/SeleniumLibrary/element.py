#  Copyright 2008-2010 Nokia Siemens Networks Oyj
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


class Element(RunOnFailure):

    def get_element_attribute(self, attribute_locator):
        """Return value of element attribute.

        `attribute_locator` consists of element locator followed by an @ sign
        and attribute name, for example "element_id@class".
        """
        return self._selenium.get_attribute(attribute_locator)

    def get_matching_xpath_count(self, xpath):
        """Returns number of elements matching `xpath`
        
        If you wish to assert that the number of matching elements
        has a certain value, use `Xpath Should Match X Times`.
        """
        return self._selenium.get_xpath_count(xpath)

    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.

        The position is returned in pixels off the left side of the page, 
        as an integer. Fails if a matching element is not found.

        See also `Get Vertical Position`.
        """
        return self._get_position(self._selenium.get_element_position_left,
                                  locator)

    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels off the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Horizontal Position`.
        """
        return self._get_position(self._selenium.get_element_position_top,
                                  locator)

    def _get_position(self, getter, locator):
        not_found = "Could not determine position for '%s'" % locator
        try:
            pos = getter(self._parse_locator(locator))
        except Exception, err:
            if not self._error_contains(err, 'not found'):
                raise
            raise RuntimeError(not_found)
        if not pos:
            raise RuntimeError(not_found)
        return int(pos)

