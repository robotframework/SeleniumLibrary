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
        element = self._table_element_finder.find_by_col(self._current_browser(), table_locator, col, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))

    def table_footer_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_footer(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Footer in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected))

    def table_header_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_header(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Header in table identified by '%s' should have contained "
               "text '%s'." % (table_locator, expected))

    def table_row_should_contain(self, table_locator, row, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_row(self._current_browser(), table_locator, row, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected))

    def table_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_content(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Table identified by '%s' should have contained text '%s'." \
                % (table_locator, expected))