from SeleniumLibrary.base import LibraryComponent, keyword


class MyLib(LibraryComponent):
    @keyword
    def tidii(self, arg):
        self.info(arg)
