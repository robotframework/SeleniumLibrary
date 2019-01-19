from SeleniumLibrary.base import LibraryComponent, keyword


class my_lib(LibraryComponent):

    @keyword
    def foo(self):
        self.info('foo')
