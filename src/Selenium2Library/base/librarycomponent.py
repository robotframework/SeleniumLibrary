from robot.api import logger

from .context import ContextAware


LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']


class LibraryComponent(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)

    @property
    def element_finder(self):
        return self.ctx.element_finder

    def info(self, msg, html=False):
        logger.info(msg, html)

    def debug(self, msg, html=False):
        logger.debug(msg, html)

    def log(self, msg, level='INFO', html=False):
        if level.upper() in LOG_LEVELS:
            logger.write(msg, level, html)

    def warn(self, msg, html=False):
        logger.warn(msg, html)

    def find_element(self, locator, tag=None, first_only=True, required=True):
        return self.element_finder.find(locator, tag, first_only, required)

    def assert_page_contains(self, locator, tag=None, message=None,
                             loglevel='INFO'):
        self.element_finder.assert_page_contains(locator, tag, message,
                                                 loglevel)

    def assert_page_not_contains(self, locator, tag=None, message=None,
                                 loglevel='INFO'):
        self.element_finder.assert_page_not_contains(locator, tag, message,
                                                     loglevel)
