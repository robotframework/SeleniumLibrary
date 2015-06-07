import os, errno
import robot
from keywordgroup import KeywordGroup
from robot.api import logger

class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0

    # Public

    def capture_page_screenshot(self, filename=None, index=False):
        """Takes a screenshot of the current page and embeds it into the log.

        `filename` argument specifies the name of the file to write the
        screenshot into. If no `filename` is given, the screenshot is saved into file
        `selenium-screenshot-<counter>.png` under the directory where
        the Robot Framework log file is written into. The `filename` is
        also considered relative to the same directory, if it is not
        given in absolute format. If an absolute or relative path is given
        but the path does not exist it will be created.

        `index` with index argument it is possible to define custom filename
        but each time get unique screen capture. Example if pabot is used
        to run multiple test suites in paraler and correct screenshots should
        be copied to log, then it is possible to use `filename` and
        `index` argument to gether to create unique name for each screenshot.

        Example:
        | Open Browser | www.someurl.com | browser=${BROWSER} |
        | Screen Capture | filename=${BROWSER}- | index=True |
        | Screen Capture | filename=${BROWSER}- | index=True |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}-1.png |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}-2.png |
        """
        path, link = self._get_screenshot_paths(filename, index=index)
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir(target_dir):
                    pass
                else: raise

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

    def _get_screenshot_paths(self, filename, index=False):
        if not filename:
            self._screenshot_index += 1
            filename = 'selenium-screenshot-%d.png' % self._screenshot_index
        elif filename and index:
            self._screenshot_index += 1
            filename = filename.replace('/', os.sep) + \
                str(self._screenshot_index) + '.png'
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link
