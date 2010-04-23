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

class Element(object):

    def get_element_attribute(self, attribute_locator):
        """Return value of element attribute.

        `attribute_locator` consists of element locator followed by an @ sign
        and attribute name, for example "element_id@class".
        """
        return self._selenium.get_attribute(attribute_locator)

    def get_matching_xpath_count(self, xpath):
        """Returns number of elements matching `xpath`"""
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
        pos = None
        try:
            pos = getter(self._parse_locator(locator))
        except Exception, err:
            if 'not found' not in self._get_error_message(err):
                raise
        if not pos:
            raise AssertionError("Could not determine position for '%s'" % locator)
        return int(pos)

