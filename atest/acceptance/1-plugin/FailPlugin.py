from SeleniumLibrary.base import LibraryComponent, keyword


class FailPlugin(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        raise ValueError("Error in import")

    @keyword
    def keyword(self):
        pass
