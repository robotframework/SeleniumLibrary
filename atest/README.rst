Testing and debugging
=====================
Requirements
------------
Before running the test, install the dependencies::

    pip install -r requirements.txt
    pip install -r requirements-dev.txt


Unit and Acceptance Tests
-------------------------

The test directory contains everything needed to run SeleniumLibrary
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

    python test/run_tests.py <browser>

Acceptance tests are executed using Robot Framework and results verified
automatically afterwards using `robotstatuschecker`_ tool. Please visit
`robotstatuschecker`_ for more details how the tool can be used. Notice that
initially some tests fail.

Units tests are written by using the Python default `unittest`_ framework.
Unit test can be executed separately by running::

    python test/run_unit_tests.py


Running test with different interpreter
---------------------------------------

By default the interpreter is set to `python` and it depends on the  operating
system settings, which python is used by default. It is possible to run test
by using different interpreter by using the `--interpreter` command line
argument.

Starting from version 3.0.0 onwards the SeleniumLibrary is tested by using
Python 2 and 3. Other interpreters are not tested by the development team.


Robot Framework command line arguments
--------------------------------------

It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run_tests.py` command. It is recommended
to use arguments to select required suite or test for the execution when
developing new functionality for the library. Example like --test, --suite,
--include and --exclude.


Using Sauce Labs for acceptance tests
-------------------------------------

When running test by using browser from Sauce labs, it is required that the
Sauce Connect is used. The Sauce Connect allows the browser from Sauce Labs
reach the acceptance test web server. The acceptance test uses tunnel with
name `localtunnel` and therefore when establishing the Sauce Connect tunnel
use the following command::

    bin/sc -u YOUR_USERNAME -k YOUR_ACCESS_KEY -i localtunnel

More details and to download Sauce Connect visit:
https://wiki.saucelabs.com/display/DOCS/High+Availability+Sauce+Connect+Proxy+Setup


Examples
--------

Examples::

    run_tests.py chrome
    run_tests.py --interpreter jython firefox --suite javascript
    run_tests.py chrome --sauceusername your_username --saucekey account_key --suite javascript
    run_tests.py --interpreter "py -2" chrome --suite javascript

To run just the unit tests, run::

    python test/run_unit_tests.py

Travis CI integration
---------------------

`Travis CI`_ is used to automatically test all new pull request to the
repository. Test are automatically run by using Chrome and Firefox  browsers,
by using on Python 2.7, Python 3.3 and Python 3.6. Acceptance test are also run
by using Selenium 2.53.6 and latest available Selenium 3 version and
acceptance test uses Robot Framework versions are: 2.8.7, 2.9.2 and 3.0.2.

.. _unittest: https://docs.python.org/3/library/unittest.html
.. _robotstatuschecker: https://github.com/robotframework/statuschecker/
.. _Travis CI: https://travis-ci.org/robotframework/SeleniumLibrary
