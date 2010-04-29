#  Copyright 2008-2009 Nokia Siemens Networks Oyj
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

    def table_should_contain(self, table_locator, expected_content):
        """doc.
        """
        locator = "css=table#%s:contains(\"%s\")" % (table_locator, expected_content)
        message = "ERROR: Table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)
        return

    def table_header_should_contain(self, table_locator, expected_content):
        """doc.
        """
        locator = "css=table#%s th:contains(\"%s\")" % (table_locator, expected_content)
        message = "ERROR: Header in table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)
        return

    def table_footer_should_contain(self, table_locator, expected_content):
        """doc.
        """
        locator = "css=table#%s tfoot td:contains(\"%s\")" % (table_locator, expected_content)
        message = "ERROR: Footer in table identified by '%s' should have contained text '%s'." % (table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)
        return

    def table_row_should_contain(self, table_locator, row, expected_content):
        """doc.
        """
        locator = "css=table#%s tr:nth-child(%s):contains(\"%s\")" % (table_locator, row, expected_content)
        message = "ERROR: Row #%s in table identified by '%s' should have contained text '%s'." % (row, table_locator, expected_content)
        self._page_should_contain_element(locator, 'element', message)
        return

    def table_column_should_contain(self, table_locator, row, expected_content):
        """doc.
        """
        locator = "css=table#%s tr td:nth-child(%s):contains(\"%s\")" % (table_locator, row, expected_content)
        message = "ERROR: Column #%s in table identified by '%s' should have contained text '%s'." % (row, table_locator, expected_content)
        try: 
            self._page_should_contain_element(locator, 'element', message)
        except AssertionError, err:
            if 'should have contained text' not in self._get_error_message(err):
                raise
            locator = "css=table#%s tr th:nth-child(%s):contains(\"%s\")" % (table_locator, row, expected_content)
            self._page_should_contain_element(locator, 'element', message)
        return    
    
    def get_table_cell(self, table_name, row, column):
        """doc.
        """
        row=int(row)-1;
        column=int(column)-1;
        return self._selenium.get_table("%s.%d.%d" % (table_name, row, column));
        
    def table_cell_should_contain(self, table_locator, row, column, expected_content):
        message = "ERROR: Cell in table '%s' in row #%s and column #%s should have contained text '%s'." % (table_locator, row, column, expected_content)
        try:
            content = self.get_table_cell(table_locator, row, column);
        except Exception, err:
            self._info(self._get_error_message(err))
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if not expected_content in content:
            self._info("Expected content not found.")
            raise AssertionError(message)