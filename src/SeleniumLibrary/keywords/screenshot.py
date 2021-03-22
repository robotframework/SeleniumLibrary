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
from typing import Union

from robot.utils import get_link_path
from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils.path_formatter import _format_path

DEFAULT_FILENAME_PAGE = "selenium-screenshot-{index}.png"
DEFAULT_FILENAME_ELEMENT = "selenium-element-screenshot-{index}.png"
EMBED = "EMBED"


class ScreenshotKeywords(LibraryComponent):
    @keyword
    def set_screenshot_directory(self, path: Union[None, str]) -> str:
        """Sets the directory for captured screenshots.

        ``path`` argument specifies the absolute path to a directory where
        the screenshots should be written to. If the directory does not
        exist, it will be created. The directory can also be set when
        `importing` the library. If it is not configured anywhere,
        screenshots are saved to the same directory where Robot Framework's
        log file is written.

        If ``path`` equals to EMBED (case insensitive) and
        `Capture Page Screenshot` or `capture Element Screenshot` keywords
        filename argument is not changed from the default value, then
        the page or element screenshot is embedded as Base64 image to
        the log.html.

        The previous value is returned and can be used to restore
        the original value later if needed.

        Returning the previous value is new in SeleniumLibrary 3.0.
        The persist argument was removed in SeleniumLibrary 3.2 and
        EMBED is new in SeleniumLibrary 4.2.
        """
        if path is None:
            path = None
        elif path.upper() == EMBED:
            path = EMBED
        else:
            path = os.path.abspath(path)
            self._create_directory(path)
        previous = self._screenshot_root_directory
        self._screenshot_root_directory = path
        return previous

    @keyword
    def capture_page_screenshot(self, filename: str = DEFAULT_FILENAME_PAGE) -> str:
        """Takes a screenshot of the current page and embeds it into a log file.

        ``filename`` argument specifies the name of the file to write the
        screenshot into. The directory where screenshots are saved can be
        set when `importing` the library or by using the `Set Screenshot
        Directory` keyword. If the directory is not configured, screenshots
        are saved to the same directory where Robot Framework's log file is
        written.

        If ``filename`` equals to EMBED (case insensitive), then screenshot
        is embedded as Base64 image to the log.html. In this case file is not
        created in the filesystem.

        Starting from SeleniumLibrary 1.8, if ``filename`` contains marker
        ``{index}``, it will be automatically replaced with an unique running
        index, preventing files to be overwritten. Indices start from 1,
        and how they are represented can be customized using Python's
        [https://docs.python.org/3/library/string.html#format-string-syntax|
        format string syntax].

        An absolute path to the created screenshot file is returned or if
        ``filename``  equals to EMBED, word `EMBED` is returned.

        Support for EMBED is new in SeleniumLibrary 4.2

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
        | `File Should Not Exist`   | EMBED                                  |
        """
        if not self.drivers.current:
            self.info("Cannot capture screenshot because no browser is open.")
            return
        if self._decide_embedded(filename):
            return self._capture_page_screen_to_log()
        return self._capture_page_screenshot_to_file(filename)

    def _capture_page_screenshot_to_file(self, filename):
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if not self.driver.save_screenshot(path):
            raise RuntimeError(f"Failed to save screenshot '{path}'.")
        self._embed_to_log_as_file(path, 800)
        return path

    def _capture_page_screen_to_log(self):
        screenshot_as_base64 = self.driver.get_screenshot_as_base64()
        self._embed_to_log_as_base64(screenshot_as_base64, 800)
        return EMBED

    @keyword
    def capture_element_screenshot(
        self,
        locator: Union[WebElement, None, str],
        filename: str = DEFAULT_FILENAME_ELEMENT,
    ) -> str:
        """Captures a screenshot from the element identified by ``locator`` and embeds it into log file.

        See `Capture Page Screenshot` for details about ``filename`` argument.
        See the `Locating elements` section for details about the locator
        syntax.

        An absolute path to the created element screenshot is returned.

        Support for capturing the screenshot from an element has limited support
        among browser vendors. Please check the browser vendor driver documentation
        does the browser support capturing a screenshot from an element.

        New in SeleniumLibrary 3.3. Support for EMBED is new in SeleniumLibrary 4.2.

        Examples:
        | `Capture Element Screenshot` | id:image_id |                                |
        | `Capture Element Screenshot` | id:image_id | ${OUTPUTDIR}/id_image_id-1.png |
        | `Capture Element Screenshot` | id:image_id | EMBED                          |
        """
        if not self.drivers.current:
            self.info(
                "Cannot capture screenshot from element because no browser is open."
            )
            return
        element = self.find_element(locator, required=True)
        if self._decide_embedded(filename):
            return self._capture_element_screen_to_log(element)
        return self._capture_element_screenshot_to_file(element, filename)

    def _capture_element_screenshot_to_file(self, element, filename):
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if not element.screenshot(path):
            raise RuntimeError(f"Failed to save element screenshot '{path}'.")
        self._embed_to_log_as_file(path, 400)
        return path

    def _capture_element_screen_to_log(self, element):
        self._embed_to_log_as_base64(element.screenshot_as_base64, 400)
        return EMBED

    @property
    def _screenshot_root_directory(self):
        return self.ctx.screenshot_root_directory

    @_screenshot_root_directory.setter
    def _screenshot_root_directory(self, value):
        self.ctx.screenshot_root_directory = value

    def _decide_embedded(self, filename):
        filename = filename.lower()
        if (
            filename == DEFAULT_FILENAME_PAGE
            and self._screenshot_root_directory == EMBED
        ):
            return True
        if (
            filename == DEFAULT_FILENAME_ELEMENT
            and self._screenshot_root_directory == EMBED
        ):
            return True
        if filename == EMBED.lower():
            return True
        return False

    def _get_screenshot_path(self, filename):
        if self._screenshot_root_directory != EMBED:
            directory = self._screenshot_root_directory or self.log_dir
        else:
            directory = self.log_dir
        filename = filename.replace("/", os.sep)
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

    def _embed_to_log_as_base64(self, screenshot_as_base64, width):
        # base64 image is shown as on its own row and thus previous row is closed on
        # purpose. Depending on Robot's log structure is a bit risky.
        self.info(
            '</td></tr><tr><td colspan="3">'
            '<img alt="screenshot" class="robot-seleniumlibrary-screenshot" '
            f'src="data:image/png;base64,{screenshot_as_base64}" width="{width}px">',
            html=True,
        )

    def _embed_to_log_as_file(self, path, width):
        # Image is shown on its own row and thus previous row is closed on
        # purpose. Depending on Robot's log structure is a bit risky.
        src = get_link_path(path, self.log_dir)
        self.info(
            '</td></tr><tr><td colspan="3">'
            f'<a href="{src}"><img src="{src}" width="{width}px"></a>',
            html=True,
        )
