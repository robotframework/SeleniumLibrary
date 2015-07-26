import robot
import os, errno

from Selenium2Library import utils
from keywordgroup import KeywordGroup


class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0
        self._screenshot_path_stack = []
        self.screenshot_root_directory = None

    # Public

    def set_screenshot_directory(self, path, persist=False):
        """Sets the root output directory for captured screenshots.

        ``path`` argument specifies the absolute path where the screenshots should
        be written to. If the specified ``path`` does not exist, it will be created.
        Setting ``persist`` specifies that the given ``path`` should
        be used for the rest of the test execution, otherwise the path will be restored
        at the end of the currently executing scope.
        """
        path = os.path.abspath(path)
        self._create_directory(path)
        if persist is False:
            self._screenshot_path_stack.append(self.screenshot_root_directory)
            # Restore after current scope ends
            utils.events.on('scope_end', 'current', self._restore_screenshot_directory)

        self.screenshot_root_directory = path

    def capture_page_screenshot(self, filename=None):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `selenium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format. If an absolute or relative path is given
        but the path does not exist it will be created.

        `css` can be used to modify how the screenshot is taken. By default
        the bakground color is changed to avoid possible problems with
        background leaking when the page layout is somehow broken.
        """
        path, link = self._get_screenshot_paths(filename)
        self._create_directory(path)

        if hasattr(self._current_browser(), 'get_screenshot_as_file'):
          if not self._current_browser().get_screenshot_as_file(path):
              raise RuntimeError('Failed to save screenshot ' + filename)
        else:
          if not self._current_browser().save_screenshot(path):
            raise RuntimeError('Failed to save screenshot ' + filename)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    # Private
    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else:
                    raise

    def _get_screenshot_directory(self):

        # Use screenshot root directory if set
        if self.screenshot_root_directory is not None:
            return self.screenshot_root_directory

        # Otherwise use RF's log directory
        return self._get_log_dir()

    # should only be called by set_screenshot_directory
    def _restore_screenshot_directory(self):
        self.screenshot_root_directory = self._screenshot_path_stack.pop()

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'selenium-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)

        screenshotDir = self._get_screenshot_directory()
        logDir = self._get_log_dir()
        path = os.path.join(screenshotDir, filename)
        link = robot.utils.get_link_path(path, logDir)
        return path, link
