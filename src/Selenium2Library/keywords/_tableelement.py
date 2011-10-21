import os
import sys
from robot.variables import GLOBAL_VARIABLES
from robot.api import logger
from Selenium2Library.locators import TableElementFinder
from keywordgroup import KeywordGroup

class _TableElementKeywords(KeywordGroup):

    def __init__(self):
        self._table_element_finder = TableElementFinder()

    # Public

    def get_table_cell(self, table_locator, row, column, loglevel='INFO'):
        """Returns the content from a table cell.

        Row and column number start from 1. Header and footer rows are
        included in the count. This means that also cell content from
        header or footer rows can be obtained with this keyword. To
        understand how tables are identified, please take a look at
        the `introduction`.
        """
        row = int(row)
        row_index = row - 1
        column = int(column)
        column_index = column - 1
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            if row_index < len(rows):
                columns = rows[row_index].find_elements_by_tag_name('th')
                if column_index >= len(columns): columns.extend(rows[row_index].find_elements_by_tag_name('td'))
                if column_index < len(columns):
                    return columns[column_index].text
        self.log_source(loglevel)
        raise AssertionError("Cell in table %s in row #%s and column #%s could not be found."
            % (table_locator, str(row), str(column)))

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
        """
        message = ("Cell in table '%s' in row #%s and column #%s "
                   "should have contained text '%s'."
                   % (table_locator, row, column, expected))
        try:
            content = self.get_table_cell(table_locator, row, column, loglevel='NONE')
        except AssertionError, err:
            self._info(err)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if expected not in content:
            self.log_source(loglevel)
            raise AssertionError(message)

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
        element = self._table_element_finder.find_by_col(self._current_browser(), table_locator, col, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))

    def table_footer_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table footer contains `expected`.

        With table footer can be described as any <td>-element that is
        child of a <tfoot>-element.  To understand how tables are
        identified, please take a look at the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self._table_element_finder.find_by_footer(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Footer in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected))

    def table_header_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that the table header, i.e. any <th>...</th> element, contains `expected`.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self._table_element_finder.find_by_header(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Header in table identified by '%s' should have contained "
               "text '%s'." % (table_locator, expected))

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
        element = self._table_element_finder.find_by_row(self._current_browser(), table_locator, row, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected))

    def table_should_contain(self, table_locator, expected, loglevel='INFO'):
        """Verifies that `expected` can be found somewhere in the table.

        To understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about
        `loglevel` argument.
        """
        element = self._table_element_finder.find_by_content(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Table identified by '%s' should have contained text '%s'." \
                % (table_locator, expected))