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
from typing import Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.base import LibraryComponent, keyword


class TableElementKeywords(LibraryComponent):
    @keyword
    def get_table_cell(
        self,
        locator: Union[WebElement, str],
        row: int,
        column: int,
        loglevel: str = "TRACE",
    ) -> str:
        """Returns contents of a table cell.

        The table is located using the ``locator`` argument and its cell
        found using ``row`` and ``column``. See the `Locating elements`
        section for details about the locator syntax.

        Both row and column indexes start from 1, and header and footer
        rows are included in the count. It is possible to refer to rows
        and columns from the end by using negative indexes so that -1
        is the last row/column, -2 is the second last, and so on.

        All ``<th>`` and ``<td>`` elements anywhere in the table are
        considered to be cells.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.
        """
        if row == 0 or column == 0:
            raise ValueError(
                "Both row and column must be non-zero, "
                f"got row {row} and column {column}."
            )
        try:
            cell = self._get_cell(locator, row, column)
        except AssertionError:
            self.log_source(loglevel)
            raise
        return cell.text

    def _get_cell(self, locator, row, column):
        rows = self._get_rows(locator, row)
        if len(rows) < abs(row):
            raise AssertionError(
                f"Table '{locator}' should have had at least {abs(row)} "
                f"rows but had only {len(rows)}."
            )
        index = row - 1 if row > 0 else row
        cells = rows[index].find_elements(By.XPATH, "./th|./td")
        if len(cells) < abs(column):
            raise AssertionError(
                f"Table '{locator}' row {row} should have had at "
                f"least {abs(column)} columns but had only {len(cells)}."
            )
        index = column - 1 if column > 0 else column
        return cells[index]

    def _get_rows(self, locator, count):
        # Get rows in same order as browsers render them.
        table = self.find_element(locator, tag="table")
        rows = table.find_elements(By.XPATH, "./thead/tr")
        if count < 0 or len(rows) < count:
            rows.extend(table.find_elements(By.XPATH, "./tbody/tr"))
        if count < 0 or len(rows) < count:
            rows.extend(table.find_elements(By.XPATH, "./tfoot/tr"))
        return rows

    @keyword
    def table_cell_should_contain(
        self,
        locator: Union[WebElement, str],
        row: int,
        column: int,
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies table cell contains text ``expected``.

        See `Get Table Cell` that this keyword uses internally for
        an explanation about accepted arguments.
        """
        content = self.get_table_cell(locator, row, column, loglevel)
        if expected not in content:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' cell on row {row} and column {column} "
                f"should have contained text '{expected}' but it had '{content}'."
            )
        self.info(f"Table cell contains '{content}'.")

    @keyword
    def table_column_should_contain(
        self,
        locator: Union[WebElement, str],
        column: int,
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies table column contains text ``expected``.

        The table is located using the ``locator`` argument and its column
        found using ``column``. See the `Locating elements` section for
        details about the locator syntax.

        Column indexes start from 1. It is possible to refer to columns
        from the end by using negative indexes so that -1 is the last column,
        -2 is the second last, and so on.

        If a table contains cells that span multiple columns, those merged
        cells count as a single column.

        See `Page Should Contain Element` for an explanation about the
        ``loglevel`` argument.
        """
        element = self._find_by_column(locator, column, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' column {column} did not contain text '{expected}'."
            )

    @keyword
    def table_footer_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies table footer contains text ``expected``.

        Any ``<td>`` element inside ``<tfoot>`` element is considered to
        be part of the footer.

        The table is located using the ``locator`` argument. See the
        `Locating elements` section for details about the locator syntax.

        See `Page Should Contain Element` for an explanation about the
        ``loglevel`` argument.
        """
        element = self._find_by_footer(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' footer did not contain text '{expected}'."
            )

    @keyword
    def table_header_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies table header contains text ``expected``.

        Any ``<th>`` element anywhere in the table is considered to be
        part of the header.

        The table is located using the ``locator`` argument. See the
        `Locating elements` section for details about the locator syntax.

        See `Page Should Contain Element` for an explanation about the
        ``loglevel`` argument.
        """
        element = self._find_by_header(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' header did not contain text '{expected}'."
            )

    @keyword
    def table_row_should_contain(
        self,
        locator: Union[WebElement, str],
        row: int,
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies that table row contains text ``expected``.

        The table is located using the ``locator`` argument and its column
        found using ``column``. See the `Locating elements` section for
        details about the locator syntax.

        Row indexes start from 1. It is possible to refer to rows
        from the end by using negative indexes so that -1 is the last row,
        -2 is the second last, and so on.

        If a table contains cells that span multiple rows, a match
        only occurs for the uppermost row of those merged cells.

        See `Page Should Contain Element` for an explanation about the
        ``loglevel`` argument.
        """
        element = self._find_by_row(locator, row, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' row {row} did not contain text '{expected}'."
            )

    @keyword
    def table_should_contain(
        self,
        locator: Union[WebElement, str],
        expected: str,
        loglevel: str = "TRACE",
    ):
        """Verifies table contains text ``expected``.

        The table is located using the ``locator`` argument. See the
        `Locating elements` section for details about the locator syntax.

        See `Page Should Contain Element` for an explanation about the
        ``loglevel`` argument.
        """
        element = self._find_by_content(locator, expected)
        if element is None:
            self.ctx.log_source(loglevel)
            raise AssertionError(
                f"Table '{locator}' did not contain text '{expected}'."
            )

    def _find_by_content(self, table_locator, content):
        return self._find(table_locator, "xpath:.//*", content)

    def _find_by_header(self, table_locator, content):
        return self._find(table_locator, "xpath:.//th", content)

    def _find_by_footer(self, table_locator, content):
        return self._find(table_locator, "xpath:.//tfoot//td", content)

    def _find_by_row(self, table_locator, row, content):
        position = self._index_to_position(row)
        locator = f"//tr[{position}]"
        return self._find(table_locator, locator, content)

    def _find_by_column(self, table_locator, col, content):
        position = self._index_to_position(col)
        locator = f"//tr//*[self::td or self::th][{position}]"
        return self._find(table_locator, locator, content)

    def _index_to_position(self, index):
        if index == 0:
            raise ValueError("Row and column indexes must be non-zero.")
        if index > 0:
            return str(index)
        if index == -1:
            return "position()=last()"
        return f"position()=last()-{abs(index) - 1}"

    def _find(self, table_locator, locator, content):
        table = self.find_element(table_locator)
        elements = self.find_elements(locator, parent=table)
        for element in elements:
            if content is None:
                return element
            if element.text and content in element.text:
                return element
        return None
