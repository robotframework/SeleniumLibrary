from SeleniumLibrary.base import LibraryComponent, keyword


class my_lib(LibraryComponent):  # noqa: N801 - prefer RF syntax for test libraries
    @keyword
    def tidii(self, arg):
        self.info(arg)
