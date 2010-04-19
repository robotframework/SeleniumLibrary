import re
import os.path
import sys
import unittest


def run_unit_tests():
    testfile = re.compile("^test_.*\.py$", re.IGNORECASE)
    basedir = os.path.abspath(os.path.dirname(__file__))
    testdir = os.path.join(basedir, 'unit')

    for path in [testdir, os.path.join(basedir, '..', 'src')]:
        if path not in sys.path:
            sys.path.insert(0, path)

    tests = [ unittest.defaultTestLoader.loadTestsFromModule(load_module(name))
              for name in os.listdir(testdir) if testfile.match(name) ]

    runner = unittest.TextTestRunner()
    result = runner.run(unittest.TestSuite(tests))
    rc = len(result.failures) + len(result.errors)
    if rc > 255: rc = 255
    return rc


def load_module(name):
    return __import__(os.path.splitext(name)[0])


if __name__ == '__main__':
    sys.exit(run_tests())

