from collections import OrderedDict

from SeleniumLibrary.base import LibraryComponent, keyword


class PluginWithKwArgs(LibraryComponent):
    def __init__(self, ctx, **kwargs):
        LibraryComponent.__init__(self, ctx)
        self.kwargs = kwargs

    @keyword
    def return_kw_args_as_string(self):
        kwargs = OrderedDict(sorted(self.kwargs.items()))
        joined_str = "start:"
        for key in kwargs:
            joined_str = "{} {}={},".format(joined_str, key, kwargs[key])
        return joined_str[:-1]
