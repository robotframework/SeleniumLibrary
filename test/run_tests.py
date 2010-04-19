#!/usr/bin/env python

#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
import sys
from subprocess import Popen, call
from tempfile import TemporaryFile

from robot import utils

from run_unit_tests import run_unit_tests


ROOT = os.path.dirname(__file__)
TESTDATADIR = os.path.join(ROOT, 'acceptance')
RESOURCEDIR = os.path.join(ROOT, 'resources')
SRCDIR = os.path.join(ROOT, '..', 'src')
UTESTDIR = os.path.join(ROOT, 'unit')
RESULTDIR = os.path.join(ROOT, 'results')
HTPPSERVER = os.path.join(RESOURCEDIR, 'testserver', 'testserver.py')
ROBOT_ARGS = [
'--doc', 'SeleniumSPacceptanceSPtestsSPwithSP%(browser)s',
'--outputdir', '%(outdir)s',
'--variable', 'browser:%(browser)s',
'--escape', 'space:SP',
'--report', 'none',
'--log', 'none',
'--loglevel', 'DEBUG',
'--pythonpath', '%(pythonpath)s',
]
REBOT_ARGS = [
'--outputdir', '%(outdir)s',
'--name', '%(browser)sSPAcceptanceSPTests',
'--escape', 'space:SP',
'--critical', 'regression',
]
ARG_VALUES = {'outdir': RESULTDIR, 'pythonpath': SRCDIR}


def acceptance_tests(interpreter, browser, args):
    ARG_VALUES['browser'] = browser.replace('*', '')
    # TODO: running unit tests this way fails on my Windows, why?
    start_http_server()
    suffix = utils.is_windows and 'ybot.bat' or 'ybot'
    runner = "%s%s" % ('jython' == interpreter and 'j' or 'p', suffix)
    execute_tests(runner)
    stop_http_server()
    return process_output()

def start_http_server():
    server_output = TemporaryFile()
    Popen(['python', HTPPSERVER ,'start'],
          stdout=server_output, stderr=server_output)

def execute_tests(runner):
    command = [runner] + [ arg % ARG_VALUES for arg in ROBOT_ARGS] + args +\
            [ TESTDATADIR ]
    call(command, env=os.environ)

def stop_http_server():
    call(['python', HTPPSERVER, 'stop'])

def process_output():
    print
    call(['python', os.path.join(RESOURCEDIR, 'statuschecker.py'),
         os.path.join(RESULTDIR, '%s-output.xml' % ARG_VALUES['browser'])])
    rebot = utils.is_windows and 'rebot.bat' or 'rebot'
    rebot_cmd = [rebot] + [ arg % ARG_VALUES for arg in REBOT_ARGS ] + \
                [os.path.join(ARG_VALUES['outdir'], '%s-output.xml' % ARG_VALUES['browser'] ) ]
    rc = call(rebot_cmd, env=os.environ)
    if rc == 0:
        print 'All critical tests passed'
    else:
        print '%d critical test%s failed' % (rc, 's' if rc != 1 else '')
    return rc


if __name__ ==  '__main__':
    if not len(sys.argv) > 2:
        print 'usage: python run_acceptance_tests python|jython browser [options]'
        print 'where `browser` is any browser or alias accepted by SeleniumLibrary.'
        sys.exit(1)
    interpreter = sys.argv[1] == 'jython' and 'jython' or 'python'
    browser = sys.argv[2].lower()
    args = sys.argv[3:]
    if not args:
        if interpreter == 'jython':
            print 'This script does not run unit tests with Jython'
            print 'They can be excecuted with jython test/run_unit_tests.py'
        else:
            print 'Running unit tests'
            failures = run_unit_tests()
            if failures != 0:
                print '\n%d unit tests failed - not running acceptance tests!' % failures
                sys.exit(1)
            print 'All unit tests passed'
    if browser != 'unit':
        sys.exit(acceptance_tests(interpreter, browser, args))
