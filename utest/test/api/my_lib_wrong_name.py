from SeleniumLibrary.base import LibraryComponent, keyword


class my_lib(LibraryComponent):
    @keyword
    def tidii(self, arg):
        self.info(arg)
