from SeleniumLibrary.base import LibraryComponent, keyword


class plugin_with_event_firing_webdriver(LibraryComponent):

    """This is example plugin documentation.

    It may contains many chapters and there might be many words
    in the documentation. This is really boring example but let
    see how it looks like in the SeleniumLibrary docs.

    There might be reference to keywords, like `Open Browser`

    = Heading 1 =

    This is chapter in heading 1.

    == Heading 2 ==

    This is chapter in heading 2
    """

    def __init__(self, ctx):
        """This init documentation.

        Which also might have multiple chapters. This is
        also a boring example.
        """
        LibraryComponent.__init__(self, ctx)
        self.event_firing_webdriver = 'event_firing_webdriver'

    @keyword
    def tidii(self):
        self.info('foo')
