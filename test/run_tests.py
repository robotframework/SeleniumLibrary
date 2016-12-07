#!/usr/bin/env python

"""Script to run Selenium2Library acceptance tests.

Tests are executed using Robot Framework and results verified automatically
afterwards using `robotstatuschecker` tool. The tool can be installed using
`pip install robotstatuschecker` and more information about it can be found
from https://github.com/robotframework/statuschecker/. Notice that initially
some tests fail.

Usage:

  run_tests.py interpreter browser [options]

Arguments:

  interpreter:  Any Python interpreter supported by the library (e.g. `python`,
                `jython`, `c:\\Python27\\python.exe`)
  browser:      Any browser supported by the library (e.g. `chrome`, `firefox`)
  options:      Additional command line options passed to Robot Framework

Examples:

  run_tests.py python chrome
  run_tests.py jython c:\\Python35\\python.exe --test "Click element"
"""

from __future__ import print_function

import os
import sys
from subprocess import call, Popen, STDOUT
from tempfile import TemporaryFile

from robot import rebot_cli
try:
    import robotstatuschecker
except ImportError:
    sys.exit('Required `robotstatuschecker` not installed.\n'
             'Install it with `pip install robotstatuschecker`.')

import env
from run_unit_tests import run_unit_tests


ROBOT_OPTIONS = [
    '--doc', 'Selenium2Library acceptance tests with {browser}',
    '--outputdir', '{outdir}',
    '--variable', 'BROWSER:{browser}',
    '--variable', 'PY_VERSION:{py_version}',
    '--report', 'NONE',
    '--log', 'NONE',
    '--loglevel', 'DEBUG',
    '--pythonpath', '{pythonpath}',
]
REBOT_OPTIONS = [
    '--outputdir', '{outdir}',
    '--critical', 'regression',
    '--noncritical', 'inprogress',
    '--noncritical', 'known_issue_-_*',
]
OPTION_VALUES = {'outdir': env.RESULTS_DIR,
                 'pythonpath': ':'.join((env.SRC_DIR, env.TEST_LIBS_DIR))}


def acceptance_tests(interpreter, browser, options):
    OPTION_VALUES['browser'] = browser.replace('*', '')
    OPTION_VALUES['py_version'] = interpreter + sys.version[:3]
    start_http_server()
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    execute_tests(interpreter, options)
    stop_http_server()
    return process_output(options)


def start_http_server():
    Popen(['python', env.HTTP_SERVER_FILE, 'start'],
          stdout=TemporaryFile(), stderr=STDOUT)


def execute_tests(interpeter, options):
    runner = [interpeter, '-m', 'robot.run']
    options = [opt.format(**OPTION_VALUES) for opt in ROBOT_OPTIONS] + options
    command =  runner + options + [env.ACCEPTANCE_TEST_DIR]
    print()
    print('Starting test execution with command:\n' + ' '.join(command))
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    # Running tests as an external process, not using `robot_cli`, to allow
    # using different interpreter that is used for running this script.
    call(command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def stop_http_server():
    call(['python', env.HTTP_SERVER_FILE, 'stop'])


def process_output(options):
    print('Verifying results...')
    output = os.path.join(env.RESULTS_DIR, 'output.xml')
    robotstatuschecker.process_output(output, verbose=False)
    options = [opt.format(**OPTION_VALUES) for opt in REBOT_OPTIONS] + options
    try:
        rebot_cli(options + [output])
    except SystemExit as exit:
        rc = exit.code
    print()
    if rc == 0:
        print('All critical tests passed.')
    else:
        print('%d critical test%s failed.' % (rc, 's' if rc != 1 else ''))
    return rc


def _run_unit_tests():
    print('Running unit tests')
    failures = run_unit_tests()
    if failures != 0:
        print('\n%Unit tests failed! Not running acceptance tests!')
    return failures


if __name__ == '__main__':
    if len(sys.argv) < 3 or '--help' in sys.argv:
        sys.exit(__doc__)
    unit_failures = _run_unit_tests()
    if unit_failures:
        sys.exit(unit_failures)
    interpreter = sys.argv[1]
    browser = sys.argv[2].lower()
    options = sys.argv[3:]
    if browser != 'unit':
        rc = acceptance_tests(interpreter, browser, options)
        sys.exit(rc)
