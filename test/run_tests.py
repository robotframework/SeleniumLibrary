#!/usr/bin/env python

from __future__ import print_function

import os
import sys
from subprocess import Popen, call
from tempfile import TemporaryFile

import env
from run_unit_tests import run_unit_tests


REBOT_ARGS = [
    '--outputdir', '%(outdir)s',
    '--name', '%(browser)sSPAcceptanceSPTests',
    '--escape', 'space:SP',
    '--noncritical', 'known_issue_%(browser)s',
]

ROBOT_ARGS = [
    '--doc', 'SeleniumSPacceptanceSPtestsSPwithSP%(browser)s',
    '--outputdir', '%(outdir)s',
    '--variable', 'browser:%(browser)s',
    '--variable', 'pyversion:%(pyVersion)s',
    '--escape', 'space:SP',
    '--loglevel', 'DEBUG',
    '--pythonpath', '%(pythonpath)s',
    '--noncritical', 'known_issue_%(browser)s',
]

ARG_VALUES = {
    'outdir': env.RESULTS_DIR,
    'pythonpath': ':'.join((env.SRC_DIR, env.TEST_LIBS_DIR))
}


def acceptance_tests(interpreter, browser, args):
    ARG_VALUES['browser'] = browser.replace('*', '')
    ARG_VALUES['pyVersion'] = interpreter + sys.version[:3]
    ARG_VALUES['sauceUserName'] = env.SAUCE_USERNAME
    ARG_VALUES['sauceAccessKey'] = env.SAUCE_ACCESS_KEY
    ARG_VALUES['travisJobNumber'] = env.TRAVIS_JOB_NUMBER

    if env.TRAVIS:
        ROBOT_ARGS.extend(['--variable', 'SAUCE_USERNAME:%(sauceUserName)s'])
        ROBOT_ARGS.extend(['--variable', 'SAUCE_ACCESS_KEY:%(sauceAccessKey)s'])
        if env.BROWSER != "firefox":
            ROBOT_ARGS.extend(
                ['--variable',
                 'DESIRED_CAPABILITIES:build:%(travisJobNumber)s-%(browser)s,tunnel-identifier:%(travisJobNumber)s'
                 ]
            )
            ROBOT_ARGS.extend(
                [
                    '--variable',
                    'REMOTE_URL:http://%(sauceUserName)s:%(sauceAccessKey)s@ondemand.saucelabs.com:80/wd/hub'
                 ]
            )
    start_http_server()
    runner = {'python': 'pybot', 'jython': 'jybot', 'ipy': 'ipybot'}[interpreter]
    if os.sep == '\\':
        runner += '.bat'
    try:
        return execute_tests(runner, args)
    finally:
        stop_http_server()


def start_http_server():
    server_output = TemporaryFile()
    Popen(['python', env.HTTP_SERVER_FILE, 'start'],
          stdout=server_output, stderr=server_output)


def execute_tests(runner, args):
    if not os.path.exists(env.RESULTS_DIR):
        os.mkdir(env.RESULTS_DIR)
    command = [runner] + [arg % ARG_VALUES for arg in ROBOT_ARGS] + args + [env.ACCEPTANCE_TEST_DIR]
    # replace sensitive information
    commands = ' '.join(command)
    if env.BROWSER != "firefox":
        for hidden in (env.SAUCE_USERNAME, env.SAUCE_ACCESS_KEY):
            commands = commands.replace(hidden, "*" * len(hidden))
    print('Starting test execution with command:\n' + commands + "\n")
    syslog = os.path.join(env.RESULTS_DIR, 'syslog.txt')
    return call(command, shell=os.sep=='\\', env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def stop_http_server():
    call(['python', env.HTTP_SERVER_FILE, 'stop'])


def process_output(args):
    print()
    call(['python', os.path.join(env.RESOURCES_DIR, 'statuschecker.py'),
         os.path.join(env.RESULTS_DIR, 'output.xml')])
    rebot = 'rebot' if os.sep == '/' else 'rebot.bat'
    rebot_cmd = [rebot] + [arg % ARG_VALUES for arg in REBOT_ARGS] + args + \
                [os.path.join(ARG_VALUES['outdir'], 'output.xml')]
    print('Starting output processing with command:\n' + ' '.join(rebot_cmd))
    rc = call(rebot_cmd, env=os.environ)
    if rc == 0:
        print('All critical tests passed')
    else:
        print('%d critical test%s failed' % (rc, 's' if rc != 1 else ''))
    return rc


def _exit(rc):
    sys.exit(rc)


def _help():
    print('Usage:  python run_tests.py python|jython browser [options]')
    print()
    print('See README.txt for details.')
    sys.exit(255)


def _run_unit_tests():
    print('Running unit tests')
    failures = run_unit_tests()
    if failures != 0:
        print('\n%d unit tests failed - not running acceptance tests!' % failures)
    else:
        print('All unit tests passed')
    return failures


if __name__ == '__main__':
    if not len(sys.argv) > 2:
        _help()
    unit_failures = _run_unit_tests()
    if unit_failures:
        sys.exit(unit_failures)
    interpreter = sys.argv[1]
    browser = sys.argv[2].lower()
    args = sys.argv[3:]
    if browser != 'unit':
        rc = acceptance_tests(interpreter, browser, args)
        sys.exit(rc)
