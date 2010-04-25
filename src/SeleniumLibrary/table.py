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
        locator = "css=table[id=\"%s\"]:contains(\"%s\")" % (table_locator, expected_content)
        message = "ERROR: Table identified by '%s' should have contained text '%s'." % (table_locator, "XXX")
        self._page_should_contain_element(locator, 'element', message)
        return
