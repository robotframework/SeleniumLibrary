import re
import os.path
import sys
import unittest

def run_unit_tests(modules_to_run=[]):
    basedir = os.path.abspath(os.path.dirname(__file__))
    testdir = os.path.join(basedir, 'unit')
    path_dirs = [
        testdir,
        os.path.join(basedir, 'lib'),
        os.path.join(basedir, '..', 'src')
    ]

    for path in path_dirs:
        if path not in sys.path:
            sys.path.insert(0, path)

    test_module_names = [test_module_name for test_module_name in load_test_module_names(testdir) 
        if not modules_to_run or test_module_name in modules_to_run]
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

def load_test_module_names(testdir):
    test_modules = []
    load_test_module_names_recursive(testdir, '', test_modules)
    return test_modules

def load_test_module_names_recursive(testdir, relative_dir, test_modules):
    dir_path = os.path.join(testdir, relative_dir)
    for name in os.listdir(dir_path):
        relative_path = os.path.join(relative_dir, name)
        path = os.path.join(testdir, relative_path)
        if os.path.isfile(path):
            if re.match("^test_.*\.py$", name, re.IGNORECASE):
                module_name = os.path.splitext(relative_path)[0].replace(os.sep, '.')
                test_modules.append(module_name)
        else:
            load_test_module_names_recursive(testdir, relative_path, test_modules)

if __name__ == '__main__':
    sys.exit(run_unit_tests(sys.argv[1:]))

