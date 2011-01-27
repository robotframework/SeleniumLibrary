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


class Table(RunOnFailure):

    def table_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that `expected` can be found somewhere in the table.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        msg = "Table identified by '%s' should have contained text '%s'." \
                % (table_locator, expected)
        locator = TableLocator(table_locator).content(expected)
        self._page_should_contain_element(locator, 'element', msg, loglevel)

    def table_header_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table header, i.e. any <th>...</th> element, contains `expected`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        msg = ("Header in table identified by '%s' should have contained "
               "text '%s'." % (table_locator, expected))
        locator = TableLocator(table_locator).header(expected)
        self._page_should_contain_element(locator, 'element', msg, loglevel)

    def table_footer_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table footer contains `expected`.

        With table footer can be described as any <td>-element that is
        child of a <tfoot>-element.  To understand how tables are
        identified, please take a look at the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        message = ("Footer in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected))
        locator = TableLocator(table_locator).footer(expected)
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_row_should_contain(self, table_locator, row, expected, loglevel='INFO'):
        """Verifies that a specific table row contains `expected`.

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
        message = ("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected))
        locator = TableLocator(table_locator).row(row, expected)
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def table_column_should_contain(self, table_locator, col, expected, loglevel='INFO'):
        """Verifies that a specific column contains `expected`.

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
        message = ("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))
        locators = TableLocator(table_locator).col(col, expected)
        try:
            self._page_should_contain_element(locators[0], 'element', message,
                                              loglevel)
        except AssertionError:
            if not len(locators) > 1:
                raise
            self._page_should_contain_element(locators[1], 'element', message,
                                              loglevel)

    def get_table_cell(self, table_locator, row, column):
        """Returns the content from a table cell.

        Row and Column number start from 1. Header and footer rows are
        included in the count. This means that also cell content from
        header or footer rows can be obtained with this keyword. To
        understand how tables are identified, please take a look at
        the `introduction`.
        """
        locator = "%s.%d.%d" % (TableLocator(table_locator).locator,
                                int(row)-1, int(column)-1)
        self._debug('Using locator: %s' % locator)
        return self._selenium.get_table(locator)

    def table_cell_should_contain(self, table_locator, row, column, expected):
        """Verifies that a certain cell in a table contains `expected`.

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
                   % (table_locator, row, column, expected))
        try:
            content = self.get_table_cell(table_locator, row, column)
        except Exception, err:
            self._info(self._get_error_message(err))
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if expected not in content:
            raise AssertionError(message)


class TableLocator(object):
    _css_selectors = dict(
        content = ':contains("%s")',
        header  = ' th:contains("%s")',
        footer  = ' tfoot td:contains("%s")',
        row     = ' tr:nth-child(%s):contains("%s")',
        col     = [' tr td:nth-child(%s):contains("%s")',
                   ' tr th:nth-child(%s):contains("%s")']
    )
    _xpath_selectors = dict(
        content = '//*[descendant-or-self::text()="%s"]',
        header  = '//th[descendant-or-self::text()="%s"]',
        footer  = '//tfoot//td[descendant-or-self::text()="%s"]',
        row     = '//tr[%s]//*[descendant-or-self::text()="%s"]',
        col     = ['//tr//*[self::td or self::th][%s][descendant-or-self::text()="%s"]']
    )

    def __init__(self, locator):
        self.locator = self._tablelocator(locator)
        if self.locator.startswith('xpath='):
            self._selectors = self._xpath_selectors
        else:
            self._selectors = self._css_selectors

    def _tablelocator(self, locator):
        if locator.startswith('xpath=') or locator.startswith('css='):
            return locator
        return 'css=table#%s' % locator

    def __getattr__(self, name):
        if name not in self._selectors:
            raise AttributeError(name)
        selector = self._selectors[name]
        if isinstance(selector, list):
            return lambda *args: [self.locator + s % args for s in selector]
        return lambda *args: self.locator + selector % args
