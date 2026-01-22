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
import base64
from typing import Optional, Union

from robot.utils import get_link_path
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.print_page_options import PrintOptions, Orientation

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils.path_formatter import _format_path

DEFAULT_FILENAME_PAGE = "selenium-screenshot-{index}.png"
DEFAULT_FILENAME_ELEMENT = "selenium-element-screenshot-{index}.png"
DEFAULT_FILENAME_FULLPAGE = "selenium-fullpage-screenshot-{index}.png"
EMBED = "EMBED"
BASE64 = "BASE64"
EMBEDDED_OPTIONS = [EMBED, BASE64]
DEFAULT_FILENAME_PDF = "selenium-page-{index}.pdf"


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
        elif path.upper() == BASE64:
            path = BASE64
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
        created in the filesystem. If ``filename`` equals to BASE64 (case
        insensitive), then the base64 string is returned and the screenshot
        is embedded to the log. This allows one to reuse the image elsewhere
        in the report.

        Example:
        | ${ss}=            | `Capture Page Screenshot`  | BASE64                                          |
        | Set Test Message  |   *HTML*Test Success<p><img src="data:image/png;base64,${ss}" width="256px"> |

        Starting from SeleniumLibrary 1.8, if ``filename`` contains marker
        ``{index}``, it will be automatically replaced with an unique running
        index, preventing files to be overwritten. Indices start from 1,
        and how they are represented can be customized using Python's
        [https://docs.python.org/3/library/string.html#format-string-syntax|
        format string syntax].

        An absolute path to the created screenshot file is returned or if
        ``filename``  equals to EMBED, word `EMBED` is returned. If ``filename``
        equals to BASE64, the base64 string containing the screenshot is returned.

        Support for BASE64 is new in SeleniumLibrary 6.8

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
        is_embedded, method = self._decide_embedded(filename)
        if is_embedded:
            return self._capture_page_screen_to_log(method)
        return self._capture_page_screenshot_to_file(filename)

    def _capture_page_screenshot_to_file(self, filename):
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if not self.driver.save_screenshot(path):
            raise RuntimeError(f"Failed to save screenshot '{path}'.")
        self._embed_to_log_as_file(path, 800)
        return path

    def _capture_page_screen_to_log(self, return_val):
        screenshot_as_base64 = self.driver.get_screenshot_as_base64()
        base64_str = self._embed_to_log_as_base64(screenshot_as_base64, 800)
        if return_val == BASE64:
            return base64_str
        return EMBED

    @keyword
    def capture_element_screenshot(
        self,
        locator: Union[WebElement, str],
        filename: str = DEFAULT_FILENAME_ELEMENT,
    ) -> str:
        """Captures a screenshot from the element identified by ``locator`` and embeds it into log file.

        See `Capture Page Screenshot` for details about ``filename`` argument.
        See the `Locating elements` section for details about the locator
        syntax.

        An absolute path to the created element screenshot is returned. If the ``filename``
        equals to BASE64 (case insensitive), then the base64 string is returned in addition
        to the screenshot embedded to the log. See ``Capture Page Screenshot`` for more
        information.

        Support for capturing the screenshot from an element has limited support
        among browser vendors. Please check the browser vendor driver documentation
        does the browser support capturing a screenshot from an element.

        New in SeleniumLibrary 3.3. Support for EMBED is new in SeleniumLibrary 4.2.
        Support for BASE64 is new in SeleniumLibrary 6.8.

        Examples:
        | `Capture Element Screenshot` | id:image_id |                                |
        | `Capture Element Screenshot` | id:image_id | ${OUTPUTDIR}/id_image_id-1.png |
        | `Capture Element Screenshot` | id:image_id | EMBED                          |
        | ${ess}= | `Capture Element Screenshot` | id:image_id | BASE64               |

        """
        if not self.drivers.current:
            self.info(
                "Cannot capture screenshot from element because no browser is open."
            )
            return
        element = self.find_element(locator, required=True)
        is_embedded, method = self._decide_embedded(filename)
        if is_embedded:
            return self._capture_element_screen_to_log(element, method)
        return self._capture_element_screenshot_to_file(element, filename)

    def _capture_element_screenshot_to_file(self, element, filename):
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if not element.screenshot(path):
            raise RuntimeError(f"Failed to save element screenshot '{path}'.")
        self._embed_to_log_as_file(path, 400)
        return path

    def _capture_element_screen_to_log(self, element, return_val):
        base64_str = self._embed_to_log_as_base64(element.screenshot_as_base64, 400)
        if return_val == BASE64:
            return base64_str
        return EMBED

    @keyword
    def capture_fullpage_screenshot(self, filename: str = DEFAULT_FILENAME_FULLPAGE) -> str:
        """Takes a screenshot of the entire page, including parts not visible in viewport.

        This keyword captures the full height and width of a web page, even if it extends
        beyond the current viewport. The implementation automatically selects the best
        available method based on the browser:

        *Screenshot Methods (in order of preference):*

        1. **Chrome DevTools Protocol (CDP)**: Used for Chrome, Edge, and Chromium browsers.
           Works in both headless and non-headless mode without screen size limitations.

        2. **Firefox Native Method**: Used for Firefox browsers. Captures full page
           using the browser's built-in capability.

        3. **Window Resize Method**: Fallback for other browsers. Temporarily resizes
           the browser window to match page dimensions. In non-headless mode, this may
           be limited by physical screen size, and a warning will be logged if the full
           page cannot be captured.

        ``filename`` argument specifies where to save the screenshot file.
        The directory can be set with `Set Screenshot Directory` keyword or
        when importing the library. If not configured, screenshots go to the
        same directory as Robot Framework's log file.

        If ``filename`` is EMBED (case insensitive), the screenshot gets embedded
        as Base64 image in log.html without creating a file. If it's BASE64,
        the base64 string is returned and also embedded in the log.

        The ``{index}`` marker in filename gets replaced with a unique number
        to prevent overwriting files. You can customize the format like
        ``{index:03}`` for zero-padded numbers.

        Returns the absolute path to the screenshot file, or EMBED/BASE64 string
        if those options are used.

        Examples:
        | `Capture Fullpage Screenshot` |                                        |
        | `File Should Exist`           | ${OUTPUTDIR}/selenium-fullpage-screenshot-1.png |
        | ${path} =                     | `Capture Fullpage Screenshot`          |
        | `Capture Fullpage Screenshot` | custom_fullpage.png                    |
        | `Capture Fullpage Screenshot` | custom_{index}.png                     |
        | `Capture Fullpage Screenshot` | EMBED                                  |
        """
        if not self.drivers.current:
            self.info("Cannot capture fullpage screenshot because no browser is open.")
            return
        is_embedded, method = self._decide_embedded(filename)
        if is_embedded:
            return self._capture_fullpage_screen_to_log(method)
        return self._capture_fullpage_screenshot_to_file(filename)

    def _capture_fullpage_screenshot_to_file(self, filename):
        """Save fullpage screenshot to file using best available method."""
        # Try CDP first (Chrome/Edge/Chromium) - works in both headless and non-headless
        if self._supports_cdp():
            result = self._capture_fullpage_via_cdp(filename)
            if result:
                self.debug("Full-page screenshot captured using Chrome DevTools Protocol")
                return result
        
        # Try Firefox native method
        if self._supports_native_fullpage():
            result = self._capture_fullpage_via_firefox(filename)
            if result:
                self.debug("Full-page screenshot captured using Firefox native method")
                return result
        
        # Fallback to resize method (works in headless mode for all browsers)
        self.debug("Using window resize method for full-page screenshot")
        return self._capture_fullpage_via_resize(filename)

    def _capture_fullpage_via_resize(self, filename):
        """Fallback method: Save fullpage screenshot by resizing window."""
        # Remember current window size so we can restore it later
        original_size = self.driver.get_window_size()
        
        try:
            # Get the actual page height - this covers all the content
            full_height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            
            # Resize window to show the full page
            self.driver.set_window_size(original_size['width'], full_height)
            
            # Give the page a moment to render after resize
            import time
            time.sleep(0.5)
            
            # Verify the window actually resized to requested dimensions
            # In non-headless mode, browsers may be limited by screen size
            actual_size = self.driver.get_window_size()
            if actual_size['height'] < full_height * 0.95:  # Allow 5% tolerance for browser chrome
                self.warn(
                    f"Browser window could not be resized to full page height. "
                    f"Requested: {full_height}px, Actual: {actual_size['height']}px. "
                    f"Screenshot may not capture the complete page. "
                    f"Consider running in headless mode for better full-page screenshot support."
                )
            
            # Now take the screenshot
            path = self._get_screenshot_path(filename)
            self._create_directory(path)
            if not self.driver.save_screenshot(path):
                raise RuntimeError(f"Failed to save fullpage screenshot '{path}'.")
            self._embed_to_log_as_file(path, 800)
            return path
            
        finally:
            # Put the window back to its original size
            self.driver.set_window_size(original_size['width'], original_size['height'])

    def _capture_fullpage_screen_to_log(self, return_val):
        """Get fullpage screenshot as base64 or embed it using best available method."""
        screenshot_as_base64 = None
        
        # Try CDP first (Chrome/Edge/Chromium) - works in both headless and non-headless
        if self._supports_cdp():
            screenshot_as_base64 = self._capture_fullpage_via_cdp_base64()
            if screenshot_as_base64:
                self.debug("Full-page screenshot captured using Chrome DevTools Protocol")
        
        # Try Firefox native method
        if not screenshot_as_base64 and self._supports_native_fullpage():
            screenshot_as_base64 = self._capture_fullpage_via_firefox_base64()
            if screenshot_as_base64:
                self.debug("Full-page screenshot captured using Firefox native method")
        
        # Fallback to resize method
        if not screenshot_as_base64:
            self.debug("Using window resize method for full-page screenshot")
            screenshot_as_base64 = self._capture_fullpage_via_resize_base64()
        
        # Embed to log
        base64_str = self._embed_to_log_as_base64(screenshot_as_base64, 800)
        if return_val == BASE64:
            return base64_str
        return EMBED

    def _capture_fullpage_via_resize_base64(self):
        """Fallback method: Get fullpage screenshot as base64 by resizing window."""
        # Remember current window size so we can restore it later
        original_size = self.driver.get_window_size()
        
        try:
            # Get the actual page height - this covers all the content
            full_height = self.driver.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
            
            # Resize window to show the full page
            self.driver.set_window_size(original_size['width'], full_height)
            
            # Give the page a moment to render after resize
            import time
            time.sleep(0.5)
            
            # Verify the window actually resized to requested dimensions
            # In non-headless mode, browsers may be limited by screen size
            actual_size = self.driver.get_window_size()
            if actual_size['height'] < full_height * 0.95:  # Allow 5% tolerance for browser chrome
                self.warn(
                    f"Browser window could not be resized to full page height. "
                    f"Requested: {full_height}px, Actual: {actual_size['height']}px. "
                    f"Screenshot may not capture the complete page. "
                    f"Consider running in headless mode for better full-page screenshot support."
                )
            
            # Take the screenshot as base64
            screenshot_as_base64 = self.driver.get_screenshot_as_base64()
            return screenshot_as_base64
            
        finally:
            # Put the window back to its original size
            self.driver.set_window_size(original_size['width'], original_size['height'])

    def _get_browser_name(self):
        """Get the name of the current browser."""
        try:
            return self.driver.capabilities.get('browserName', '').lower()
        except:
            return ''

    def _supports_cdp(self):
        """Check if browser supports Chrome DevTools Protocol."""
        browser_name = self._get_browser_name()
        return browser_name in ['chrome', 'chromium', 'msedge', 'edge', 'MicrosoftEdge']

    def _supports_native_fullpage(self):
        """Check if browser supports native full-page screenshots."""
        browser_name = self._get_browser_name()
        return browser_name == 'firefox'

    def _capture_fullpage_via_cdp(self, filename):
        """Capture full-page screenshot using Chrome DevTools Protocol."""
        try:
            # Get page dimensions
            metrics = self.driver.execute_cdp_cmd('Page.getLayoutMetrics', {})
            width = int(metrics['contentSize']['width'])
            height = int(metrics['contentSize']['height'])
            
            # Capture screenshot with full page dimensions
            screenshot = self.driver.execute_cdp_cmd('Page.captureScreenshot', {
                'clip': {
                    'width': width,
                    'height': height,
                    'x': 0,
                    'y': 0,
                    'scale': 1
                },
                'captureBeyondViewport': True
            })
            
            # Save the screenshot
            path = self._get_screenshot_path(filename)
            self._create_directory(path)
            
            with open(path, 'wb') as f:
                f.write(base64.b64decode(screenshot['data']))
            
            self._embed_to_log_as_file(path, 800)
            return path
        except Exception as e:
            self.debug(f"CDP full-page screenshot failed: {e}. Falling back to resize method.")
            return None

    def _capture_fullpage_via_cdp_base64(self):
        """Capture full-page screenshot using CDP and return as base64."""
        try:
            # Get page dimensions
            metrics = self.driver.execute_cdp_cmd('Page.getLayoutMetrics', {})
            width = int(metrics['contentSize']['width'])
            height = int(metrics['contentSize']['height'])
            
            # Capture screenshot with full page dimensions
            screenshot = self.driver.execute_cdp_cmd('Page.captureScreenshot', {
                'clip': {
                    'width': width,
                    'height': height,
                    'x': 0,
                    'y': 0,
                    'scale': 1
                },
                'captureBeyondViewport': True
            })
            
            return screenshot['data']
        except Exception as e:
            self.debug(f"CDP full-page screenshot failed: {e}. Falling back to resize method.")
            return None

    def _capture_fullpage_via_firefox(self, filename):
        """Capture full-page screenshot using Firefox native method."""
        try:
            path = self._get_screenshot_path(filename)
            self._create_directory(path)
            
            # Firefox has a native full-page screenshot method
            screenshot_binary = self.driver.get_full_page_screenshot_as_png()
            
            with open(path, 'wb') as f:
                f.write(screenshot_binary)
            
            self._embed_to_log_as_file(path, 800)
            return path
        except Exception as e:
            self.debug(f"Firefox native full-page screenshot failed: {e}. Falling back to resize method.")
            return None

    def _capture_fullpage_via_firefox_base64(self):
        """Capture full-page screenshot using Firefox and return as base64."""
        try:
            screenshot_binary = self.driver.get_full_page_screenshot_as_png()
            return base64.b64encode(screenshot_binary).decode('utf-8')
        except Exception as e:
            self.debug(f"Firefox native full-page screenshot failed: {e}. Falling back to resize method.")
            return None

    @property
    def _screenshot_root_directory(self):
        return self.ctx.screenshot_root_directory

    @_screenshot_root_directory.setter
    def _screenshot_root_directory(self, value):
        self.ctx.screenshot_root_directory = value

    def _decide_embedded(self, filename):
        filename = filename.upper()
        if (
            filename == DEFAULT_FILENAME_PAGE.upper()
            and self._screenshot_root_directory in EMBEDDED_OPTIONS
        ):
            return True, self._screenshot_root_directory
        if (
            filename == DEFAULT_FILENAME_ELEMENT.upper()
            and self._screenshot_root_directory in EMBEDDED_OPTIONS
        ):
            return True, self._screenshot_root_directory
        if (
            filename == DEFAULT_FILENAME_FULLPAGE.upper()
            and self._screenshot_root_directory in EMBEDDED_OPTIONS
        ):
            return True, self._screenshot_root_directory
        if filename in EMBEDDED_OPTIONS:
            return True, self._screenshot_root_directory
        return False, None

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
    
    @keyword
    def print_page_as_pdf(self,
                            filename: str = DEFAULT_FILENAME_PDF,
                            background: Optional[bool]  = None,
                            margin_bottom: Optional[float] = None,
                            margin_left: Optional[float] = None,
                            margin_right: Optional[float] = None,
                            margin_top: Optional[float] = None,
                            orientation: Optional[Orientation] = None,
	                        page_height: Optional[float] = None,
                            page_ranges: Optional[list]  = None,
                            page_width: Optional[float] = None,
                            scale: Optional[float] = None,
	                        shrink_to_fit: Optional[bool]  = None,
                            # path_to_file=None,
                         ):
        """ Print the current page as a PDF

        ``page_ranges`` defaults to `['-']` or "all" pages. ``page_ranges`` takes a list of
        strings indicating the ranges.

        The page size defaults to 21.59 for ``page_width`` and 27.94 for ``page_height``.
        This is the equivalent size of US-Letter. The assumed units on these parameters
        is centimeters.

        The default margin for top, left, bottom, right is `1`. The assumed units on
        these parameters is centimeters.

        The default ``orientation`` is `portrait`. ``orientation`` can be either `portrait`
        or `landscape`.

        The default ``scale`` is `1`. ``scale`` must be greater than or equal to `0.1` and
        less than or equal to `2`.

        ``background`` and ``scale_to_fit`` can be either `${True}` or `${False}`..

        If all print options are None then a pdf will fail to print silently.
        """

        if page_ranges is None:
            page_ranges = ['-']

        print_options = PrintOptions()
        if background is not None:
            print_options.background =  background
        if margin_bottom is not None:
            print_options.margin_bottom = margin_bottom
        if margin_left is not None:
            print_options.margin_left = margin_left
        if margin_right is not None:
            print_options.margin_right = margin_right
        if margin_top is not None:
            print_options.margin_top = margin_top
        if orientation is not None:
            print_options.orientation = orientation
        if page_height is not None:
            print_options.page_height = page_height
        if page_ranges is not None:
            print_options.page_ranges = page_ranges
        if page_width is not None:
            print_options.page_width = page_width
        if scale is not None:
            print_options.scale = scale
        if shrink_to_fit is not None:
            print_options.shrink_to_fit = shrink_to_fit

        if not self.drivers.current:
            self.info("Cannot print page to pdf because no browser is open.")
            return
        return self._print_page_as_pdf_to_file(filename, print_options)

    def _print_page_as_pdf_to_file(self, filename, options):
        path = self._get_pdf_path(filename)
        self._create_directory(path)
        pdfdata = self.driver.print_page(options)
        if not pdfdata:
            raise RuntimeError(f"Failed to print page.")
        self._save_pdf_to_file(pdfdata, path)
        return path

    def _save_pdf_to_file(self, pdfbase64, path):
        pdfdata = base64.b64decode(pdfbase64)
        with open(path, mode='wb') as pdf:
            pdf.write(pdfdata)

    def _get_pdf_path(self, filename):
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
