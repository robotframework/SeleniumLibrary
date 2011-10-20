import env
import os, sys
import unittest
from Selenium2Library import utils

def run_unit_tests(modules_to_run=[]):
    (test_module_names, test_modules) = utils.import_modules_under(
        env.UNIT_TEST_DIR, include_root_package_name = False, pattern="test*.py")

    bad_modules_to_run = [module_to_run for module_to_run in modules_to_run
        if module_to_run not in test_module_names]
    if bad_modules_to_run:
        print "Specified test module%s not exist: %s" % (
            ' does' if len(bad_modules_to_run) == 1 else 's do',
            ', '.join(bad_modules_to_run))
        return -1

    tests = [unittest.defaultTestLoader.loadTestsFromModule(test_module) 
        for test_module in test_modules]

    runner = unittest.TextTestRunner()
    result = runner.run(unittest.TestSuite(tests))
    rc = len(result.failures) + len(result.errors)
    if rc > 255: rc = 255
    return rc

if __name__ == '__main__':
    sys.exit(run_unit_tests(sys.argv[1:]))

