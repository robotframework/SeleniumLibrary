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

import os

from runonfailure import RunOnFailure


class TextField(RunOnFailure):
    """Contains keywords that operate on text fields."""

    def textfield_should_contain(self, locator, expected, message=''):
        """Verifies text field identified by `locator` contains text `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self.get_value(locator)
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def textfield_value_should_be(self, locator, expected, message=''):
        """Verifies the value in text field identified by `locator` is exactly `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self.get_value(locator)
        if actual != expected:
            if not message:
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Content of text field '%s' is '%s'." % (locator, expected))

    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._selenium.type(self._parse_locator(locator), text)

    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        self._selenium.type(self._parse_locator(locator), text)

    def choose_file(self, identifier, file_path):
        """Inputs the `file_path` into file input field found by `identifier`.

        This keyword is most often used to input files into upload forms.
        In normal usage the file specified with `file_path` must be available
        on the same host where the Selenium Server is running.

        An alternative usage is specifying the `file_path` with an URL
        (starting with `http://` or `https://`) in which case the file
        will be downloaded automatically. The limitations of this
        method are that it only works on Firefox and the file must be
        placed at the root level of a web server.

        Example:
        | Choose File | my_upload_field | /home/user/files/trades.csv |
        | Choose File | my_upload_field | http://uploadhost.com/trades.csv |

        The support for remote files was added in SeleniumLibrary 2.3.2.
        It uses Selenium's `attach_file` method which is explained at
        http://saucelabs.com/blog/index.php/2009/11/selenium-tip-of-the-week-upload-files-on-browsers-running-over-remote-machines/
        """
        if file_path.startswith(('http://', 'https://')):
            self._selenium.attach_file(identifier, file_path)
        else:
            if not os.path.isfile(file_path):
                self._info("File '%s' does not exist on the local file system"
                           % file_path)
            self._selenium.type(identifier, file_path)
