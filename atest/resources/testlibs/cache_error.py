from robot.libraries.BuiltIn import BuiltIn


def invalidate_driver():
    sl = BuiltIn().get_library_instance("SeleniumLibrary")
    sl.register_driver(None, "tidii")
    sl.register_driver(None, "foobar")
