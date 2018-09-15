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

from SeleniumLibrary.utils import is_falsy, timestr_to_secs
from selenium.common.exceptions import NoSuchWindowException

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.locators import WindowManager


class WindowKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._window_manager = WindowManager(ctx)

    @keyword
    def select_window(self, locator='MAIN', timeout=None):
        """Selects browser window matching ``locator``.

        If the window is found, all subsequent commands use the selected
        window, until this keyword is used again. If the window is not
        found, this keyword fails. The previous window handle is returned,
        and can be used to return back to it later.

        Notice that in this context _window_ means a pop-up window opened
        when doing something on an existing window. It is not possible to
        select windows opened with `Open Browser`, `Switch Browser` must
        be used instead. Notice also that alerts should be handled with
        `Handle Alert` or other alert related keywords.

        The ``locator`` can be specified using different strategies somewhat
        similarly as when `locating elements` on pages.

        - By default the ``locator`` is matched against window handle, name,
          title, and URL. Matching is done in that order and the the first
          matching window is selected.

        - The ``locator`` can specify an explicit strategy by using format
          ``strategy:value`` (recommended) or ``strategy=value``. Supported
          strategies are ``name``, ``title`` and ``url``, which match windows
          using name, title, and URL, respectively. Additionally, ``default``
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
          can be get from `Get Window Handles` prior to doing an action that
          opens a new window.

        The ``timeout`` is used to specify how long keyword will poll to select
        the new window. The ``timeout`` is new in SeleniumLibrary 3.2.

        Example:
        | `Click Link`      | popup1      |      | # Open new window |
        | `Select Window`   | example     |      | # Select window using default strategy |
        | `Title Should Be` | Pop-up 1    |      |
        | `Click Button`    | popup2      |      | # Open another window |
        | ${handle} = | `Select Window`   | NEW  | # Select latest opened window |
        | `Title Should Be` | Pop-up 2    |      |
        | `Select Window`   | ${handle}   |      | # Select window using handle |
        | `Title Should Be` | Pop-up 1    |      |
        | `Select Window`   | MAIN        |      | # Select the main window |
        | `Title Should Be` | Main        |      |
        | ${excludes} = | `Get Window Handles` | | # Get list of current windows |
        | `Click Link`      | popup3      |      | # Open one more window |
        | `Select Window`   | ${excludes} |      | # Select window using excludes |
        | `Title Should Be` | Pop-up 3    |      |

        *NOTE:*

        - The ``strategy:value`` syntax is only supported by SeleniumLibrary
          3.0 and newer.
        - Prior to SeleniumLibrary 3.0 matching windows by name, title
          and URL was case-insensitive.
        - Earlier versions supported aliases ``None``, ``null`` and the
          empty string for selecting the main window, and alias ``self``
          for selecting the current window. Support for these aliases were
          removed in SeleniumLibrary 3.2.
        """
        epoch = time.time()
        timeout = epoch if is_falsy(timeout) else timestr_to_secs(timeout) + epoch
        try:
            return self.driver.current_window_handle
        except NoSuchWindowException:
            pass
        finally:
            self._window_manager.select(locator, timeout)

    @keyword
    def close_window(self):
        """Closes currently opened pop-up window."""
        self.driver.close()

    @keyword
    def get_window_handles(self):
        """Return all current window handles as a list.

        Can be used as a list of windows to exclude with `Select Window`.

        Prior to SeleniumLibrary 3.0, this keyword was named `List Windows`.
        """
        return self.driver.window_handles

    @keyword
    def list_windows(self):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Get Window Handles` instead."""
        return self.get_window_handles()

    @keyword
    def get_window_identifiers(self):
        """Returns and logs id attributes of all known browser windows."""
        ids = [info.id for info in self._window_manager.get_window_infos()]
        return self._log_list(ids)

    @keyword
    def get_window_names(self):
        """Returns and logs names of all known browser windows."""
        names = [info.name for info in self._window_manager.get_window_infos()]
        return self._log_list(names)

    @keyword
    def get_window_titles(self):
        """Returns and logs titles of all known browser windows."""
        titles = [info.title for info in self._window_manager.get_window_infos()]
        return self._log_list(titles)

    @keyword
    def get_locations(self):
        """Returns and logs URLs of all known browser windows."""
        urls = [info.url for info in self._window_manager.get_window_infos()]
        return self._log_list(urls)

    @keyword
    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self.driver.maximize_window()

    @keyword
    def get_window_size(self):
        """Returns current window width and height as integers.

        See also `Set Window Size`.

        Example:
        | ${width} | ${height}= | `Get Window Size` |
        """
        size = self.driver.get_window_size()
        return size['width'], size['height']

    @keyword
    def set_window_size(self, width, height):
        """Sets current windows size to given ``width`` and ``height``.

        Values can be given using strings containing numbers or by using
        actual numbers. See also `Get Window Size`.

        Browsers have a limit how small they can be set. Trying to set them
        smaller will cause the actual size to be bigger than the requested
        size.

        Example:
        | `Set Window Size` | 800 | 600 |
        """
        return self.driver.set_window_size(int(width), int(height))

    @keyword
    def get_window_position(self):
        """Returns current window position.

        Position is relative to the top left corner of the screen. Returned
        values are integers. See also `Set Window Position`.

        Example:
        | ${x} | ${y}= | `Get Window Position` |
        """
        position = self.driver.get_window_position()
        return position['x'], position['y']

    @keyword
    def set_window_position(self, x, y):
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
        self.driver.set_window_position(int(x), int(y))

    def _log_list(self, items, what='item'):
        msg = [
            'Altogether {} {}.'.format(
                len(items), what if len(items) == 1 else '{}s'.format(what))
        ]
        for index, item in enumerate(items):
            msg.append('{}: {}'.format(index + 1, item))
        self.info('\n'.join(msg))
        return items
