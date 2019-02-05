from collections import namedtuple
import os
import unittest

from robot.errors import DataError

from SeleniumLibrary import SeleniumLibrary


class ExtendingSeleniumLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sl = SeleniumLibrary()
        cls.root_dir = os.path.dirname(os.path.abspath(__file__))
        Lib = namedtuple('Lib', 'lib, args')
        lib = Lib(lib=os.path.join(cls.root_dir, 'my_lib.py'), args=[])
        cls.my_lib = lib

    def test_no_libraries(self):
        for item in [None, 'None', '']:
            libraries = self.sl._string_to_modules(item)
            self.assertEqual(libraries, [])

    def test_parse_library(self):
        lib = 'path.to.MyLibrary'
        libraries = self.sl._string_to_modules(lib)
        self.assertEqual(len(libraries), 1)
        self.assertEqual(libraries[0].lib, lib)
        self.assertEqual(libraries[0].args, [])

    def test_parse_libraries(self):
        lib = 'path.to.MyLibrary,path.to.OtherLibrary'
        libraries = self.sl._string_to_modules(lib)
        self.assertEqual(len(libraries), 2)
        self.assertEqual(libraries[0].lib, lib.split(',')[0])
        self.assertEqual(libraries[0].args, [])
        self.assertEqual(libraries[1].lib, lib.split(',')[1])
        self.assertEqual(libraries[1].args, [])

    def test_parse_library_with_args(self):
        lib = 'path.to.MyLibrary'
        lib_args = 'arg1;arg2'
        libraries = self.sl._string_to_modules('%s;%s' % (lib, lib_args))
        library = libraries[0]
        self.assertEqual(len(libraries), 1)
        self.assertEqual(library.lib, lib)
        self.assertEqual(library.args, [arg for arg in lib_args.split(';')])

    def test_parse_plugin_with_kw_args(self):
        lib = 'PluginWithKwArgs.py'
        lib_args = 'kw1=Text1;kw2=Text2'
        libraries = self.sl._string_to_modules('%s;%s' % (lib, lib_args))
        library = libraries[0]
        self.assertEqual(len(libraries), 1)
        self.assertEqual(library.lib, lib)
        self.assertEqual(library.args, [])
        self.assertEqual(library.kw_args, {'kw1': 'Text1', 'kw2': 'Text2'})

    def test_import_library(self):
        library = self.sl._import_modules([self.my_lib, self.my_lib])
        self.assertEqual(len(library), 2)
        self.assertEqual('%s.%s' % (library[0].__module__, library[0].__name__),
                         'my_lib.my_lib')

    def test_plugin_does_not_exist(self):
        not_here = os.path.join(self.root_dir, 'not_here.py')
        with self.assertRaises(DataError):
            SeleniumLibrary(plugins=not_here)

        with self.assertRaises(DataError):
            SeleniumLibrary(plugins='SeleniumLibrary.NotHere')

    def test_parse_plugin_with_kw_args(self):

        kw_args_lib = os.path.join(self.root_dir, '..', '..', '..',
                                   'atest', 'acceptance', '1-plugin',
                                   'PluginWithKwArgs.py;kw1=Text1;kw2=Text2')
        SeleniumLibrary(plugins=kw_args_lib)
