#!/usr/bin/env python

import os
import shutil
import sys
from os.path import abspath, dirname, join

from pytest import main as py_main


CURDIR = dirname(abspath(__file__))
SRC = join(CURDIR, os.pardir, 'src')


def remove_output_dir():
    output_dir = os.path.join(CURDIR, 'output_dir')
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)


def run_unit_tests():
    sys.path.insert(0, SRC)
    try:
        result = py_main(['--rootdir=%s' % CURDIR, '-p', 'no:cacheprovider', CURDIR])
    finally:
        sys.path.pop(0)
    return result


if __name__ == '__main__':
    remove_output_dir()
    sys.exit(run_unit_tests())
