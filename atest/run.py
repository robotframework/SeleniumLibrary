#!/usr/bin/env python
"""Script to run SeleniumLibrary acceptance tests.

Tests are executed using Robot Framework and results verified automatically
afterwards using `robotstatuschecker` tool. The tool can be installed using
`pip install robotstatuschecker` and more information about it can be found
from: https://github.com/robotframework/statuschecker/. Notice that initially
some tests may fail.

When running test by using browser from Sauce labs, it is required that the
Sauce Connect is used. The Sauce Connect allows the browser from Sauce Labs
reach the acceptance test web server. The acceptance test uses tunnel with
name `localtunnel` and therefore when establishing the Sauce Connect tunnel
use the following command:
    `bin/sc -u YOUR_USERNAME -k YOUR_ACCESS_KEY -i localtunnel`

More details and to downlaod Sauce Connect visit:
https://wiki.saucelabs.com/display/DOCS/High+Availability+Sauce+Connect+Setup

It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run_tests.py` command. It is
recommended to use arguments to select required suite or test for the
execution when developing new functionality for the library. Example like
--test, --suite, --include and --exclude.

Examples:

    run.py chrome
    run.py headlesschrome
    run.py --interpreter jython firefox --suite javascript
    run.py chrome --sauceusername your_username --saucekey account_key --suite javascript

"""

from __future__ import print_function

from contextlib import contextmanager
import os
import sys
import argparse
import textwrap
import shutil
import subprocess

from robot import rebot_cli
try:
    import robotstatuschecker
except ImportError:
    sys.exit('Required `robotstatuschecker` not installed.\n'
             'Install it with `pip install robotstatuschecker`.')


# Folder settings
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, "acceptance")
UNIT_TEST_RUNNER = os.path.join(ROOT_DIR, '..', 'utest', 'run.py')
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
SRC_DIR = os.path.normpath(os.path.join(ROOT_DIR, "..", "src"))
TEST_LIBS_DIR = os.path.join(RESOURCES_DIR, "testlibs")
HTTP_SERVER_FILE = os.path.join(RESOURCES_DIR, "testserver", "testserver.py")
# Travis settings for pull request
TRAVIS = os.environ.get("TRAVIS", False)
TRAVIS_EVENT_TYPE = os.environ.get("TRAVIS_EVENT_TYPE", None)
TRAVIS_JOB_NUMBER = os.environ.get("TRAVIS_JOB_NUMBER", "localtunnel")
SAUCE_USERNAME = os.environ.get("SAUCE_USERNAME", None)
SAUCE_ACCESS_KEY = os.environ.get("SAUCE_ACCESS_KEY", None)
TRAVIS_BROWSERS = ['chrome', 'firefox', 'headlesschrome']

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


def acceptance_tests(interpreter, browser, rf_options=[],
                     sauce_username=None, sauce_key=None):
    if os.path.exists(RESULTS_DIR):
        shutil.rmtree(RESULTS_DIR)
    os.mkdir(RESULTS_DIR)
    with http_server():
        execute_tests(interpreter, browser, rf_options,
                      sauce_username, sauce_key)
    failures = process_output(browser)
    if failures:
        print('\n{} critical test{} failed.'
              .format(failures, 's' if failures != 1 else ''))
    else:
        print('\nAll critical tests passed.')
    sys.exit(failures)


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


def execute_tests(interpreter, browser, rf_options, sauce_username, sauce_key):
    options = []
    runner = interpreter.split() + ['-m', 'robot.run']
    options.extend([opt.format(browser=browser) for opt in ROBOT_OPTIONS])
    options += rf_options
    if sauce_username and sauce_key:
        options.extend(get_sauce_conf(browser, sauce_username, sauce_key))
    command = runner
    command += options + [ACCEPTANCE_TEST_DIR]
    log_start(command, sauce_username, sauce_key)
    syslog = os.path.join(RESULTS_DIR, 'syslog.txt')
    subprocess.call(
        command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog)
    )


def log_start(command_list, *hiddens):
    command = subprocess.list2cmdline(command_list)
    for hidden in hiddens:
        if hidden:
            command = command.replace(hidden, '*' * len(hidden))
    print()
    print('Starting test execution with command:')
    print(command)


def get_sauce_conf(browser, sauce_username, sauce_key):
    if browser in TRAVIS_BROWSERS and TRAVIS:
        return []
    return [
        '--variable', 'SAUCE_USERNAME:{}'.format(sauce_username),
        '--variable', 'SAUCE_ACCESS_KEY:{}'.format(sauce_key),
        '--variable',
        'REMOTE_URL:http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
            sauce_username, sauce_key
        ),
        '--variable',
        'DESIRED_CAPABILITIES:build:{0}-{1},tunnel-identifier:{0}'.format(
            TRAVIS_JOB_NUMBER, browser
        )
    ]


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


def sauce_credentials(sauce_username, sauce_key):
    if TRAVIS and not sauce_username and not sauce_key:
        username = SAUCE_USERNAME
        key = SAUCE_ACCESS_KEY
    else:
        username = sauce_username
        key = sauce_key
    return username, key


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
    parser.add_argument('--sauceusername', '-U',
                        help='Username to order browser from SauceLabs.')
    parser.add_argument('--saucekey', '-K',
                        help='Access key to order browser from SauceLabs.')
    parser.add_argument('--nounit', help='Does not run unit test when set.',
                        default=False, action='store_true')
    args, rf_options = parser.parse_known_args()
    browser = args.browser.lower().strip()
    if TRAVIS and browser not in TRAVIS_BROWSERS and TRAVIS_EVENT_TYPE != 'cron':
        # When running in Travis only Chrome and Firefox are available for PR.
        print(
            'Can not run test with browser "{}" from SauceLabs with PR.\n'
            'SauceLabs can be used only when running with cron and from '
            'SeleniumLibrary master branch, but your event type '
            'was "{}". Only Chrome and Firefox are supported with PR and when using '
            'Travis'.format(browser, TRAVIS_EVENT_TYPE)
        )
        sys.exit(0)
    sauce_username, sauce_key = sauce_credentials(
        args.sauceusername, args.saucekey)
    interpreter = args.interpreter
    if args.nounit:
        print('Not running unit tests.')
    else:
        rc = subprocess.call([interpreter, UNIT_TEST_RUNNER])
        if rc != 0:
            print('Not running acceptance test, because unit tests failed.')
            sys.exit(rc)
    acceptance_tests(interpreter, browser, rf_options,
                     sauce_username, sauce_key)
