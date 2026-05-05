from SeleniumLibrary.base import keyword


class my_lib_not_inherit:  # noqa: N801 - prefer RF syntax for test libraries
    def __init__(self, ctx):
        self.ctx = ctx

    @keyword
    def bar(self, arg):
        self.info(arg)
