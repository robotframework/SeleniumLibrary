#!/usr/bin/env python
import argparse
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


def run_unit_tests(reporter, reporter_args):
    sys.path.insert(0, SRC)
    py_args = ['--rootdir=%s' % CURDIR, '-p', 'no:cacheprovider', CURDIR]
    if reporter:
        py_args.insert(0, f'--approvaltests-add-reporter={reporter}')
    if reporter_args:
        py_args.insert(1, f'--approvaltests-add-reporter-args={reporter_args}')
    try:
        result = py_main(py_args)
    except Exception:
        result = 254
    finally:
        sys.path.pop(0)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SeleniumLibrary Unit test runner.')
    parser.add_argument('-R', '--approvaltests-use-reporter', default='PythonNative', dest='reporter')
    parser.add_argument('-A', '--approvaltests-add-reporter-args', default=None, dest='reporter_args')
    args = parser.parse_args()
    remove_output_dir()
    sys.exit(run_unit_tests(args.reporter, args.reporter_args))
