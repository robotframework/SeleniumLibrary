from SeleniumLibrary.base import LibraryComponent, keyword


class PluginWithVarArgs(LibraryComponent):
    def __init__(self, ctx, *args):
        LibraryComponent.__init__(self, ctx)
        self.args = args

    @keyword
    def return_var_args_as_string(self):
        joined_str = "start:"
        for arg in self.args:
            joined_str = f"{joined_str} {arg},"
        return joined_str[:-1]
