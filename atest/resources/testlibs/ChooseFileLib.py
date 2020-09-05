from robot.libraries.BuiltIn import BuiltIn


def my_choose_file(locator, path):
    sl = BuiltIn().get_library_instance("SeleniumLibrary")
    sl.choose_file(locator, path)
