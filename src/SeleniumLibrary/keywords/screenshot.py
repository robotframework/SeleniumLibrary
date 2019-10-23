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

import os
from os.path import basename

from robot.utils import get_link_path

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_noney
from SeleniumLibrary.utils.path_formatter import _format_path
import base64

class ScreenshotKeywords(LibraryComponent):
    DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT = 'selenium-screenshot-{index}.png'
    DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT= 'selenium-element-screenshot-{index}.png'
    EMBED_FLAG = "EMBED"

    @keyword
    def set_screenshot_directory(self, path):
        """Sets the directory for captured screenshots.

        ``path`` argument specifies the absolute path to a directory where
        the screenshots should be written to. If the directory does not
        exist, it will be created. The directory can also be set when
        `importing` the library. If it is not configured anywhere,
        screenshots are saved to the same directory where Robot Framework's
        log file is written.
        The special EMBED word may be used to specify default behavior when
        no filename is specified in the Capture related keywords. In that
        case, screenshots will be embedded in the log file; otherwise,
        screenshots will be saved locally as files and references to them
        in the log file will be used instead.

        The previous value is returned and can be used to restore
        the original value later if needed.

        Returning the previous value is new in SeleniumLibrary 3.0.
        The persist argument was removed in SeleniumLibrary 3.2.
        """
        if is_noney(path):
            path = None
        elif path.upper() == ScreenshotKeywords.EMBED_FLAG:
            path = ScreenshotKeywords.EMBED_FLAG;
        else:
            path = os.path.abspath(path)
            self._create_directory(path)
        previous = self.ctx.screenshot_root_directory
        self.ctx.screenshot_root_directory = path
        return previous

    @keyword
    def capture_page_screenshot(self, filename=DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT):
        """Takes a screenshot of the current page and embeds it into a log file.

        ``filename`` argument specifies the name of the file to write the
        screenshot into. The directory where screenshots are saved can be
        set when `importing` the library or by using the `Set Screenshot
        Directory` keyword. If the directory is not configured, screenshots
        are saved to the same directory where Robot Framework's log file is
        written.
        The special EMBED filename may be used to enforce the screenshot to be
        embedded as Base64 encoded image data in the log file.

        Starting from SeleniumLibrary 1.8, if ``filename`` contains marker
        ``{index}``, it will be automatically replaced with an unique running
        index, preventing files to be overwritten. Indices start from 1,
        and how they are represented can be customized using Python's
        [https://docs.python.org/3/library/string.html#format-string-syntax|
        format string syntax].

        An absolute path to the created screenshot file is returned or EMBED,
        if it has been embedded.

        Examples:
        | `Capture Page Screenshot` |                                        |
        | `File Should Exist`       | ${OUTPUTDIR}/selenium-screenshot-1.png |
        | ${path} =                 | `Capture Page Screenshot`              |
        | `File Should Exist`       | ${OUTPUTDIR}/selenium-screenshot-2.png |
        | `File Should Exist`       | ${path}                                |
        | `Capture Page Screenshot` | custom_name.png                        |
        | `File Should Exist`       | ${OUTPUTDIR}/custom_name.png           |
        | `Capture Page Screenshot` | custom_with_index_{index}.png          |
        | `File Should Exist`       | ${OUTPUTDIR}/custom_with_index_1.png   |
        | `Capture Page Screenshot` | formatted_index_{index:03}.png         |
        | `File Should Exist`       | ${OUTPUTDIR}/formatted_index_001.png   |
        | `Capture Page Screenshot` | EMBED                                  |
        | `File Should Not Exist`   | ${OUTPUTDIR}/selenium-screenshot-1.png |
        """
        if not self.drivers.current:
            self.info('Cannot capture screenshot because no browser is open.')
            return
        path = self._get_screenshot_path(filename)
        if (path == ScreenshotKeywords.EMBED_FLAG):
            screenshot_base64_data =  self.driver.get_screenshot_as_base64()
            self._embed_to_log(screenshot_base64_data, 800)
            #return ScreenshotKeywords.EMBED_FLAG
        else:
            self._create_directory(path)
            if not self.driver.save_screenshot(path):
                raise RuntimeError("Failed to save screenshot '{}'.".format(path))
            self._embed_reference_to_log(path, 800)
        return path

    @keyword
    def capture_element_screenshot(self, locator, filename=DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT):
        """Captures a screenshot from the element identified by ``locator`` and embeds it into log file.

        See `Capture Page Screenshot` for details about ``filename`` argument.
        See the `Locating elements` section for details about the locator
        syntax.

        An absolute path to the created element screenshot is returned or EMBED,
        if it has been embedded.

        Support for capturing the screenshot from an element has limited support
        among browser vendors. Please check the browser vendor driver documentation
        does the browser support capturing a screenshot from an element.

        New in SeleniumLibrary 3.3

        Examples:
        | `Capture Element Screenshot` | id:image_id |                                |
        | `Capture Element Screenshot` | id:image_id | ${OUTPUTDIR}/id_image_id-1.png |
        | `Capture Element Screenshot` | id:image_id | EMBED                          |
        """
        if not self.drivers.current:
            self.info('Cannot capture screenshot from element because no browser is open.')
            return
        path = self._get_screenshot_path(filename)
        if path == ScreenshotKeywords.EMBED_FLAG:
            element = self.find_element(locator, required=True)
            screenshot_base64_data =  base64.b64encode(element.screenshot_as_png)
            self._embed_to_log(screenshot_base64_data, 400)
        else:
            self._create_directory(path)
            element = self.find_element(locator, required=True)
            if not element.screenshot(path):
                raise RuntimeError("Failed to save element screenshot '{}'.".format(path))
            self._embed_reference_to_log(path, 400)
        return path

    def _screenshot_root_directory_is_embed(self):
        return (self.ctx.screenshot_root_directory is not None and self.ctx.screenshot_root_directory.upper() == ScreenshotKeywords.EMBED_FLAG)

    def _screenshot_should_be_embedded(self, path):
        # screenshot should be embedded if path=EMBED or if filename is not defined (i.e. is the default) and screenshot_root_directory is EMBED
        if (path.upper() == ScreenshotKeywords.EMBED_FLAG) or \
              ((path == ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT or path == ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT) and self._screenshot_root_directory_is_embed() == True):
            return True
        else:
            return False

    def _get_screenshot_path(self, filename):
        if self._screenshot_should_be_embedded(filename) == True:
            return ScreenshotKeywords.EMBED_FLAG

        if self._screenshot_root_directory_is_embed():
            if os.path.isabs(filename):
                return filename
            else:
                directory = self.log_dir
        else:
            directory = self.ctx.screenshot_root_directory or self.log_dir

        filename = filename.replace('/', os.sep)
        index = 0
        while True:
            index += 1
            formatted = _format_path(filename, index)
            path = os.path.join(directory, formatted)
            # filename didn't contain {index} or unique path was found
            if formatted == filename or not os.path.exists(path):
                return path

    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

    def _embed_to_log(self, screenshot_base64_data, width):
        # Image is shown on its own row and thus previous row is closed on
        # purpose. Depending on Robot's log structure is a bit risky.
        self.info('</td></tr><tr><td colspan="3">'
                  '<img alt="screenshot" class="robot-seleniumlibrary-screenshot" src="data:image/png;base64,{screenshot_data}" width="{width}px">'
                  .format(screenshot_data=screenshot_base64_data, width=width), html=True)

    def _embed_reference_to_log(self, path, width):
        # Image is shown on its own row and thus previous row is closed on
        # purpose. Depending on Robot's log structure is a bit risky.
        self.info('</td></tr><tr><td colspan="3">'
                  '<a href="{src}"><img src="{src}" width="{width}px"></a>'
                  .format(src=get_link_path(path, self.log_dir), width=width), html=True)