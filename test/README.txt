Selenium Library Tests
======================

Introduction
------------

This directory contains everything needed to run SeleniumLibrary 
tests with Robot Framework. This includes:

- Unit tests under `utest` directory.
- Acceptance tests written with Robot Framework under `acceptance` 
  directory
- A very simple httpserver.py which is used to serve the html for tests in
  `resources/testserver`
- A collection of simple html files under 'resources/html' directory
- Start-up scripts for executing the tests


Running Tests
-------------

There's a python script for running the tests. It can be
used as follows:

python run_tests.py python|jython ff|ie [options]  

The first argument to the scrip defines the interpreter to be used
to run Robot. The second argument defines the browser to be used.
At the moment the script only recognizes Firefox and Internet Explorer,
but new browser maybe added when needed.

Due to the structure of the tests, the directory containg the test
case files (`acceptance`) is always given to Robot as test data path.
To run only a subset of test cases, Robot command line arguments
--test, --suite, --include and --exclude may be used.

The script always runs unit tests before starting the browser tests. To run
only unit tests, a special value `unit` may be used as a browser.

Examples::
  # Run all test with Python and Firefox
  atest/run_tests.py python ff
  # Run only test suite `javascript` with Jython and Internet Explorer
  atest/run_tests.py jython ie -s javascrip


Failing Tests
-------------

When the tests are executed, a number of test cases can be seen to
fail in the console output.  This is because these test cases are
designed to test error messages of SeleniumLibrary.  The script
'teststatuschecker.py' is used to check that these test cases failed
with expected error message. After that, report and log files are
generated and these files show the correct status of the test run.


TODO: docuement syntax of documentation for statuschecker

