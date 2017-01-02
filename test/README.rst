Testing and debugging
=====================
Requirements
------------
Before running the test, install the dependecies::

    pip install requirements.txt
    pip install requirements-dev.txt


Unit and Acceptance Tests
-------------------------

The test directory contains everything needed to run Selenium2Library
tests with Robot Framework. This includes:

- Unit tests under `unit` directory.
- Acceptance tests written with Robot Framework under `acceptance`
  directory
- A very simple `httpserver.py` which is used to serve the html for tests in
  `resources/testserver`
- A collection of simple html files under `resources/html` directory
- Start-up scripts for executing the tests: `run_tests.py` and
  `run_unit_tests.py`

To run unit and acceptance tests, run::

    python test/run_tests.py ff|ie|chrome

Tests are executed using Robot Framework and results verified automatically
afterwards using `robotstatuschecker` tool. The tool can be installed using
`pip install robotstatuschecker` and more information about it can be found
from: https://github.com/robotframework/statuschecker/. Notice that initially
some tests fail.


It is posisble to pass Robot Framework command line arguments to the test
exection as a last arguments to the `run_tests.py` command. Example arguments
like --test, --suite, --include and --exclude may be used to configure
acceptance test execution.

Examples::

    python run_tests.py chrome
    python run_tests.py --interpreter jython firefox --suite javascript
    python run_tests.py chrome --sauceusername your_username --saucekey account_key --suite javascript
    py -3 run_tests.py --interpreter "py -2" chrome --suite javascript

To run just the unit tests, run::

    python test/run_unit_tests.py

Using Sauce Labs for acceptance tests
-------------------------------------

When running test by using browser from Sauce labs, it is required that the
Sauce Connect is used. The Sauce Connect allows the browser from Sauce Labs
reach the acceptance test webserver. The acceptance test uses tunnel with
name `localtunnel` and therefore when establishing the Sauce Connect tunnel
use the following command::
    bin/sc -u YOUR_USERNAME -k YOUR_ACCESS_KEY -i localtunnel

More details and to downlaod Sauce Connect visit:
https://wiki.saucelabs.com/display/DOCS/High+Availability+Sauce+Connect+Setup
