import env
import re
import os
import sys
import unittest
import glob

def run_unit_tests(modules_to_run=[]):
    test_module_files = [ test_file_path[len(env.UNIT_TEST_DIR)+1:]
        for test_file_path in glob.glob(os.path.join(env.UNIT_TEST_DIR, "*", "test_*.py"))
        if os.path.exists(os.path.join(os.path.dirname(test_file_path), "__init__.py")) ]
    test_module_names = [ os.path.splitext(test_module_file)[0].replace(os.sep, '.')
        for test_module_file in test_module_files ]

    bad_modules_to_run = [module_to_run for module_to_run in modules_to_run
        if module_to_run not in test_module_names]
    if bad_modules_to_run:
        print "Specified test module%s not exist: %s" % (
            ' does' if len(bad_modules_to_run) == 1 else 's do',
            ', '.join(bad_modules_to_run))
        return -1

    test_modules = [__import__(test_module_name, globals(), locals(), ['*'], -1)
        for test_module_name in test_module_names]
    tests = [unittest.defaultTestLoader.loadTestsFromModule(test_module) 
        for test_module in test_modules]

    runner = unittest.TextTestRunner()
    result = runner.run(unittest.TestSuite(tests))
    rc = len(result.failures) + len(result.errors)
    if rc > 255: rc = 255
    return rc

if __name__ == '__main__':
    sys.exit(run_unit_tests(sys.argv[1:]))

