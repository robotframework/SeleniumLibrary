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

import os
import base64

from robot import utils


class Screenshot(object):

    def capture_screenshot(self, filename=None):
        """Takes a screenshot of the entire screen and embeds it into the log.

        If no `filename` is given, the screenshot is saved into file
        `selenium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format.

        When running on a locked Windows machine, the resulting screenshots
        will be all black. A workaround is using the `Capture Page Screenshot`
        keyword instead.

        There were some changes to this keyword in the 2.3 release:
        - Possibility to take screenshots also when the Selenium Server is
          running on a remote machine was added.
        - Support for absolute `filename` paths was added.
        - Automatic creation of intermediate directories in the path
          where the screenshot is saved was removed.
          `OperatingSystem.Create Directory` can be used instead.
        """
        data = self._selenium.capture_screenshot_to_string()
        self._save_screenshot(data, filename)

    def capture_page_screenshot(self, filename=None, css='background=#CCFFDD'):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. It works the same was as with `Capture Screenshot`.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.

        Selenium currently supports this keyword out-of-the-box only with
        Firefox browser. To make it work with IE, you can start the Selenium
        Server with `-singleWindow` option and use `*ieproxy` as the browser.
        Additionally, the browser independent `Capture Screenshot` keyword
        can be used instead.

        This keyword was added in SeleniumLibrary 2.3.
        """
        data = self._selenium.capture_entire_page_screenshot_to_string(css)
        self._save_screenshot(data, filename)

    def _save_screenshot(self, data, filename):
        path, link = self._get_screenshot_paths(filename)
        outfile = open(path, 'wb')
        # 'decodestring' is used instead of 'b64decode'to support Jython 2.2
        outfile.write(base64.decodestring(data))
        outfile.close()
        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    def _get_screenshot_paths(self, filename):
        if not filename:
            filename = self._namegen.next()
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = utils.get_link_path(path, logdir)
        return path, link
