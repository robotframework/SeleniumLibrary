import importlib
import os
import unittest

from SeleniumLibrary import SeleniumLibrary


class ExtendingSeleniumLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sl = SeleniumLibrary()
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cls.my_lib = os.path.join(root_dir, 'my_lib.py')

    def test_no_libraries(self):
        for item in [None, 'None', '']:
            libraries = self.sl._string_to_modules(item)
            self.assertEqual(libraries, [])

    def test_parse_library(self):
        lib = 'path.to.MyLibrary'
        libraries = self.sl._string_to_modules(lib)
        self.assertEqual(libraries, [lib])

    def test_parse_libraries(self):
        lib = 'path.to.MyLibrary,path.to.OtherLibrary'
        libraries = self.sl._string_to_modules(lib)
        self.assertEqual(libraries, lib.split(','))

    def test_import_library(self):
        library = self.sl._import_modules([self.my_lib, self.my_lib])
        self.assertEqual(len(library), 2)
        self.assertEqual('%s.%s' % (library[0].__module__, library[0].__name__),
                         'my_lib.my_lib')
