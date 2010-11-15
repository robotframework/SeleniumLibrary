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

class Table(object):

    def table_should_contain(self, table_locator, expected_content, loglevel='INFO'):
        """Verifies that the `expected content` can be found somewhere in the table.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        locator = "%s:contains('%s')" % (self._get_table_locator(table_locator),
                                         expected_content)
        message = "Table identified by '%s' should have contained text '%s'." \
            % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_header_should_contain(self, table_locator, expected_content, loglevel='INFO'):
        """Verifies that the table header, i.e. any <th>...</th> element, contains the `expected_content`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        locator = "%s th:contains('%s')" % (self._get_table_locator(table_locator),
                                            expected_content)
        message = ("Header in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected_content))
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_footer_should_contain(self, table_locator, expected_content, loglevel='INFO'):
        """Verifies that the table footer contains the `expected_content`.

        With table footer can be described as any <td>-element that is
        child of a <tfoot>-element.  To understand how tables are
        identified, please take a look at the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        locator = "%s tfoot td:contains('%s')" \
            % (self._get_table_locator(table_locator), expected_content)
        message = ("Footer in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected_content))
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_row_should_contain(self, table_locator, row, expected_content, loglevel='INFO'):
        """Verifies that a specific table row contains the `expected_content`.

        The uppermost row is row number 1. For tables that are
        structured with thead, tbody and tfoot, only the tbody section
        is searched. Please use `Table Header Should Contain` or
        `Table Footer Should Contain` for tests against the header or
        footer content.

        If the table contains cells that span multiple rows, a match
        only occurs for the uppermost row of those merged cells. To
        understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about `loglevel` argument.
        """
        locator = "%s tr:nth-child(%s):contains('%s')" \
            % (self._get_table_locator(table_locator), row, expected_content)
        message = ("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected_content))
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_column_should_contain(self, table_locator, col, expected_content, loglevel='INFO'):
        """Verifies that a specific column contains the `expected_content`.

        The first leftmost column is column number 1. If the table
        contains cells that span multiple columns, those merged cells
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
        locator = "%s tr td:nth-child(%s):contains('%s')" \
            % (self._get_table_locator(table_locator), col, expected_content)
        message = ("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected_content))
        try:
            self._page_should_contain_element(locator, 'element', message,
                                              loglevel)
        except AssertionError:
            locator = "%s tr th:nth-child(%s):contains('%s')" \
                % (self._get_table_locator(table_locator), col, expected_content)
            self._page_should_contain_element(locator, 'element', message,
                                              loglevel)

    def get_table_cell(self, table_locator, row, column):
        """Returns the content from a table cell.

        Row and Column number start from 1. Header and footer rows are
        included in the count. This means that also cell content from
        header or footer rows can be obtained with this keyword. To
        understand how tables are identified, please take a look at
        the `introduction`.
        """
        locator = "%s.%d.%d" % (self._get_table_locator(table_locator),
                                int(row)-1, int(column)-1)
        return self._selenium.get_table(locator)

    def table_cell_should_contain(self, table_locator, row, column, expected_content):
        """Verifies that a certain cell in a table contains the `expected content`.

        Row and Column number start from 1. This keyword passes if the
        specified cell contains the given content. If you want to test
        that the cell content matches exactly, or that it e.g. starts
        with some text, use `Get Table Cell` keyword in combination
        with built-in keywords such as `Should Be Equal` or `Should
        Start With`.

        To understand how tables are identified, please take a look at
        the `introduction`.
        """
        message = ("Cell in table '%s' in row #%s and column #%s "
                   "should have contained text '%s'."
                   % (table_locator, row, column, expected_content))
        try:
            content = self.get_table_cell(table_locator, row, column)
        except Exception, err:
            self._info(self._get_error_message(err))
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if expected_content not in content:
            raise AssertionError(message)

    def _get_table_locator(self, table_locator):
        if table_locator.startswith("css="):
            return table_locator
        else:
            return "css=table#%s" % (table_locator)
