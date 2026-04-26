from SeleniumLibrary.base import LibraryComponent, keyword


class MyLib(LibraryComponent):
    """Some dummy documentation.

    = MyLib Heading 1 =

    This is heading 1 documentation.

    == MyLib Heading 2 ==

     This is heading 2 documentation.
    """

    @keyword
    def foo(self):
        self.info("foo")

    @keyword
    def bar(self, arg):
        self.info(arg)

my_lib = MyLib
