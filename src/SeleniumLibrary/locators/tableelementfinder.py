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

    def find_by_content(self, table_locator, content):
        return self._find(table_locator, '//*', content)

    def find_by_header(self, table_locator, content):
        return self._find(table_locator, '//th', content)

    def find_by_footer(self, table_locator, content):
        return self._find(table_locator, '//tfoot//td', content)

    def find_by_row(self, table_locator, row, content):
        position = self._index_to_position(row)
        locator = '//tr[{}]'.format(position)
        return self._find(table_locator, locator, content)

    def find_by_column(self, table_locator, col, content):
        position = self._index_to_position(col)
        locator = '//tr//*[self::td or self::th][{}]'.format(position)
        return self._find(table_locator, locator, content)

    def _index_to_position(self, index):
        index = int(index)
        if index == 0:
            raise ValueError('Row and column indexes must be non-zero.')
        if index > 0:
            return str(index)
        if index == -1:
            return 'position()=last()'
        return 'position()=last()-{}'.format(abs(index) - 1)

    def _find(self, table_locator, locator, content):
        table = self.find_element(table_locator)
        elements = self.find_elements(locator, parent=table)
        for element in elements:
            if content is None:
                return element
            if element.text and content in element.text:
                return element
        return None
