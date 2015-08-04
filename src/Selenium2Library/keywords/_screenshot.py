import robot
import os, errno

from Selenium2Library import utils
from keywordgroup import KeywordGroup


class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = {}
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

    def capture_page_screenshot(self, filename=None, overwrite=False):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is
        saved into file `selenium-screenshot-<counter>.png` under the directory
        where the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format. If an absolute or relative path is given
        but the path does not exist it will be created.

        With `overwrite` it is possible to define what is done if file already
        exist. By default filename is not overwritten but new one is created
        by adding <counter> in the end. Example if capture.png exist and
        this is the first overwrite, then new file is created with name
        capture-1.png

        Example:
        | Open Browser | www.someurl.com | browser=${BROWSER} |
        | Capture Page Screenshot | filename=${BROWSER} |
        | Capture Page Screenshot | filename=${BROWSER} |
        | Capture Page Screenshot | filename=${BROWSER} |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}.png |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}-1.png |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}-2.png |
        | Capture Page Screenshot |
        | Capture Page Screenshot |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-1.png |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-2.png |
        | Capture Page Screenshot | filename=DefaultName.png | overwrite=${True} |
        | Capture Page Screenshot | filename=DefaultName.png | overwrite=${True} |
        | File Should Exist  | ${OUTPUTDIR}${/}DefaultName.png |
        | File Should Not Exist | ${OUTPUTDIR}${/}DefaultName-1.png |

        *NOTE:* The `overwrite` is ignored if `filename` is not defined
        Example:
        | Open Browser | www.someurl.com | browser=${BROWSER} |
        | Capture Page Screenshot | overwrite=${True} | # overwrite is ignored |
        | Capture Page Screenshot | overwrite=${True} | # overwrite is ignored |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-1.png |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-2.png |
        """

        path, link = self._get_screenshot_paths(filename, overwrite=overwrite)
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

    def _get_screenshot_paths(self, filename, overwrite=False):
        if not filename:
            index = self._get_new_index('selenium-screenshot')
            filename = 'selenium-screenshot-%d.png' % index
        elif filename and not overwrite:
            filename = self._screenshot_existence(filename.replace('/',
                                                                   os.sep))
        else:
            filename = filename.replace('/', os.sep)

        screenshot_dir = self._get_screenshot_directory()
        logdir = self._get_log_dir()
        path = os.path.join(screenshot_dir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _screenshot_existence(self, filename):
        if os.path.exists(self._get_logdir_path(filename)[0]):
            index = self._get_new_index(filename)
            try:
                return '-%s.png'.join(filename.rsplit('.png', 1)) % index
            except TypeError:
                return filename + '-%s' % index
        else:
            return filename

    def _get_logdir_path(self, filename):
        logdir = self._get_log_dir()
        return os.path.join(logdir, filename), logdir

    def _get_new_index(self, filename):
        try:
            index = self._screenshot_index[filename] + 1
            self._screenshot_index[filename] = index
            return index
        except KeyError:
            self._screenshot_index[filename] = 1
            return 1
