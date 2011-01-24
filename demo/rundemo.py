#! /usr/bin/env python

"""Runner Script for Robot Framework SeleniumLibrary Demo

Tests are run by giving a path to the tests to be executed as an argument to
this script. Possible Robot Framework options are given before the path.

Examples:
  rundemo.py login_tests                        # Run all tests in a directory
  rundemo.py login_tests/valid_login.text       # Run tests in a specific file
  rundemo.py --variable BROWSER:IE login_tests  # Override variable
  rundemo.py -v BROWSER:IE -v DELAY:0.5 login_tests
  rundemo.py --variable SUT:flex login_tests

By default tests are executed with Firefox browser, but this can be changed
by overriding the `BROWSER` variable as illustrated above. Similarly it is
possible to slow down the test execution by overriding the `DELAY` variable
with a non-zero value.

There are HTML and Flex implementations of the demo application and these tests
can be executed against both. The HTML version is used by default, but this can
be changed by overriding `SUT` variable with value `flex`.

When tests are run, the demo application and Selenium Server are started and
stopped automatically. It is possible to start and stop them also separately
by using `demoapp` and `selenium` options. This allows running tests with the
normal `pybot` start-up script, as well as investigating the demo application.

Running the demo requires that Robot Framework, SeleniumLibrary, Python, and
Java to be installed. For more comprehensive instructions, see the demo wiki
page at `http://code.google.com/p/robotframework-seleniumlibrary/wiki/Demo`.
"""

import os
import sys
from tempfile import TemporaryFile
from subprocess import Popen, call, STDOUT

try:
    import SeleniumLibrary
except ImportError:
    print 'Importing SeleniumLibrary module failed.'
    print 'Please make sure you have SeleniumLibrary installed.'
    sys.exit(1)


ROOT = os.path.dirname(os.path.abspath(__file__))
DEMOAPP = os.path.join(ROOT, 'demoapp', 'server.py')


def run_tests(args):
    start_selenium_server()
    start_demo_application()
    call(['pybot'] + args, shell=(os.sep == '\\'))
    stop_demo_application()
    stop_selenium_server()

def start_demo_application():
    Popen(['python', DEMOAPP, 'start'], stdout=TemporaryFile(), stderr=STDOUT)

def stop_demo_application():
    call(['python', DEMOAPP, 'stop'], stdout=TemporaryFile(), stderr=STDOUT)

def start_selenium_server():
    logfile = open(os.path.join(ROOT, 'selenium_log.txt'), 'w')
    SeleniumLibrary.start_selenium_server(logfile)

def stop_selenium_server():
    SeleniumLibrary.shut_down_selenium_server()

def print_help():
    print __doc__

def print_usage():
    print 'Usage: rundemo.py [options] datasource'
    print '   or: rundemo.py demoapp start|stop'
    print '   or: rundemo.py selenium start|stop'
    print '   or: rundemo.py help'


if __name__ == '__main__':
    action = {'demoapp-start': start_demo_application,
              'demoapp-stop': stop_demo_application,
              'selenium-start': start_selenium_server,
              'selenium-stop': stop_selenium_server,
              'help': print_help,
              '': print_usage}.get('-'.join(sys.argv[1:]))
    if action:
        action()
    else:
        run_tests(sys.argv[1:])
