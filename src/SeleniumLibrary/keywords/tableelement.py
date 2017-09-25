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
    def get_table_cell(self, table_locator, row, column, loglevel='INFO'):
        """Returns the content from a table cell.

        Row and column number start from 1. Header and footer rows are
        included in the count. A negative row or column number can be used
        to get rows counting from the end (end: -1). Cell content from header
        or footer rows can be obtained with this keyword. To understand how
        tables are identified, please take a look at the `introduction`.

        See `Page Should Contain` for explanation about `loglevel` argument.
        """
        row = int(row)
        row_index = row
        if row > 0:
            row_index = row - 1
        column = int(column)
        column_index = column
        if column > 0:
            column_index = column - 1
        table = self.element_finder.find(table_locator)
        if table:
            rows = table.find_elements_by_xpath("./thead/tr")
            if row_index >= len(rows) or row_index < 0:
                rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            if row_index >= len(rows) or row_index < 0:
                rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            if row_index < len(rows):
                columns = rows[row_index].find_elements_by_tag_name('th')
                if column_index >= len(columns) or column_index < 0:
                    columns.extend(rows[row_index].find_elements_by_tag_name('td'))
                if column_index < len(columns):
                    return columns[column_index].text
        self.ctx.log_source(loglevel)
        raise AssertionError("Cell in table %s in row #%s and column #%s "
                             "could not be found."
                             % (table_locator, str(row), str(column)))

    @keyword
    def table_cell_should_contain(self, table_locator, row, column, expected, loglevel='INFO'):
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
        message = ("Cell in table '%s' in row #%s and column #%s "
                   "should have contained text '%s'."
                   % (table_locator, row, column, expected))
        try:
            content = self.get_table_cell(table_locator, row, column, loglevel='NONE')
        except AssertionError as err:
            self.info(err)
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info("Cell contains %s." % (content))
        if expected not in content:
            self.ctx.log_source(loglevel)
            raise AssertionError(message)

    @keyword
    def table_column_should_contain(self, table_locator, col, expected, loglevel='INFO'):
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
        element = self.table_element_finder.find_by_col(table_locator, col,
                                                        expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                                 "should have contained text '%s'."
                                 % (col, table_locator, expected))

    @keyword
    def table_footer_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table footer contains `expected`.

        With table footer can be described as any <td>-element that is
        child of a <tfoot>-element.  To understand how tables are
        identified, please take a look at the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_footer(table_locator,
                                                           expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Footer in table identified by '%s' "
                                 "should have contained "
                                 "text '%s'." % (table_locator, expected))

    @keyword
    def table_header_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table header, i.e. any <th>...</th> element, contains `expected`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_header(table_locator,
                                                           expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Header in table identified by '%s' should "
                                 "have contained "
                                 "text '%s'." % (table_locator, expected))

    @keyword
    def table_row_should_contain(self, table_locator, row, expected, loglevel='INFO'):
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
        element = self.table_element_finder.find_by_row(table_locator,
                                                        row, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Row #%s in table identified by '%s' "
                                 "should have contained "
                                 "text '%s'." % (row, table_locator, expected))

    @keyword
    def table_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that `expected` can be found somewhere in the table.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self.table_element_finder.find_by_content(table_locator,
                                                            expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError("Table identified by '%s' should have "
                                 "contained text '%s'."
                                 % (table_locator, expected))
