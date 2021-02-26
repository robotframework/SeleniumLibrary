from robot.api import logger

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.locators import ElementFinder


class DummyFinder:
    def __init__(self, ctx):
        self.ctx = ctx

    def find(self, *args):
        logger.info('DummyFinder args "%s"' % str(args))
        logger.info("Original finder %s" % self.ctx._original_element_finder)
        return "Dummy find"


class MyPlugin(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        ctx._original_element_finder = ElementFinder(ctx)
        self.element_finder = DummyFinder(ctx)

    @keyword
    def new_keyword(self):
        """Adding new keyword."""
        self.info("New Keyword")
        return "New Keyword"

    @keyword()
    def open_browser(self, location):
        """Overwrite existing keyword."""
        self.info(location)
        return location
