from SeleniumLibrary.base import LibraryComponent, keyword


class RunningKeyword(LibraryComponent):

    @keyword
    def get_running_keyword(self):
        return self.ctx._running_keyword

    @keyword(name='Get Running Keyword By Decorator')
    def get_running_keyword_2(self):
        return self.get_running_keyword()
