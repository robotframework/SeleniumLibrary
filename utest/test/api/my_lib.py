from SeleniumLibrary.base import LibraryComponent, keyword


class my_lib(LibraryComponent):
    """Some dummy documentation.

    = Heading 1 =

    This is heading 1 documentation.

    == Heading 2 ==

     This is heading 2 documentation.
    """

    @keyword
    def foo(self):
        self.info('foo')

    @keyword
    def bar(self, arg):
        self.info(arg)
