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

When Selenium Grid is used, it is possible to include and exclude test.
Generally speaking almost all test should work when Selenium Grid is used,
but there few valid exceptions. If test uses `robotstatuschecker` tool
to verify logging of the keyword, in some cases Selenium Grid adds
some extra logging and causes test to fail. In this case, these test
should be tagged with `NoGrid` tag to exclude the test when Selenium Grid
is being used. Also there might be need write test that are only run
when Selenium Grid is used. Then in this case, test should be tagged with
`OnlyGrid` tag to include them only when Selenium Grid is used.

It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run_tests.py` command. It is
recommended to use arguments to select required suite or test for the
execution when developing new functionality for the library. Example like
--test, --suite, --include and --exclude.

Examples:

    run.py chrome
    run.py headlesschrome
    run.py --interpreter c:\Python38\python.exe firefox --suite javascript
    run.py headlesschrome --nounit --grid true
"""

import platform
import time
import zipfile
from contextlib import contextmanager
import os
import sys
import argparse
import textwrap
import shutil
import subprocess
import tempfile

from robot import rebot_cli
from robot import __version__ as robot_version
from robot.utils import is_truthy

try:
    import robotstatuschecker
except ImportError:
    sys.exit(
        "Required `robotstatuschecker` not installed.\n"
        "Install it with `pip install robotstatuschecker`."
    )
import requests


# Folder settings
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPTANCE_TEST_DIR = os.path.join(ROOT_DIR, "acceptance")
UNIT_TEST_RUNNER = os.path.join(ROOT_DIR, os.pardir, "utest", "run.py")
RESOURCES_DIR = os.path.join(ROOT_DIR, "resources")
RESULTS_DIR = os.path.join(ROOT_DIR, "results")
ZIP_DIR = os.path.join(ROOT_DIR, "zip_results")
SRC_DIR = os.path.normpath(os.path.join(ROOT_DIR, os.pardir, "src"))
TEST_LIBS_DIR = os.path.join(RESOURCES_DIR, "testlibs")
HTTP_SERVER_FILE = os.path.join(RESOURCES_DIR, "testserver", "testserver.py")
EVENT_FIRING_LISTENER = os.path.join(RESOURCES_DIR, "testlibs", "MyListener.py")

ROBOT_OPTIONS = [
    "--doc",
    "SeleniumLibrary acceptance tests with {browser}",
    "--outputdir",
    RESULTS_DIR,
    "--variable",
    "BROWSER:{browser}",
    "--report",
    "NONE",
    "--log",
    "NONE",
    "--loglevel",
    "DEBUG",
    "--pythonpath",
    SRC_DIR,
    "--pythonpath",
    TEST_LIBS_DIR,
]
REBOT_OPTIONS = [
    "--outputdir",
    RESULTS_DIR,
    "--noncritical",
    "known issue {browser}",
]


def acceptance_tests(interpreter, browser, rf_options=None, grid=None, event_firing=None):
    if os.path.exists(RESULTS_DIR):
        shutil.rmtree(RESULTS_DIR)
    os.mkdir(RESULTS_DIR)
    if grid:
        hub, node = start_grid()
    with http_server():
        execute_tests(interpreter, browser, rf_options, grid, event_firing)
    failures = process_output(browser)
    if failures:
        print(
            "\n{} critical test{} failed.".format(
                failures, "s" if failures != 1 else ""
            )
        )
    else:
        print("\nAll critical tests passed.")
    if grid:
        hub.kill()
        node.kill()
    return failures


def start_grid():
    node_file = tempfile.TemporaryFile()
    hub_file = tempfile.TemporaryFile()
    selenium_jar = None
    for file in os.listdir("."):
        if file.startswith("selenium-server-standalone"):
            selenium_jar = file
            break
    if not selenium_jar:
        raise ValueError("Selenium server jar not found: %s" % selenium_jar)
    hub = subprocess.Popen(
        ["java", "-jar", selenium_jar, "-role", "hub", "-host", "localhost"],
        stderr=subprocess.STDOUT,
        stdout=hub_file,
    )
    time.sleep(2)  # It takes about two seconds to start the hub.
    ready = _grid_status(False, "hub")
    if not ready:
        hub.kill()
        raise ValueError("Selenium grid hub was not ready in 60 seconds.")
    node = subprocess.Popen(
        ["java", "-jar", selenium_jar, "-role", "node"],
        stderr=subprocess.STDOUT,
        stdout=node_file,
    )
    ready = _grid_status(True, "node")
    if not ready:
        hub.kill()
        node.kill()
        raise ValueError("Selenium grid node was not ready in 60 seconds.")
    return hub, node


def _grid_status(status=False, role="hub"):
    count = 0
    while True:
        try:
            response = requests.get("http://localhost:4444/wd/hub/status")
            data = response.json()
            if data["value"]["ready"] == status:
                print("Selenium grid %s ready/started." % role)
                return True
        except Exception:
            pass
        count += 1
        if count == 12:
            raise ValueError("Selenium grid %s not ready/started in 60 seconds." % role)
        print("Selenium grid %s not ready/started." % role)
        time.sleep(5)


@contextmanager
def http_server():
    serverlog = open(os.path.join(RESULTS_DIR, "serverlog.txt"), "w")
    process = subprocess.Popen(
        ["python", HTTP_SERVER_FILE, "start"],
        stdout=serverlog,
        stderr=subprocess.STDOUT,
    )
    try:
        yield
    finally:
        subprocess.call(["python", HTTP_SERVER_FILE, "stop"])
        process.wait()
        serverlog.close()


def execute_tests(interpreter, browser, rf_options, grid, event_firing):
    options = []
    if grid:
        runner = interpreter.split() + [
            "-m",
            "pabot.pabot",
            "--processes",
            "2",
        ]
    else:
        runner = interpreter.split() + ["-m", "robot.run"]
    options.extend([opt.format(browser=browser) for opt in ROBOT_OPTIONS])
    if rf_options:
        options += rf_options
    command = runner
    if grid:
        command += [
            "--variable",
            "REMOTE_URL:http://localhost:4444/wd/hub",
            "--exclude",
            "NoGrid",
        ]
    else:
        command += ["--exclude", "OnlyGrid"]
    if event_firing:
        command += [
            "--variable",
            f"event_firing_or_none:{EVENT_FIRING_LISTENER}",
        ]
    command += options + [ACCEPTANCE_TEST_DIR]
    log_start(command)
    syslog = os.path.join(RESULTS_DIR, "syslog.txt")
    subprocess.call(command, env=dict(os.environ, ROBOT_SYSLOG_FILE=syslog))


def log_start(command_list, *hiddens):
    command = subprocess.list2cmdline(command_list)
    for hidden in hiddens:
        if hidden:
            command = command.replace(hidden, "*" * len(hidden))
    print()
    print("Starting test execution with command:")
    print(command)


def process_output(browser):
    print("Verifying results...")
    options = []
    output = os.path.join(RESULTS_DIR, "output.xml")
    robotstatuschecker.process_output(output, verbose=False)
    options.extend([opt.format(browser=browser) for opt in REBOT_OPTIONS])
    try:
        rebot_cli(options + [output])
    except SystemExit as exit:
        return exit.code


def create_zip():
    if os.path.exists(ZIP_DIR):
        shutil.rmtree(ZIP_DIR)
    os.mkdir(ZIP_DIR)
    python_version = platform.python_version()
    zip_name = f"rf-{robot_version}-python-{python_version}.zip"
    zip_path = os.path.join(ZIP_DIR, zip_name)
    print("Zip created in: %s" % zip_path)
    zip_file = zipfile.ZipFile(zip_path, "w")
    for root, dirs, files in os.walk(RESULTS_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.join("SeleniumLibrary/atest/result", file)
            zip_file.write(file_path, arcname)
    zip_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="\n".join(__doc__.splitlines()[2:]),
    )
    parser.add_argument(
        "--interpreter",
        "-I",
        default="python",
        help=textwrap.dedent(
            """\
                            Any Python interpreter supported by the library.
                            E.g. `python` or `c:\\Python38\\python.exe`.
                            By default set to `python`."""
        ),
    )
    parser.add_argument(
        "browser",
        help=("Any browser supported by the library (e.g. `chrome`or `firefox`)."),
    )
    parser.add_argument(
        "--nounit",
        help="Does not run unit test when set.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--grid", "-G", help="Run test by using Selenium grid", default=False
    )
    parser.add_argument(
        "--zip",
        help="Creates zip file from output dir.",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--event-firing-webdriver",
        help="Run tests using event firing webdriver.",
        default=False,
        action="store_true",
    )
    args, rf_options = parser.parse_known_args()
    browser = args.browser.lower().strip()
    selenium_grid = is_truthy(args.grid)
    interpreter = args.interpreter
    event_firing_webdriver = args.event_firing_webdriver
    if args.nounit:
        print("Not running unit tests.")
    else:
        rc = subprocess.call([interpreter, UNIT_TEST_RUNNER])
        if rc != 0:
            print("Not running acceptance test, because unit tests failed.")
            sys.exit(rc)
    failures = acceptance_tests(interpreter, browser, rf_options, selenium_grid, event_firing_webdriver)
    if args.zip:
        create_zip()
    sys.exit(failures)
