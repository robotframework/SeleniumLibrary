#!/usr/bin/env python
"""Script to run SeleniumLibrary acceptance tests.

Tests are executed using Robot Framework and results verified automatically
afterwards using `robotstatuschecker` tool. The tool can be installed using
`pip install robotstatuschecker` and more information about it can be found
from: https://github.com/robotframework/statuschecker/. Notice that initially
some tests may fail.

It is possible to run test with Selenium Grid. the Grid requires that Java
is available in the PATH and Grid is downloaded in the root of the repository.
The Grid jar file name should start with "selenium-server-standalone" and
this script will automatically start the Grid with hub and node roles.
More details about the Selenium grid can be found from:
https://github.com/SeleniumHQ/selenium/wiki/Grid2

It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run_tests.py` command. It is
recommended to use arguments to select required suite or test for the
execution when developing new functionality for the library. Example like
--test, --suite, --include and --exclude.

Examples:

    run.py chrome
    run.py headlesschrome
    run.py --interpreter jython firefox --suite javascript
    run.py headlesschrome --nounit --grid true
"""

from __future__ import print_function

import time
from contextlib import contextmanager
import os
import sys
import argparse
import textwrap
import shutil
import subprocess
import tempfile

from robot import rebot_cli
from robot.utils import is_truthy

try:
    import robotstatuschecker
except ImportError:
    sys.exit('Required `robotstatuschecker` not installed.\n'
             'Install it with `pip install robotstatuschecker`.')
import requests


# Folder settings
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, 'acceptance')
UNIT_TEST_RUNNER = os.path.join(ROOT_DIR, os.pardir, 'utest', 'run.py')
RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')
SRC_DIR = os.path.normpath(os.path.join(ROOT_DIR, os.pardir, 'src'))
TEST_LIBS_DIR = os.path.join(RESOURCES_DIR, 'testlibs')
HTTP_SERVER_FILE = os.path.join(RESOURCES_DIR, 'testserver', 'testserver.py')

ROBOT_OPTIONS = [
    '--doc', 'SeleniumLibrary acceptance tests with {browser}',
    '--outputdir', RESULTS_DIR,
    '--variable', 'BROWSER:{browser}',
    '--report', 'NONE',
    '--log', 'NONE',
    '--loglevel', 'DEBUG',
    '--pythonpath', SRC_DIR,
    '--pythonpath', TEST_LIBS_DIR
]
REBOT_OPTIONS = [
    '--outputdir', RESULTS_DIR,
    '--noncritical', 'known issue {browser}',
]


def unit_tests():
    print('Running unit tests')
    failures = run_unit_tests()
    if failures:
        print('\nUnit tests failed! Not running acceptance tests.')
        sys.exit(failures)


def acceptance_tests(interpreter, browser, rf_options=None, grid=None):
    if os.path.exists(RESULTS_DIR):
        shutil.rmtree(RESULTS_DIR)
    os.mkdir(RESULTS_DIR)
    if grid:
        hub, node = start_grid()
    with http_server():
        execute_tests(interpreter, browser, rf_options, grid)
    failures = process_output(browser)
    if failures:
        print('\n{} critical test{} failed.'
              .format(failures, 's' if failures != 1 else ''))
    else:
        print('\nAll critical tests passed.')
    if grid:
        hub.kill()
        node.kill()
    sys.exit(failures)


def start_grid():
    node_file = tempfile.TemporaryFile()
    hub_file = tempfile.TemporaryFile()
    selenium_jar = None
    for file in os.listdir():
        if file.startswith('selenium-server-standalone'):
            selenium_jar = file
            break
    if not selenium_jar:
        raise ValueError('Selenium server jar not found: %s' % selenium_jar)
    hub = subprocess.Popen(['java', '-jar', selenium_jar, '-role', 'hub', '-host', 'localhost'],
                           stderr=subprocess.STDOUT, stdout=hub_file)
    time.sleep(1)  # It takes about seconds to start the hub.
    ready = _grid_status(False, 'hub')
    if not ready:
        hub.kill()
        raise ValueError('Selenium grid hub was not ready in 60 seconds.')
    node = subprocess.Popen(['java', '-jar', selenium_jar, '-role', 'node'],
                            stderr=subprocess.STDOUT, stdout=node_file)
    ready = _grid_status(True, 'node')
    if not ready:
        hub.kill()
        node.kill()
        raise ValueError('Selenium grid node was not ready in 60 seconds.')
    return hub, node


def _grid_status(status=False, role='hub'):
    count = 0
    while True:
        try:
            response = requests.get('http://localhost:4444/wd/hub/status')
            data = response.json()
            if data['value']['ready'] == status:
                print('Selenium grid %s ready/started.' % role)
                return True
        except Exception:
            pass
        count += 1
        if count == 12:
            raise ValueError('Selenium grid %s not ready/started in 60 seconds.' % role)
        print('Selenium grid %s not ready/started.' % role)
        time.sleep(5)


@contextmanager
def http_server():
    serverlog = open(os.path.join(RESULTS_DIR, 'serverlog.txt'), 'w')
    process = subprocess.Popen(['python', HTTP_SERVER_FILE, 'start'],
                               stdout=serverlog, stderr=subprocess.STDOUT)
    try:
        yield
    finally:
        subprocess.call(['python', HTTP_SERVER_FILE, 'stop'])
        process.wait()
        serverlog.close()


def execute_tests(interpreter, browser, rf_options, grid):
    options = []
    runner = interpreter.split() + ['-m', 'robot.run']
    options.extend([opt.format(browser=browser) for opt in ROBOT_OPTIONS])
    if rf_options:
        options += rf_options
    command = runner
    if grid:
        command += ['--variable', 'REMOTE_URL:http://localhost:4444/wd/hub',
                    '--exclude', 'NoGrid']
    command += options + [ACCEPTANCE_TEST_DIR]
    log_start(command)
    syslog = os.path.join(RESULTS_DIR, 'syslog.txt')
    subprocess.call(command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def log_start(command_list, *hiddens):
    command = subprocess.list2cmdline(command_list)
    for hidden in hiddens:
        if hidden:
            command = command.replace(hidden, '*' * len(hidden))
    print()
    print('Starting test execution with command:')
    print(command)


def process_output(browser):
    print('Verifying results...')
    options = []
    output = os.path.join(RESULTS_DIR, 'output.xml')
    robotstatuschecker.process_output(output, verbose=False)
    options.extend([opt.format(browser=browser) for opt in REBOT_OPTIONS])
    try:
        rebot_cli(options + [output])
    except SystemExit as exit:
        return exit.code


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='\n'.join(__doc__.splitlines()[2:])
    )
    parser.add_argument('--interpreter', '-I',
                        default='python',
                        help=textwrap.dedent("""\
                            Any Python interpreter supported by the library.
                            E.g. `python`, `jython` or `c:\\Python27\\python.exe`.
                            By default set to `python`."""))
    parser.add_argument('browser',
                        help=('Any browser supported by the library '
                              '(e.g. `chrome`or `firefox`).'))
    parser.add_argument('--nounit', help='Does not run unit test when set.',
                        default=False, action='store_true')
    parser.add_argument('--grid', '-G', help='Run test by using Selenium grid',
                        default=False)
    args, rf_options = parser.parse_known_args()
    browser = args.browser.lower().strip()
    selenium_grid = is_truthy(args.grid)
    interpreter = args.interpreter
    if args.nounit:
        print('Not running unit tests.')
    else:
        rc = subprocess.call([interpreter, UNIT_TEST_RUNNER])
        if rc != 0:
            print('Not running acceptance test, because unit tests failed.')
            sys.exit(rc)
    acceptance_tests(interpreter, browser, rf_options, selenium_grid)
