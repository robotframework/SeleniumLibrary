#!/usr/bin/env python

import os
import shutil
import sys
from os.path import abspath, dirname, join
from unittest import defaultTestLoader, TextTestRunner


CURDIR = dirname(abspath(__file__))


def remove_output_dir():
    output_dir = os.path.join(CURDIR, 'output_dir')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)


def run_unit_tests():
    sys.path.insert(0, join(CURDIR, os.pardir, 'src'))
    try:
        suite = defaultTestLoader.discover(join(CURDIR, 'test'), 'test_*.py')
        result = TextTestRunner().run(suite)
    finally:
        sys.path.pop(0)
    return min(len(result.failures) + len(result.errors), 255)


if __name__ == '__main__':
    remove_output_dir()
    sys.exit(run_unit_tests())
