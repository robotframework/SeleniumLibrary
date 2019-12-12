from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary import ElementFinder


def custom_library_locator(parent, criteria, tag, constraints):
    sl = BuiltIn().get_library_instance('SeleniumLibrary')
    el = ElementFinder(sl)
    elements = parent.find_elements_by_xpath('//%s' % criteria)
    return el._filter_elements(elements, tag, constraints)
