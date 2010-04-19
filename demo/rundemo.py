#! /usr/bin/env python

'''Selenium Library Demo Runner

Usage: rundemo.py [options] datasource

This script starts necessary helper programs (a simple HTTP server and Selenium
server) and executes the given test case file/directory. After test cases have
finished executing, the helper programs are shut down. 

Options are passed to Robot Framework as they are given, for a complete list
of options, run 'pybot --help'.

By default, tests are executed with Firefox browser, this can be changed by
using command line option '--variable', eg. '--variable BROWSER:ie'. Selenium
Library documentation lists the accepted values of browser.

The speed of the test execution can be slowed by defining a non-zero value for
variable delay, eg. '--variable DELAY:2'

For debugging purposes, the output of Selenium server is written in 
'selenium_log.txt' under the 'reports' directory.

Requires that Robot Framework, Selenium Library, Python 2.4 or newer and 
Java 1.5 or newer are installed.
'''

import os
import sys
import time
import tempfile
from subprocess import Popen, call, STDOUT

import SeleniumLibrary
from SeleniumLibrary import selenium

INSTPATH = os.path.split(os.path.abspath(SeleniumLibrary.__file__))[0]
TMPFILE = tempfile.TemporaryFile()
if not os.path.exists('reports'):
    os.mkdir('reports')
SELENIUM_LOG_FILE = open(os.path.join('reports', 'selenium_log.txt'), 'w')
DEFAULT_ARGS = [ 
'--outputdir', 'reports', 
'--log', 'demo_log.html',
'--report', 'demo_report.html', 
'--output', 'demo_output.xml',
'--reporttitle', 'Selenium_Demo_Tests_Report',
'--logtitle', 'Selenium_Demo_Tests_Log']

def start_apps():
    jarpath = os.path.join(INSTPATH, 'lib', 'selenium-server.jar')
    Popen(['java', '-jar', jarpath], stdout=SELENIUM_LOG_FILE, stderr=STDOUT)
    Popen(['python', 'httpserver/httpserver.py', 'start'], 
            stdout=TMPFILE, stderr=TMPFILE) 
    time.sleep(1)

def run_demo(cmdline_args):
    shell = (os.sep == '\\')
    call(['pybot'] + DEFAULT_ARGS + cmdline_args, shell=shell)
    print 'Selenium log:', os.path.abspath(SELENIUM_LOG_FILE.name)

def stop_apps():
    Popen(['python', 'httpserver/httpserver.py', 'stop'], stdout=TMPFILE, 
            stderr=STDOUT) 
    selenium('localhost', 4444, '', '').do_command('shutDownSeleniumServer', [])

if __name__ == '__main__':
    if len(sys.argv) < 2 or '--help' in sys.argv[1]:
        print __doc__
        sys.exit(1)
    start_apps()
    run_demo(sys.argv[1:])
    stop_apps()
    SELENIUM_LOG_FILE.close()
    TMPFILE.close()

