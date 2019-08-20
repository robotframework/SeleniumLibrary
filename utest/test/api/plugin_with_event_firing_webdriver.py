from SeleniumLibrary.base import LibraryComponent, keyword


class plugin_with_event_firing_webdriver(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.event_firing_webdriver = 'event_firing_webdriver'

    @keyword
    def tidii(self):
        self.info('foo')
