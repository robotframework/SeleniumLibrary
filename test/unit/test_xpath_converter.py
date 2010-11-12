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

import unittest

from robot.utils.asserts import assert_equals, assert_raises_with_msg
from SeleniumLibrary.xpath import LocatorParser


LINK_XPATH = 'xpath=//a[@id="%s" or @name="%s" or @href="%s" or ' \
             'normalize-space(descendant-or-self::text())="%s" or ' \
             '@href="http://fake.url/%s"]'


class _FakeLibrary:
    get_location = lambda self: 'http://fake.url/'


class TestXpathForLocator(unittest.TestCase):

    def setUp(self):
        self._parser = LocatorParser(_FakeLibrary())

    def test_escaping_quote(self):
        for inp in ['"', '    ""     ', 'my link with " quote']:
            esc = inp.replace('"', '&quot;')
            assert_equals(self._parser.locator_for(inp, 'a'),
                          LINK_XPATH % (esc, esc, esc, esc, esc))

    def test_escaping_less_than(self):
        for inp in ["<", " < <    <", "my link with < less than"]:
            esc = inp.replace("<", '&lt;')
            assert_equals(self._parser.locator_for(inp, 'a'),
                          LINK_XPATH % (esc, esc, esc, esc, esc))

    def test_add_locator_prefix(self):
        self._parser.add_strategy('jquery')
        locator = 'jquery=div.#my_select'
        assert_equals(self._parser.locator_for(locator, 'select'), locator)


if __name__ == '__main__':
    unittest.main()
