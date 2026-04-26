from SeleniumLibrary.base import keyword


class MyLibNotInherit:
    def __init__(self, ctx):
        self.ctx = ctx

    @keyword
    def bar(self, arg):
        self.info(arg)

my_lib_not_inherit = MyLibNotInherit
