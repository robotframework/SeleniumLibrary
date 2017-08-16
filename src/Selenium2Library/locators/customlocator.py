from robot.libraries.BuiltIn import BuiltIn

from Selenium2Library.base import ContextAware


try:
    basestring
except NameError:
    basestring = str


class CustomLocator(ContextAware):

    def __init__(self, ctx, name, finder):
        ContextAware.__init__(self, ctx)
        self.name = name
        self.finder = finder

    def find(self, criteria, tag, constraints):
        # Allow custom locators to be keywords or normal methods
        if isinstance(self.finder, basestring):
            element = BuiltIn().run_keyword(self.finder, self.browser,
                                            criteria, tag, constraints)
        elif hasattr(self.finder, '__call__'):
            element = self.finder(self.browser, criteria, tag, constraints)
        else:
            raise AttributeError('Invalid type provided for Custom Locator %s'
                                 % self.name)

        # Always return an array
        if hasattr(element, '__len__') and not isinstance(element, basestring):
            return element
        else:
            return [element]
