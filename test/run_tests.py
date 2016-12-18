#!/usr/bin/env python

"""Script to run Selenium2Library acceptance tests.

Tests are executed using Robot Framework and results verified automatically
afterwards using `robotstatuschecker` tool. The tool can be installed using
`pip install robotstatuschecker` and more information about it can be found
from https://github.com/robotframework/statuschecker/. Notice that initially
some tests fail.

Usage:

  run_tests.py browser [options]

Arguments:

  browser:        Any browser supported by the library (e.g. `chrome`or
                  `firefox`)
  --interpreter:  Any Python interpreter supported by the library (e.g.
                  `python`, `jython` or `c:\\Python27\\python.exe`). By
                  default set to `python`.
  --suite:        Selects the test suites by name.
  --scusername:   Username to access Sauce Labs to order browsers when
                  running test from local computer.
  --sckey:        Access key for Sauce Labs account.

When running test by using browser from Sauce labs, it is required that
the Sauce Connect is used. The Sauce Connect allows the browser from Sauce Labs
reach the acceptance test webserver. The acceptance test uses tunnel with
name `localtunnel` and therefore when establishing  the Sauce Connect tunnel
use the following command:
`bin/sc -u YOUR_USERNAME -k YOUR_ACCESS_KEY -i localtunnel`

More details and to downlaod Sauce Connect visit:
https://wiki.saucelabs.com/display/DOCS/High+Availability+Sauce+Connect+Setup

Examples:

  run_tests.py python chrome
  run_tests.py jython firefox --suite list
  run_tests.py python chrome --scusername your_username --sckey account_key
"""

from __future__ import print_function

from contextlib import contextmanager
import os
import sys
import argparse
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


def acceptance_tests(interpreter, browser, suite, sauceusername, saucekey):
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    with http_server():
        execute_tests(interpreter, browser, suite, sauceusername, saucekey)
    failures = process_output(browser, suite)
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


def execute_tests(interpreter, browser, suite, sauceusername, saucekey):
    runner = [interpreter, '-m', 'robot.run']
    options = [opt.format(browser=browser,
                          py_version=interpreter + sys.version[:3])
               for opt in ROBOT_OPTIONS]
    if sauceusername and saucekey:
        options.extend(get_sauce_conf(browser, sauceusername, saucekey))
    command = runner
    if suite:
        command += ['-s', suite]
    command += options + [env.ACCEPTANCE_TEST_DIR]
    log_start(command, sauceusername, saucekey)
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    subprocess.call(
        command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog)
    )


def log_start(command_list, sauceusername, saucekey):
    command = subprocess.list2cmdline(command_list)
    for hidden in [sauceusername, saucekey]:
        if hidden:
            command = command.replace(hidden, '*' * len(hidden))
    print()
    print('Starting test execution with command:')
    print(command)


def get_sauce_conf(browser, sauceusername, saucekey):
    if browser == 'chrome' and env.TRAVIS:
        conf = []
    else:
        conf = [
            '--variable', 'SAUCE_USERNAME:{}'.format(sauceusername),
            '--variable', 'SAUCE_ACCESS_KEY:{}'.format(saucekey),
            '--variable',
            'REMOTE_URL:http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
                sauceusername, saucekey
            ),
            '--variable',
            'DESIRED_CAPABILITIES:build:{0}-{1},tunnel-identifier:{0}'.format(
                env.TRAVIS_JOB_NUMBER, browser
            )
        ]
    return conf


def process_output(browser, suite):
    print('Verifying results...')
    output = os.path.join(env.RESULTS_DIR, 'output.xml')
    robotstatuschecker.process_output(output, verbose=False)
    options = [opt.format(browser=browser) for opt in REBOT_OPTIONS]
    if suite:
        options += ['-s', suite]
    try:
        rebot_cli(options + [output])
    except SystemExit as exit:
        return exit.code


def sauce_credentials(sauceusername, saucekey):
    if env.TRAVIS:
        username = env.SAUCE_USERNAME
        key = env.SAUCE_ACCESS_KEY
    else:
        username = sauceusername
        key = saucekey
    return username, key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Library test runner')
    parser.add_argument(
        '--interpreter',
        default='python',
        help='Interpreter used run the test'
    )
    parser.add_argument('browser', help='Browser used in testing')
    parser.add_argument(
        '--suite',
        '-s',
        help='Selects the test suites by name.'
    )
    parser.add_argument(
        '--scusername',
        help='Username to order browser from SaucuLabs'
    )
    parser.add_argument(
        '--sckey',
        help='Access key to order browser from SaucuLabs'
    )

    args = parser.parse_args()
    browser = args.browser.lower().strip()
    if browser != 'chrome' and env.TRAVIS_EVENT_TYPE != 'cron':
        print(
            'Can not run test with browser "{}" from SauceLabs\n'
            'SauceLabs can be used only when running with corn and from '
            'Selenium2Library master banch, but your event type '
            'was "{}"'.format(browser, env.TRAVIS_EVENT_TYPE)
        )
        sys.exit(0)
    sauceusername, saucekey = sauce_credentials(
        args.scusername, args.sckey)
    unit_tests()
    acceptance_tests(args.interpreter, browser, args.suite,
                     sauceusername, saucekey)
