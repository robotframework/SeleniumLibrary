import errno
import os
import re

from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.utils import get_link_path

from Selenium2Library.base import LibraryComponent, keyword
from Selenium2Library.utils import events
from Selenium2Library.utils import is_falsy


class ScreenshotKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._screenshot_index = {}
        self._screenshot_path_stack = []
        self.screenshot_root_directory = None

    @keyword
    def set_screenshot_directory(self, path, persist=False):
        """Sets the root output directory for captured screenshots.

        ``path`` argument specifies the absolute path where the screenshots
        should be written to. If the specified ``path`` does not exist,
        it will be created. Setting ``persist`` specifies that the given
        ``path`` should be used for the rest of the test execution, otherwise
        the path will be restored at the end of the currently executing scope.
        """
        path = os.path.abspath(path)
        self._create_directory(path)
        if is_falsy(persist):
            self._screenshot_path_stack.append(self.screenshot_root_directory)
            # Restore after current scope ends
            events.on('scope_end', 'current',
                      self._restore_screenshot_directory)
        self.screenshot_root_directory = path

    @keyword
    def capture_page_screenshot(self,
                                filename='selenium-screenshot-{index}.png'):
        """Takes a screenshot of the current page and embeds it into the log.

        ``filename`` argument specifies the name of the file to write the
        screenshot into. If no ``filename`` is given, the screenshot is saved
        into file _selenium-screenshot-{index}.png_ under the directory where
        the Robot Framework log file is written into. The ``filename`` is
        also considered relative to the same directory, if it is not
        given in absolute format. If an absolute or relative path is given
        but the path does not exist it will be created.

        Starting from Selenium2Library 1.8 if ``filename`` contains _{index}_
        characters, it will be automatically replaced with running index.
        The running index is unique for each different filename. The absolute
        path of the saved screenshot is always returned and it does not depend
        does the ``filename`` contain _{index}_. See example 1 and 2 for more
        details.

        The _{index}_ is replaced with the actual index by using Python's
        [https://docs.python.org/2/library/stdtypes.html#str.format|
        str.format] method, and it can be formatted using the standard
        [https://docs.python.org/2/library/string.html#format-string-syntax|
        format string syntax]. The example 3 shows this by setting the width and
        the fill character.

        If there is a need to write literal _{index}_ or if ``filename``
        contains _{_ or _}_ characters, then the braces must be doubled.

        If _{index}_ is used, the computed filename will not overwrite
        an existing file. The number chosen will be the first number
        that results in a unique filename. For example, if the
        computed name is screenshot-1.png but screenshot-1.png already
        exists, screenshot-2.png will be tried, and so on, until a
        unique name is found.

        Example 1:
        | ${file1} = | Capture Page Screenshot |
        | File Should Exist | ${OUTPUTDIR}${/}selenium-screenshot-1.png |
        | Should Be Equal | ${file1} | ${OUTPUTDIR}${/}selenium-screenshot-1.png |
        | ${file2} = | Capture Page Screenshot |
        | File Should Exist | ${OUTPUTDIR}${/}selenium-screenshot-2.png |
        | Should Be Equal | ${file2} | ${OUTPUTDIR}${/}selenium-screenshot-2.png |

        Example 2:
        | ${file1} = | Capture Page Screenshot | ${OTHER_DIR}${/}other-{index}-name.png |
        | ${file2} = | Capture Page Screenshot | ${OTHER_DIR}${/}some-other-name-{index}.png |
        | ${file3} = | Capture Page Screenshot | ${OTHER_DIR}${/}other-{index}-name.png |
        | File Should Exist | ${OTHER_DIR}${/}other-1-name.png |
        | Should Be Equal | ${file1} | ${OTHER_DIR}${/}other-1-name.png |
        | File Should Exist | ${OTHER_DIR}${/}some-other-name-1.png |
        | Should Be Equal | ${file2} | ${OTHER_DIR}${/}some-other-name-1.png |
        | File Should Exist | ${OTHER_DIR}${/}other-2-name.png |
        | Should Be Equal | ${file3} | ${OTHER_DIR}${/}other-2-name.png |

        Example 3:
        | Capture Page Screenshot | ${OTHER_DIR}${/}sc-{index:06}.png |
        | File Should Exist | ${OTHER_DIR}${/}sc-000001.png |

        """
        path, link = self._get_screenshot_paths(filename)
        self._create_directory(path)
        if hasattr(self.browser, 'get_screenshot_as_file'):
            if not self.browser.get_screenshot_as_file(path):
                raise RuntimeError('Failed to save screenshot ' + link)
        else:
            if not self.browser.save_screenshot(path):
                raise RuntimeError('Failed to save screenshot ' + link)
        # Image is shown on its own row and thus prev row is closed on purpose
        msg = (
            '</td></tr><tr><td colspan="3"><a href="{}">'
            '<img src="{}" width="800px"></a>'.format(link, link)
        )
        self.info(msg, html=True)
        return path

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

    def _get_screenshot_paths(self, filename_template):
        screenshotdir = self._get_screenshot_directory()

        filename = filename_template.format(
            index=self._get_screenshot_index(filename_template))

        # try to match {index} but not {{index}} (plus handle
        # other variants like {index!r})
        if re.search(r'(?<!{){index(![rs])?(:.*?)?}(?!})', filename_template):
            # make sure the computed filename doesn't exist. We only
            # do this if the template had the {index} formatting
            # sequence (or one of it's variations)
            while os.path.exists(os.path.join(screenshotdir, filename)):
                filename = filename_template.format(
                    index=self._get_screenshot_index(filename_template))

        filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(screenshotdir, filename)
        link = get_link_path(path, logdir)
        return path, link

    def _get_screenshot_index(self, filename):
        if filename not in self._screenshot_index:
            self._screenshot_index[filename] = 0
        self._screenshot_index[filename] += 1
        return self._screenshot_index[filename]

    def _get_log_dir(self):
        try:
            logfile = BuiltIn().get_variable_value('${LOG FILE}')
        except RobotNotRunningError:
            logfile = os.getcwd()
        if logfile != 'NONE':
            logdir = os.path.dirname(logfile)
        else:
            logdir = BuiltIn().get_variable_value('${OUTPUTDIR}')
        return logdir
