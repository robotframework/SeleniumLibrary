from SeleniumLibrary.base import LibraryComponent, keyword


class plugin_with_event_firing_webdriver(LibraryComponent):

    """This is example for plugin_with_event_firing_webdriver plugin documentation.

    It may contains many chapters and there might be many words
    in the documentation. This is really boring example but let
    see how it looks like in the SeleniumLibrary docs.

    There might be reference to keywords, like `Open Browser`

    == plugin_with_event_firing_webdriver Heading 2 part 1 ==

    This is chapter in heading 2.

    == plugin_with_event_firing_webdriver Heading 2 part 2==

    This is another chapter in heading 2
    """

    def __init__(self, ctx):
        """This init documentation.

        Which also might have multiple chapters. This is
        also a boring example.
        """
        LibraryComponent.__init__(self, ctx)
        self.event_firing_webdriver = "event_firing_webdriver"

    @keyword
    def tidii(self):
        self.info("foo")
