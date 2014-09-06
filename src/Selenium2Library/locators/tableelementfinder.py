from selenium.common.exceptions import NoSuchElementException
from Selenium2Library import utils
from elementfinder import ElementFinder

class TableElementFinder(object):

    def __init__(self, element_finder=None):
        if not element_finder:
            element_finder = ElementFinder()
        self._element_finder = element_finder

        self._locator_suffixes = {
            ('css', 'default'): [''],
            ('css', 'content'): [''],
            ('css', 'header'): [' th'],
            ('css', 'footer'): [' tfoot td'],
            ('css', 'row'): [' tr:nth-child(%s)'],
            ('css', 'last-row'): [' tr:nth-last-child(%s)'],
            ('css', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],
            ('css', 'last-col'): [' tr td:nth-last-child(%s)', ' tr th:nth-last-child(%s)'],

            ('jquery', 'default'): [''],
            ('jquery', 'content'): [''],
            ('jquery', 'header'): [' th'],
            ('jquery', 'footer'): [' tfoot td'],
            ('jquery', 'row'): [' tr:nth-child(%s)'],
            ('jquery', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],

            ('sizzle', 'default'): [''],
            ('sizzle', 'content'): [''],
            ('sizzle', 'header'): [' th'],
            ('sizzle', 'footer'): [' tfoot td'],
            ('sizzle', 'row'): [' tr:nth-child(%s)'],
            ('sizzle', 'col'): [' tr td:nth-child(%s)', ' tr th:nth-child(%s)'],

            ('xpath', 'default'): [''],
            ('xpath', 'content'): ['//*'],
            ('xpath', 'header'): ['//th'],
            ('xpath', 'footer'): ['//tfoot//td'],
            ('xpath', 'row'): ['//tr[%s]//*'],
            ('xpath', 'last-row'): [' //tbody/tr[position()=last()-(%s-1)]'],
            ('xpath', 'col'): ['//tr//*[self::td or self::th][%s]'],
            ('xpath', 'last-col'): [' //tbody/tr/td[position()=last()-(%s-1)]', ' //tbody/tr/td[position()=last()-(%s-1)]']
        };

    def find(self, browser, table_locator):
        locators = self._parse_table_locator(table_locator, 'default')
        return self._search_in_locators(browser, locators, None)

    def find_by_content(self, browser, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'content')
        return self._search_in_locators(browser, locators, content)

    def find_by_header(self, browser, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'header')
        return self._search_in_locators(browser, locators, content)

    def find_by_footer(self, browser, table_locator, content):
        locators = self._parse_table_locator(table_locator, 'footer')
        return self._search_in_locators(browser, locators, content)

    def find_by_row(self, browser, table_locator, row, content):
        location_method = "row"
        row = str(row)
        if row[0] == "-":
            row = row[1:]
            location_method = "last-row"
        locators = self._parse_table_locator(table_locator, location_method)
        locators = [locator % str(row) for locator in locators]
        return self._search_in_locators(browser, locators, content)

    def find_by_col(self, browser, table_locator, col, content):
        location_method = "col"
        col = str(col)
        if col[0] == "-":
            col = col[1:]
            location_method = "last-col"
        locators = self._parse_table_locator(table_locator, location_method)
        locators = [locator % str(col) for locator in locators]
        return self._search_in_locators(browser, locators, content)

    def _parse_table_locator(self, table_locator, location_method):
        if table_locator.startswith('xpath='):
            table_locator_type = 'xpath'
        elif table_locator.startswith('jquery=') or table_locator.startswith('sizzle='):
            table_locator_type = 'sizzle'
        else:
            if not table_locator.startswith('css='):
                table_locator = "css=table#%s" % table_locator
            table_locator_type = 'css'

        locator_suffixes = self._locator_suffixes[(table_locator_type, location_method)]

        return map(
            lambda locator_suffix: table_locator + locator_suffix,
            locator_suffixes)

    def _search_in_locators(self, browser, locators, content):
        for locator in locators:
            elements = self._element_finder.find(browser, locator)
            for element in elements:
                if content is None: return element
                element_text = element.text
                if element_text and content in element_text:
                    return element
        return None
