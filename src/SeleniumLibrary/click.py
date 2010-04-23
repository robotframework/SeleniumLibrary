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

class Click(object):

    def _click(self, locator, dont_wait=''):
        self._selenium.click(locator)
        if not dont_wait:
            self._wait_for_page_to_load()
    
    def click_element(self, locator, dont_wait=''):
        """Click element identified by `locator`.
        
        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking element '%s'." % locator)
        self._click(self._parse_locator(locator), dont_wait)

    def click_link(self, locator, dont_wait=''):
        """Clicks a link identified by locator.
        
        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking link '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'link'), dont_wait)
        except Exception, err:
            if 'not found' not in self._get_error_message(err):
                raise
            self._click("link=%s" % locator, dont_wait)

    def click_button(self, locator, dont_wait=''):
        """Clicks a button identified by `locator`.
        
        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking button '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'input'), dont_wait)
        except Exception, err:
            if 'ERROR: Element xpath=//' not in self._get_error_message(err):
                raise
            self._click(self._parse_locator(locator, 'button'), dont_wait)    
    
    def click_image(self, locator, dont_wait=''):
        """Clicks an image found by `locator`.
        
        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking image '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'image'), dont_wait)
        except Exception, err:
            if not 'ERROR Element xpath=//' not in self._get_error_message(err):
                raise
            self._click(self._parse_locator(locator, 'input'), dont_wait)

    def submit_form(self, locator='', dont_wait=''):
        """Submits a form identified by `locator`.
        
        If `locator` is empty, first form in the page will be submitted.
        Key attributes for forms are `id` and `name`. See `introduction` for
        details about locating elements and about meaning of `dont_wait`
        argument.
        """
        self._info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        else:
            locator = self._parse_locator(locator)
        self._selenium.submit(locator)
        if not dont_wait:
            self._wait_for_page_to_load()

