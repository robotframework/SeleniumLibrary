from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.by import By

from SeleniumLibrary import ElementFinder


def custom_library_locator(parent, criteria, tag, constraints):
    sl = BuiltIn().get_library_instance("SeleniumLibrary")
    el = ElementFinder(sl)
    elements = parent.find_elements(By.XPATH, "//%s" % criteria)
    return el._filter_elements(elements, tag, constraints)
