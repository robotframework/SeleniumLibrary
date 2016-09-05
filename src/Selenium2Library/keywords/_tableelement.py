import os
import sys
from Selenium2Library.locators import TableElementFinder
from keywordgroup import KeywordGroup

class _TableElementKeywords(KeywordGroup):

    def __init__(self):
        self._table_element_finder = TableElementFinder()

    # Public

    def get_table_rows(self, table_locator, loglevel='INFO'):
        """Return the rows of the table.
        
        Header and footer rows are included in the count.
        """
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            return len(rows)
        self.log_source(loglevel)
        raise AssertionError("Table %s could not be found." % table_locator)

    def get_table_cols_at_row(self, table_locator, row, loglevel='INFO'):
        """Return the columns of the table in one row.
            
        Row number start from 1. It will count the columns at one row, 
        the argument 'row' is the row number which you should give it.
        """
        row = int(row)
        row_index = row - 1
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            if row_index < len(rows):
                columns = rows[row_index].find_elements_by_tag_name('th')
                columns.extend(rows[row_index].find_elements_by_tag_name('td'))
                return len(columns)
        raise AssertionError("Table %s in row #%s could not be found." % (table_locator, str(row)))

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
        if row > 0: row_index = row - 1
        column = int(column)
        column_index = column
        if column > 0: column_index = column - 1
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
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

        See `Page Should Contain` for explanation about `loglevel` argument.
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
        element = self._table_element_finder.find_by_col(self._current_browser(), table_locator, col, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))

    """Added By Adam Wu (XPath Version)""
    def get_index_in_table_column(self, table_locator, col, content, loglevel='INFO'):
        ""get content's index in a specific column contains `content`.

        Row and column number start from 1. Header and footer rows are
        included in the count. This means that also cell content from
        header or footer rows can be obtained with this keyword. To
        understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about `loglevel` argument.
        ""
        col = int(col)
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            row_index = 0
            for row in rows:
                row_index=row_index+1
                col_elements = row.find_elements_by_tag_name('th')
                col_elements.extend(row.find_elements_by_tag_name('td'))
                current_col = 0
                for element in col_elements:
                    current_col = current_col + 1                
                    element_text = element.text
                    if element_text and current_col==col and content in element_text:
                        return row_index
        self.log_source(loglevel)
        raise AssertionError("%s could not be found in col #%s of table %s."
            % (content, str(col), table_locator))
    """

    """Added By Adam Wu CSS Version"""
    def get_index_in_table_column(self, table_locator, col, expected, loglevel='INFO'):
        """get content's index in a specific column contains `content`.

        Row and column number start from 1. Header and footer rows are
        included in the count. However, the header and footer content
        will not be matched against 'expected'.

        See `Page Should Contain Element` for explanation about `loglevel` argument.
        """
        has_head=0
        element = self._table_element_finder.find_by_header(self._current_browser(), table_locator, None)
        if element is not None:
            has_head = 1
        index = self._table_element_finder.find_in_col(self._current_browser(), table_locator, col, expected)
        if index <= 0:
            self.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))
        return index+has_head
        
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
        element = self._table_element_finder.find_by_row(self._current_browser(), table_locator, row, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected))

    """Added By Adam Wu"""
    def get_index_in_table_row(self, table_locator, row, expected, loglevel='INFO'):
        """Get content's index in a specific table row contains `content`.

        Row and column number start from 1. Header and footer rows are
        included in the count. This means that also cell content from
        header or footer rows can be obtained with this keyword. To
        understand how tables are identified, please take a look at
        the `introduction`.

        See `Page Should Contain Element` for explanation about `loglevel` argument.
        """
        row = int(row)
        row_index = row - 1
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath("./thead/tr")
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tbody/tr"))
            if row_index >= len(rows): rows.extend(table.find_elements_by_xpath("./tfoot/tr"))
            if row_index < len(rows):
                columns = rows[row_index].find_elements_by_tag_name('th')
                columns.extend(rows[row_index].find_elements_by_tag_name('td'))
                column_index = 0
                for element in columns:
                    column_index = column_index + 1
                    element_text = element.text
                    if element_text and expected in element_text:
                        return column_index
        self.log_source(loglevel)
        raise AssertionError("%s could not be found in row #%s of table %s."
            % (expected, str(row), table_locator))
        
        
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
