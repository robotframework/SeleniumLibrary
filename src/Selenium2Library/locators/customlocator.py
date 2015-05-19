from robot.libraries.BuiltIn import BuiltIn

try:
    string_type = basestring
except NameError:
    string_type = str

class CustomLocator(object):

    def __init__(self, name, keyword):
        self.name = name
        self.keyword = keyword

    def find(self, *args):
        element = BuiltIn().run_keyword(self.keyword, *args)
        if hasattr(element, '__len__') and (not isinstance(element, string_type)):
            return element
        else:
            return [element]
