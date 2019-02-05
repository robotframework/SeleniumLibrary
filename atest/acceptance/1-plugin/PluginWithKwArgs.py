from SeleniumLibrary.base import LibraryComponent, keyword


class PluginWithKwArgs(LibraryComponent):

        def __init__(self, ctx, **kwargs):
            LibraryComponent.__init__(self, ctx)
            self.kwargs = kwargs

        @keyword
        def return_kw_args_as_string(self):
            joined_str = 'start:'
            for key in self.kwargs:
                joined_str = '%s %s=%s,' % (joined_str, key, self.kwargs[key])
            return joined_str[:-1]