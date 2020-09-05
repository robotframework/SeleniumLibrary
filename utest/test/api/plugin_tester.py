from SeleniumLibrary.base import LibraryComponent, keyword


class plugin_tester(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        ctx.event_firing_webdriver = "should be last"

    @keyword
    def foo(self):
        self.info("foo")

    @keyword
    def bar(self, arg):
        self.info(arg)
