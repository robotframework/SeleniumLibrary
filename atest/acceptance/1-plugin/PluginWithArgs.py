from SeleniumLibrary.base import LibraryComponent, keyword


class PluginWithArgs(LibraryComponent):
    def __init__(self, ctx, arg1, arg2):
        LibraryComponent.__init__(self, ctx)
        self.arg1 = arg1
        self.arg2 = arg2

    @keyword
    def return_arg1_arg2_as_string(self):
        return f"{self.arg1} {self.arg2}"
