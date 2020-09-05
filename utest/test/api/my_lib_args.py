from SeleniumLibrary.base import LibraryComponent, keyword


class my_lib_args(LibraryComponent):
    def __init__(self, ctx, arg1, arg2, *args, **kwargs):
        LibraryComponent.__init__(self, ctx)
        self.arg1 = arg1
        self.arg2 = arg2
        self.args = args
        self.kwargs = kwargs

    @keyword(tags=["MyTag"])
    def foo_1(self):
        self.info("foo")

    @keyword
    def bar_2(self, arg):
        self.info(arg)

    @keyword
    def add_cookie(self, foo, bar):
        self.info(foo)
        self.info(bar)
