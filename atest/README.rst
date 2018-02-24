Testing
=======
Requirements
------------
Before running the test, install the dependencies::

    pip install -r requirements-dev.txt

Also before running the tests, install the `browser driver`_ the `PATH`_.

Acceptance Tests
----------------
The atest directory contains everything needed to run SeleniumLibrary
acceptance tests with Robot Framework. This includes:

- Acceptance tests written with Robot Framework under `acceptance`
  directory.
- A very simple `httpserver.py` which is used to serve the html for tests in
  `resources/testserver`.
- A collection of simple html files under `resources/html` directory.
- Start-up scripts for executing the unit and acceptance tests: `run.py`.

To run unit and acceptance tests, run::

    python test/run.py <browser>

Acceptance tests are executed using Robot Framework and results verified
automatically afterwards using `robotstatuschecker`_ tool. Please visit
`robotstatuschecker`_ for more details how the tool can be used. Notice that
initially some tests fail.

Running test with different interpreter
---------------------------------------
By default the interpreter is set to `python` and it depends on the operating
system settings, which python is used by default. It is possible to run test
by using different interpreter by using the `--interpreter` command line
argument.

Robot Framework command line arguments
--------------------------------------
It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run.py` command. It is recommended
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

    run.py chrome
    run.py --interpreter jython firefox --suite javascript
    run.py chrome --sauceusername your_username --saucekey account_key --suite javascript
    run.py --interpreter "py -2" chrome --suite javascript

To run just the unit tests, run::

    python utest/run.py

Travis CI integration
---------------------
`Travis CI`_ is used to automatically test all new pull request to the
repository. The detailed information about execution matrix can be found
from the `.travis.yam`_. Generally speaking the test are automatically run
by using Chrome and Firefox browsers. The project uses Python 2.7, Python 3.3,
Python 3.6 and PyPy 3.5 for test execution. The project uses Selenium 2.53.6
and latest available Selenium 3 version for test execution. Test uses
Robot Framework versions 2.8.7, 2.9.2 and 3.0.2 for acceptance test execution.

.. _browser driver: https://github.com/robotframework/SeleniumLibrary#browser-drivers
.. _PATH: https://en.wikipedia.org/wiki/PATH_(variable)
.. _robotstatuschecker: https://github.com/robotframework/statuschecker/
.. _Travis CI: https://travis-ci.org/robotframework/SeleniumLibrary
.. _.travis.yam: https://github.com/robotframework/SeleniumLibrary/blob/master/.travis.yml
