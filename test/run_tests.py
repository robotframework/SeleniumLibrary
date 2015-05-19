#!/usr/bin/env python

import env
import os
import sys
from subprocess import Popen, call
from tempfile import TemporaryFile

from run_unit_tests import run_unit_tests

ROBOT_ARGS = [
    '--doc', 'SeleniumSPacceptanceSPtestsSPwithSP%(browser)s',
    '--outputdir', '%(outdir)s',
    '--variable', 'browser:%(browser)s',
    '--variable', 'pyversion:%(pyVersion)s',
    '--escape', 'space:SP',
    '--report', 'none',
    '--log', 'none',
    #'--suite', 'Acceptance.Keywords.Textfields',
    '--loglevel', 'DEBUG',
    '--pythonpath', '%(pythonpath)s',
    '--noncritical', 'known_issue_-_%(pyVersion)s',
    '--noncritical', 'known_issue_-_%(browser)s',
]
REBOT_ARGS = [
    '--outputdir', '%(outdir)s',
    '--name', '%(browser)sSPAcceptanceSPTests',
    '--escape', 'space:SP',
    '--critical', 'regression',
    '--noncritical', 'inprogress',
    '--noncritical', 'known_issue_-_%(pyVersion)s',
    '--noncritical', 'known_issue_-_%(browser)s',
]
ARG_VALUES = {'outdir': env.RESULTS_DIR, 'pythonpath': ':'.join((env.SRC_DIR, env.TEST_LIBS_DIR))}

def acceptance_tests(interpreter, browser, args):
    ARG_VALUES['browser'] = browser.replace('*', '')
    ARG_VALUES['pyVersion'] = interpreter + sys.version[:3]
    start_http_server()
    runner = {'python': 'pybot', 'jython': 'jybot', 'ipy': 'ipybot'}[interpreter]
    if os.sep == '\\':
        runner += '.bat'
    execute_tests(runner, args)
    stop_http_server()
    return process_output(args)

def start_http_server():
    server_output = TemporaryFile()
    Popen(['python', env.HTTP_SERVER_FILE ,'start'],
          stdout=server_output, stderr=server_output)

def execute_tests(runner, args):
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    command = [runner] + [arg % ARG_VALUES for arg in ROBOT_ARGS] + args + [env.ACCEPTANCE_TEST_DIR]
    print ''
    print 'Starting test execution with command:\n' + ' '.join(command)
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    call(command, shell=os.sep=='\\', env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))

def stop_http_server():
    call(['python', env.HTTP_SERVER_FILE, 'stop'])

def process_output(args):
    print
    if _has_robot_27():
        call(['python', os.path.join(env.RESOURCES_DIR, 'statuschecker.py'),
             os.path.join(env.RESULTS_DIR, 'output.xml')])
    rebot = 'rebot' if os.sep == '/' else 'rebot.bat'
    rebot_cmd = [rebot] + [ arg % ARG_VALUES for arg in REBOT_ARGS ] + args + \
                [os.path.join(ARG_VALUES['outdir'], 'output.xml') ]
    print ''
    print 'Starting output processing with command:\n' + ' '.join(rebot_cmd)
    rc = call(rebot_cmd, env=os.environ)
    if rc == 0:
        print 'All critical tests passed'
    else:
        print '%d critical test%s failed' % (rc, 's' if rc != 1 else '')
    return rc

def _has_robot_27():
    try:
        from robot.result import ExecutionResult
    except:
        return False
    return True

def _exit(rc):
    sys.exit(rc)

def _help():
    print 'Usage:  python run_tests.py python|jython browser [options]'
    print
    print 'See README.txt for details.'
    return 255

def _run_unit_tests():
    print 'Running unit tests'
    failures = run_unit_tests()
    if failures != 0:
        print '\n%d unit tests failed - not running acceptance tests!' % failures
    else:
        print 'All unit tests passed'
    return failures


if __name__ ==  '__main__':
    if not len(sys.argv) > 2:
        _exit(_help())
    unit_failures = _run_unit_tests()
    if unit_failures:
        _exit(unit_failures)
    interpreter = sys.argv[1]
    browser = sys.argv[2].lower()
    args = sys.argv[3:]
    if browser != 'unit':
        _exit(acceptance_tests(interpreter, browser, args))
