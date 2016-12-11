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

from contextlib import contextmanager
import os
import sys
import subprocess

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
    '--outputdir', env.RESULTS_DIR,
    '--variable', 'BROWSER:{browser}',
    '--variable', 'PY_VERSION:{py_version}',
    '--report', 'NONE',
    '--log', 'NONE',
    '--loglevel', 'DEBUG',
    '--pythonpath', os.pathsep.join([env.SRC_DIR, env.TEST_LIBS_DIR]),
]
REBOT_OPTIONS = [
    '--outputdir', env.RESULTS_DIR,
    '--critical', 'regression',
    '--noncritical', 'inprogress',
    '--noncritical', 'known issue {browser}',
]


def unit_tests():
    print('Running unit tests')
    failures = run_unit_tests()
    if failures:
        print('\nUnit tests failed! Not running acceptance tests.')
        sys.exit(failures)


def acceptance_tests(interpreter, browser, options):
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    with http_server():
        execute_tests(interpreter, browser, options)
    failures = process_output(browser, options)
    if failures:
        print('\n{} critical test{} failed.'
              .format(failures, 's' if failures != 1 else ''))
    else:
        print('\nAll critical tests passed.')
    sys.exit(failures)


@contextmanager
def http_server():
    serverlog = open(os.path.join(env.RESULTS_DIR, 'serverlog.txt'), 'w')
    process = subprocess.Popen(['python', env.HTTP_SERVER_FILE, 'start'],
                               stdout=serverlog, stderr=subprocess.STDOUT)
    try:
        yield
    finally:
        subprocess.call(['python', env.HTTP_SERVER_FILE, 'stop'])
        process.wait()
        serverlog.close()


def execute_tests(interpreter, browser, cli_options):
    runner = [interpreter, '-m', 'robot.run']
    options = [opt.format(browser=browser,
                          py_version=interpreter + sys.version[:3])
               for opt in ROBOT_OPTIONS]
    if env.TRAVIS:
        options.extend(get_travis_conf(browser))
    command = runner + options + cli_options + [env.ACCEPTANCE_TEST_DIR]
    log_start(command)
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    # Running tests as an external process, not using `robot_cli`, to allow
    # using different interpreter that is used for running this script.
    subprocess.call(command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def get_travis_conf(browser):
    conf = [
        '--variable', 'SAUCE_USERNAME:{}'.format(env.SAUCE_USERNAME),
        '--variable', 'SAUCE_ACCESS_KEY:{}'.format(env.SAUCE_ACCESS_KEY)
    ]
    if browser == 'firefox':
        conf.extend([
            '--variable',
            'REMOTE_URL:http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
                env.SAUCE_USERNAME, env.SAUCE_ACCESS_KEY
            )
        ])
    else:
        conf.extend([
            '--variable',
            'DESIRED_CAPABILITIES:build:{0}-{1},tunnel-identifier:{0}'.format(
                env.TRAVIS_JOB_NUMBER, browser
            )
        ])
    return conf


def log_start(command_list):
    command = subprocess.list2cmdline(command_list)
    for hidden in [env.SAUCE_USERNAME, env.SAUCE_ACCESS_KEY]:
        if hidden:
            command = command.replace(hidden, '*' * len(hidden))
    print()
    print('Starting test execution with command:')
    print(command)


def process_output(browser, cli_options):
    print('Verifying results...')
    output = os.path.join(env.RESULTS_DIR, 'output.xml')
    robotstatuschecker.process_output(output, verbose=False)
    options = [opt.format(browser=browser) for opt in REBOT_OPTIONS]
    try:
        rebot_cli(options + cli_options + [output])
    except SystemExit as exit:
        return exit.code


if __name__ == '__main__':
    if len(sys.argv) < 3 or '--help' in sys.argv:
        sys.exit(__doc__)
    unit_tests()
    acceptance_tests(interpreter=sys.argv[1],
                     browser=sys.argv[2].lower(),
                     options=sys.argv[3:])
