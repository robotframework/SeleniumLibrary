from robot.libraries.BuiltIn import BuiltIn


try:
    basestring
except NameError:
    basestring = str


class CustomLocator(object):

    def __init__(self, name, finder):
        self.name = name
        self.finder = finder

    def find(self, *args):
        # Allow custom locators to be keywords or normal methods
        if isinstance(self.finder, basestring):
            element = BuiltIn().run_keyword(self.finder, *args)
        elif hasattr(self.finder, '__call__'):
            element = self.finder(*args)
        else:
            raise AttributeError('Invalid type provided for Custom Locator %s' % self.name)

        # Always return an array
        if hasattr(element, '__len__') and (not isinstance(element, basestring)):
            return element
        else:
            return [element]
