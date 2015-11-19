import robot
import os, errno
from PIL import Image

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

        ``path`` argument specifies the absolute path where the screenshots
        should be written to. If the specified ``path`` does not exist,
        it will be created. Setting ``persist`` specifies that the given
        ``path`` should be used for the rest of the test execution, otherwise
        the path will be restored at the end of the currently executing scope.
        """
        path = os.path.abspath(path)
        self._create_directory(path)
        if persist is False:
            self._screenshot_path_stack.append(self.screenshot_root_directory)
            # Restore after current scope ends
            utils.events.on('scope_end', 'current',
                            self._restore_screenshot_directory)

        self.screenshot_root_directory = path

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
        if hasattr(self._current_browser(), 'get_screenshot_as_file'):
            if not self._current_browser().get_screenshot_as_file(path):
                raise RuntimeError('Failed to save screenshot ' + link)
        else:
            if not self._current_browser().save_screenshot(path):
                raise RuntimeError('Failed to save screenshot ' + link)
        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))
        return path

    def capture_element_screenshot(self, locator, file_name='element-screenshot-{index}.png'):
        width, height =  self.get_element_size (locator)
        y_coord = self.get_vertical_position(locator)
        x_coord = self.get_horizontal_position(locator)

        bounding_box = (
            x_coord, # left
            y_coord, # upper
            (x_coord + width), # right
            (y_coord  + height) # bottom
        )
        screenshotdir = self._get_screenshot_directory()
        file_name = os.path.join(screenshotdir, file_name)
        self.capture_page_screenshot(file_name)
        base_image = Image.open(file_name)
        cropped_image = base_image.crop(bounding_box)
        base_image = base_image.resize(cropped_image.size)
        base_image.paste(cropped_image, (0, 0))
        base_image.save(file_name)


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
        filename = filename.format(
            index=self._get_screenshot_index(filename))
        filename = filename.replace('/', os.sep)
        screenshotdir = self._get_screenshot_directory()
        logdir = self._get_log_dir()
        path = os.path.join(screenshotdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _get_screenshot_index(self, filename):
        if filename not in self._screenshot_index:
            self._screenshot_index[filename] = 0
        self._screenshot_index[filename] += 1
        return self._screenshot_index[filename]
