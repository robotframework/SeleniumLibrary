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

from robot import utils


class LocatorParser:
    _strategies = ['dom=', 'xpath=' , 'css=']
    _tag_attributes = {
        'a':       ['@id', '@name', '@href',
                    'normalize-space(descendant-or-self::text())'],
        'img':     ['@id', '@src', '@alt'],
        'input':   ['@id', '@name', '@value', '@src'],
        'button':  ['@id', '@name', '@value',
                    'normalize-space(descendant-or-self::text())'],
    }
    _synonyms = {'link': 'a',
                 'image': 'img',
                 'radio button': 'input'}

    def __init__(self, library):
        self._library = library

    def add_strategy(self, prefix):
        if prefix[-1:] != '=':
            prefix += '='
        self._strategies.append(prefix)

    def locator_for(self, locator, tagname):
        if self._is_predefined_strategy(locator):
            return locator
        locator = utils.html_attr_escape(locator)
        tagname = self._synonyms.get(tagname, tagname)
        if tagname not in self._tag_attributes:
            return locator
        xpath_attributes = ['%s="%s"' % (attr, locator) for attr in
                            self._tag_attributes[tagname]]
        xpath_attributes.extend(self._get_attrs_requiring_full_url(
                self._tag_attributes[tagname], locator))
        return "xpath=//%s[%s]" % (tagname, ' or '.join(xpath_attributes))

    def _is_predefined_strategy(self, locator):
        if '=' not in locator:
            return False
        prefix = locator.split('=')[0] + '='
        return prefix in self._strategies

    def _get_attrs_requiring_full_url(self, names, locator):
        if '@src' in names:
            return ['@src="%s/%s"' % (self._get_base_url(), locator)]
        if '@href' in names:
            return ['@href="%s/%s"' % (self._get_base_url(), locator)]
        return []

    def _get_base_url(self):
        url = self._library.get_location()
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url
