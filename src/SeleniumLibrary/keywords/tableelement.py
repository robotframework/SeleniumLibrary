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

from SeleniumLibrary.base import LibraryComponent, keyword


class TableElementKeywords(LibraryComponent):

    @keyword
    def get_table_cell(self, locator, row, column, loglevel='INFO'):
        """Returns the content from a table cell.

        Row and column number start from 1. Header and footer rows are
        included in the count. A negative row or column number can be used
        to get rows counting from the end (end: -1). Cell content from header
        or footer rows can be obtained with this keyword. To understand how
        tables are identified, please take a look at the `introduction`.

        See `Page Should Contain` for explanation about `loglevel` argument.
        """
        row = int(row)
        column = int(column)
        if row == 0 or column == 0:
            raise ValueError('Both row and column must be non-zero, '
                             'got row %d and column %d.' % (row, column))
        try:
            cell = self._get_cell(locator, row, column)
        except AssertionError:
            self.log_source(loglevel)
            raise
        return cell.text

    def _get_cell(self, locator, row, column):
        rows = self._get_rows(locator, row)
        if len(rows) < abs(row):
            raise AssertionError("Table '%s' should have had at least %d "
                                 "rows but had only %d."
                                 % (locator, abs(row), len(rows)))
        index = row - 1 if row > 0 else row
        cells = rows[index].find_elements_by_xpath('./th|./td')
        if len(cells) < abs(column):
            raise AssertionError("Table '%s' row %d should have had at "
                                 "least %d columns but had only %d."
                                 % (locator, row, abs(column), len(cells)))
        index = column - 1 if column > 0 else column
        return cells[index]

    def _get_rows(self, locator, count):
        # Get rows in same order as browsers render them.
        table = self.find_element(locator, tag='table')
        rows = table.find_elements_by_xpath("./thead/tr")
        if count < 0 or len(rows) < count:
            rows.extend(table.find_elements_by_xpath("./tbody/tr"))
        if count < 0 or len(rows) < count:
            rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
        return rows

    @keyword
    def table_cell_should_contain(self, locator, row, column, expected, loglevel='INFO'):
        """Verifies that a certain cell in a table contains `expected`.

        Row and column number start from 1. This keyword passes if the
        specified cell contains the given content. If you want to test
        that the cell content matches exactly, or that it e.g. starts
        with some text, use `Get Table Cell` keyword in combination
        with built-in keywords such as `Should Be Equal` or `Should
        Start With`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain` for explanation about `loglevel` argument.
        """
        content = self.get_table_cell(locator, row, column, loglevel)
        if expected not in content:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' cell on row %s and column %s "
                                 "should have contained text '%s' but it had "
                                 "'%s'."
                                 % (locator, row, column, expected, content))
        self.info("Table cell contains '%s'." % content)

    @keyword
    def table_column_should_contain(self, locator, column, expected, loglevel='INFO'):
        """Verifies that a specific column contains `expected`.

        The first leftmost column is column number 1. A negative column
        number can be used to get column counting from the end of the row (end: -1).
        If the table contains cells that span multiple columns, those merged cells
        count as a single column. For example both tests below work,
        if in one row columns A and B are merged with colspan="2", and
        the logical third column contains "C".

        Example:
        | Table Column Should Contain | tableId | 3 | C |
        | Table Column Should Contain | tableId | 2 | C |

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_column(locator, column, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' column %s did not contain text "
                                 "'%s'." % (locator, column, expected))

    @keyword
    def table_footer_should_contain(self, locator, expected, loglevel='INFO'):
        """Verifies that the table footer contains `expected`.

        With table footer can be described as any <td>-element that is
        child of a <tfoot>-element.  To understand how tables are
        identified, please take a look at the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_footer(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' footer did not contain text "
                                 "'%s'." % (locator, expected))

    @keyword
    def table_header_should_contain(self, locator, expected, loglevel='INFO'):
        """Verifies that the table header, i.e. any <th>...</th> element, contains `expected`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_header(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' header did not contain text "
                                 "'%s'." % (locator, expected))

    @keyword
    def table_row_should_contain(self, locator, row, expected, loglevel='INFO'):
        """Verifies that a specific table row contains `expected`.

        The uppermost row is row number 1. A negative column
        number can be used to get column counting from the end of the row
        (end: -1). For tables that are structured with thead, tbody and tfoot,
        only the tbody section is searched. Please use `Table Header Should Contain`
        or `Table Footer Should Contain` for tests against the header or
        footer content.

        If the table contains cells that span multiple rows, a match
        only occurs for the uppermost row of those merged cells. To
        understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about `loglevel` argument.
        """
        element = self.table_element_finder.find_by_row(locator, row, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' row %s did not contain text "
                                 "'%s'." % (locator, row, expected))

    @keyword
    def table_should_contain(self, locator, expected, loglevel='INFO'):
        """Verifies that `expected` can be found somewhere in the table.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_content(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table '%s' did not contain text '%s'."
                                 % (locator, expected))
