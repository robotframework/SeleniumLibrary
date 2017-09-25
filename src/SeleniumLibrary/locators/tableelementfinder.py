# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from SeleniumLibrary.base import ContextAware


class TableElementFinder(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        self._table_suffixes = {
            'content': ['//*'],
            'header': ['//th'],
            'footer': ['//tfoot//td'],
            'row': ['//tr[%s]//*'],
            'last-row': ['//tbody/tr[position()=last()-(%s-1)]'],
            'col': ['//tr//*[self::td or self::th][%s]'],
            'last-col': ['//tbody/tr/td[position()=last()-(%s-1)]',
                         '//tbody/tr/td[position()=last()-(%s-1)]']
        }

    def find_by_content(self, table_locator, content):
        table_element = self.element_finder.find(table_locator)
        locators = self._table_suffixes['content']
        return self._search_in_locators(table_element, locators, content)

    def find_by_header(self, table_locator, content):
        table_element = self.element_finder.find(table_locator)
        locators = self._table_suffixes['header']
        return self._search_in_locators(table_element, locators, content)

    def find_by_footer(self, table_locator, content):
        table_element = self.element_finder.find(table_locator)
        locators = self._table_suffixes['footer']
        return self._search_in_locators(table_element, locators, content)

    def find_by_row(self, table_locator, row, content):
        location_method = "row"
        row = str(row)
        if row[0] == "-":
            row = row[1:]
            location_method = "last-row"
        table_element = self.element_finder.find(table_locator)
        locators = self._table_suffixes[location_method]
        locators = [locator % str(row) for locator in locators]
        return self._search_in_locators(table_element, locators, content)

    def find_by_col(self, table_locator, col, content):
        location_method = "col"
        col = str(col)
        if col[0] == "-":
            col = col[1:]
            location_method = "last-col"
        table_element = self.element_finder.find(table_locator)
        locators = self._table_suffixes[location_method]
        locators = [locator % str(col) for locator in locators]
        return self._search_in_locators(table_element, locators, content)

    def _search_in_locators(self, table_element, locators, content):
        print 'locators, ', locators
        for locator in locators:
            print 'locator: "{}"'.format(locator)
            elements = self.element_finder.find(locator, first_only=False,
                                                required=False,
                                                parent=table_element)
            for element in elements:
                if content is None:
                    return element
                element_text = element.text
                if element_text and content in element_text:
                    return element
        return None
