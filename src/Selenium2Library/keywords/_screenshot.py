import os, errno
import robot
from keywordgroup import KeywordGroup
from robot.api import logger

class _ScreenshotKeywords(KeywordGroup):

    def __init__(self):
        self._screenshot_index = 0

    # Public

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
        | Screen Capture | filename=${BROWSER} |
        | Screen Capture | filename=${BROWSER} |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}.png |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}-1.png |
        | Screen Capture |
        | Screen Capture |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-2.png |
        | File Should Exist  | ${OUTPUTDIR}${/}selenium-screenshot-3.png |
        | Screen Capture | filename=${BROWSER}.png | overwrite=${True} |
        | Screen Capture | filename=${BROWSER}.png | overwrite=${True} |
        | File Should Exist  | ${OUTPUTDIR}${/}${BROWSER}.png |
        | File Should Not Exist | ${OUTPUTDIR}${/}overwrite-${BROWSER}-4.png |
        """
        path, link = self._get_screenshot_paths(filename, overwrite=overwrite)
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

    def _get_screenshot_paths(self, filename, overwrite=False):
        if not filename:
            self._screenshot_index += 1
            filename = 'selenium-screenshot-%d.png' % self._screenshot_index
        elif filename and not overwrite:
            filename = self._screenshot_existence(filename.replace('/',
                                                                   os.sep))
        else:
            filename = filename.replace('/', os.sep)
        path, logdir = self._get_logdir_path(filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _screenshot_existence(self, filename):
        if os.path.exists(self._get_logdir_path(filename)[0]):
            self._screenshot_index += 1
            try:
                return '-%s.png'.join(filename.rsplit('.png', 1)) \
                    % self._screenshot_index
            except TypeError:
                return filename + '-%s' % self._screenshot_index
        else:
            return filename

    def _get_logdir_path(self, filename):
        logdir = self._get_log_dir()
        return os.path.join(logdir, filename), logdir
