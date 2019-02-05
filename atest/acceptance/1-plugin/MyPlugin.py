from SeleniumLibrary.base import LibraryComponent, keyword


class MyPlugin(LibraryComponent):

    @keyword
    def new_keyword(self):
        """Adding new keyword."""
        self.info('New Keyword')
        return 'New Keyword'

    @keyword()
    def open_browser(self, location):
        """Overwrite existing keyword."""
        self.info(location)
        return location
