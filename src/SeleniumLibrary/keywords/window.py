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
import time
from typing import Optional, List, Tuple, Union

from SeleniumLibrary.utils import is_truthy, is_falsy, timestr_to_secs
from selenium.common.exceptions import NoSuchWindowException

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.locators import WindowManager
from SeleniumLibrary.utils import plural_or_not


class WindowKeywords(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._window_manager = WindowManager(ctx)

    @keyword
    def switch_window(
        self,
        locator: Union[list, str] = "MAIN",
        timeout: Optional[str] = None,
        browser: str = "CURRENT",
    ):
        """Switches to browser window matching ``locator``.

        If the window is found, all subsequent commands use the selected
        window, until this keyword is used again. If the window is not
        found, this keyword fails. The previous windows handle is returned
        and can be used to switch back to it later.

        Notice that alerts should be handled with
        `Handle Alert` or other alert related keywords.

        The ``locator`` can be specified using different strategies somewhat
        similarly as when `locating elements` on pages.

        - By default, the ``locator`` is matched against window handle, name,
          title, and URL. Matching is done in that order and the first
          matching window is selected.

        - The ``locator`` can specify an explicit strategy by using the format
          ``strategy:value`` (recommended) or ``strategy=value``. Supported
          strategies are ``name``, ``title``, and ``url``. These matches windows
          using their name, title, or URL, respectively. Additionally, ``default``
          can be used to explicitly use the default strategy explained above.

        - If the ``locator`` is ``NEW`` (case-insensitive), the latest
          opened window is selected. It is an error if this is the same
          as the current window.

        - If the ``locator`` is ``MAIN`` (default, case-insensitive),
          the main window is selected.

        - If the ``locator`` is ``CURRENT`` (case-insensitive), nothing is
          done. This effectively just returns the current window handle.

        - If the ``locator`` is not a string, it is expected to be a list
          of window handles _to exclude_. Such a list of excluded windows
          can be got from `Get Window Handles` before doing an action that
          opens a new window.

        The ``timeout`` is used to specify how long keyword will poll to select
        the new window. The ``timeout`` is new in SeleniumLibrary 3.2.

        Example:
        | `Click Link`      | popup1      |      | # Open new window |
        | `Switch Window`   | example     |      | # Select window using default strategy |
        | `Title Should Be` | Pop-up 1    |      |
        | `Click Button`    | popup2      |      | # Open another window |
        | ${handle} = | `Switch Window`   | NEW  | # Select latest opened window |
        | `Title Should Be` | Pop-up 2    |      |
        | `Switch Window`   | ${handle}   |      | # Select window using handle |
        | `Title Should Be` | Pop-up 1    |      |
        | `Switch Window`   | MAIN        |      | # Select the main window |
        | `Title Should Be` | Main        |      |
        | ${excludes} = | `Get Window Handles` | | # Get list of current windows |
        | `Click Link`      | popup3      |      | # Open one more window |
        | `Switch Window`   | ${excludes} |      | # Select window using excludes |
        | `Title Should Be` | Pop-up 3    |      |

        The ``browser`` argument allows with ``index_or_alias`` to implicitly switch to
        a specific browser when switching to a window. See `Switch Browser`

        - If the ``browser`` is ``CURRENT`` (case-insensitive), no other browser is
          selected.

        *NOTE:*

        - The ``strategy:value`` syntax is only supported by SeleniumLibrary
          3.0 and newer.
        - Prior to SeleniumLibrary 3.0 matching windows by name, title
          and URL was case-insensitive.
        - Earlier versions supported aliases ``None``, ``null`` and the
          empty string for selecting the main window, and alias ``self``
          for selecting the current window. Support for these aliases was
          removed in SeleniumLibrary 3.2.
        """
        epoch = time.time()
        timeout = epoch if is_falsy(timeout) else timestr_to_secs(timeout) + epoch
        try:
            return self.driver.current_window_handle
        except NoSuchWindowException:
            pass
        finally:
            if not isinstance(browser, str) or not browser.upper() == "CURRENT":
                self.drivers.switch(browser)
            self._window_manager.select(locator, timeout)

    @keyword
    def close_window(self):
        """Closes currently opened and selected browser window/tab. """
        self.driver.close()

    @keyword
    def get_window_handles(self, browser: str = "CURRENT") -> List[str]:
        """Returns all child window handles of the selected browser as a list.

        Can be used as a list of windows to exclude with `Select Window`.

        How to select the ``browser`` scope of this keyword, see `Get Locations`.

        Prior to SeleniumLibrary 3.0, this keyword was named `List Windows`.
        """
        return self._window_manager.get_window_handles(browser)

    @keyword
    def get_window_identifiers(self, browser: str = "CURRENT") -> List:
        """Returns and logs id attributes of all windows of the selected browser.

        How to select the ``browser`` scope of this keyword, see `Get Locations`."""
        ids = [info.id for info in self._window_manager.get_window_infos(browser)]
        return self._log_list(ids)

    @keyword
    def get_window_names(self, browser: str = "CURRENT") -> List[str]:
        """Returns and logs names of all windows of the selected browser.

        How to select the ``browser`` scope of this keyword, see `Get Locations`."""
        names = [info.name for info in self._window_manager.get_window_infos(browser)]
        return self._log_list(names)

    @keyword
    def get_window_titles(self, browser: str = "CURRENT") -> List[str]:
        """Returns and logs titles of all windows of the selected browser.

        How to select the ``browser`` scope of this keyword, see `Get Locations`."""
        titles = [info.title for info in self._window_manager.get_window_infos(browser)]
        return self._log_list(titles)

    @keyword
    def get_locations(self, browser: str = "CURRENT") -> List[str]:
        """Returns and logs URLs of all windows of the selected browser.

        *Browser Scope:*

        The ``browser`` argument specifies the browser that shall return
        its windows information.

        - ``browser`` can be ``index_or_alias`` like in `Switch Browser`.

        - If ``browser`` is ``CURRENT`` (default, case-insensitive)
          the currently active browser is selected.

        - If ``browser`` is ``ALL`` (case-insensitive)
          the window information of all windows of all opened browsers are returned."""
        urls = [info.url for info in self._window_manager.get_window_infos(browser)]
        return self._log_list(urls)

    @keyword
    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self.driver.maximize_window()

    @keyword
    def minimize_browser_window(self):
        """Minimizes current browser window."""
        self.driver.minimize_window()

    @keyword
    def get_window_size(self, inner: bool = False) -> Tuple[float, float]:
        """Returns current window width and height as integers.

        See also `Set Window Size`.

        If ``inner`` parameter is set to True, keyword returns
        HTML DOM window.innerWidth and window.innerHeight properties.
        See `Boolean arguments` for more details on how to set boolean
        arguments. The ``inner`` is new in SeleniumLibrary 4.0.

        Example:
        | ${width} | ${height}= | `Get Window Size` |      |
        | ${width} | ${height}= | `Get Window Size` | True |
        """
        if is_truthy(inner):
            inner_width = int(self.driver.execute_script("return window.innerWidth;"))
            inner_height = int(self.driver.execute_script("return window.innerHeight;"))
            return inner_width, inner_height
        size = self.driver.get_window_size()
        return size["width"], size["height"]

    @keyword
    def set_window_size(self, width: int, height: int, inner: bool = False):
        """Sets current windows size to given ``width`` and ``height``.

        Values can be given using strings containing numbers or by using
        actual numbers. See also `Get Window Size`.

        Browsers have a limit on their minimum size. Trying to set them
        smaller will cause the actual size to be bigger than the requested
        size.

        If ``inner`` parameter is set to True, keyword sets the necessary
        window width and height to have the desired HTML DOM _window.innerWidth_
        and _window.innerHeight_. See `Boolean arguments` for more details on how to set boolean
        arguments.

        The ``inner`` argument is new since SeleniumLibrary 4.0.

        This ``inner`` argument does not support Frames. If a frame is selected,
        switch to default before running this.

        Example:
        | `Set Window Size` | 800 | 600 |      |
        | `Set Window Size` | 800 | 600 | True |
        """
        if is_falsy(inner):
            return self.driver.set_window_size(width, height)
        self.driver.set_window_size(width, height)
        inner_width = int(self.driver.execute_script("return window.innerWidth;"))
        inner_height = int(self.driver.execute_script("return window.innerHeight;"))
        self.info(
            f"window.innerWidth is {inner_width} and window.innerHeight is {inner_height}"
        )
        width_offset = width - inner_width
        height_offset = height - inner_height
        window_width = width + width_offset
        window_height = height + height_offset
        self.info(f"Setting window size to {window_width} {window_height}")
        self.driver.set_window_size(window_width, window_height)
        result_width = int(self.driver.execute_script("return window.innerWidth;"))
        result_height = int(self.driver.execute_script("return window.innerHeight;"))
        if result_width != width or result_height != height:
            raise AssertionError("Keyword failed setting correct window size.")

    @keyword
    def get_window_position(self) -> Tuple[int, int]:
        """Returns current window position.

        The position is relative to the top left corner of the screen. Returned
        values are integers. See also `Set Window Position`.

        Example:
        | ${x} | ${y}= | `Get Window Position` |
        """
        position = self.driver.get_window_position()
        return position["x"], position["y"]

    @keyword
    def set_window_position(self, x: int, y: int):
        """Sets window position using ``x`` and ``y`` coordinates.

        The position is relative to the top left corner of the screen,
        but some browsers exclude possible task bar set by the operating
        system from the calculation. The actual position may thus be
        different with different browsers.

        Values can be given using strings containing numbers or by using
        actual numbers. See also `Get Window Position`.

        Example:
        | `Set Window Position` | 100 | 200 |
        """
        self.driver.set_window_position(x, y)

    def _log_list(self, items, what="item"):
        msg = [f"Altogether {len(items)} {what}{plural_or_not(items)}."]
        for index, item in enumerate(items):
            msg.append(f"{index + 1}: {item}")
        self.info("\n".join(msg))
        return items
