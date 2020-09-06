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

    python atest/run.py <browser>

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

Running test with Selenium Grid
-------------------------------
It is possible to run test by using `Selenium Grid`_ if keywords contains
some grid specific implementation. Running test Selenium Grid requires
that latest released  selenium-server-standalone-*.jar is downloaded
in the project root and Java is installed. The `run.py` will start and
stop Selenium servers automatically. The testing with Selenium Grid
can done by using `--grid true` argument. In some cases Selenium Grid adds
some extra logging and causes test to fail when `robotstatuschecker`_ is
used. In this case, these test should be tagged with `NoGrid` tag to
exclude the test when Selenium Grid is being used. Also there might
be need write test that are only run when Selenium Grid is used.
Then in this case, test should be tagged with `OnlyGrid` tag to
include them only when Selenium Grid is used.

Robot Framework command line arguments
--------------------------------------
It is possible to pass Robot Framework command line arguments to the test
execution as last arguments to the `run.py` command. It is recommended
to use arguments to select required suite or test for the execution when
developing new functionality for the library. Example like --test, --suite,
--include and --exclude.

Examples
--------
Examples::

    run.py chrome
    run.py --interpreter c:\Python38\python.exe firefox --suite javascript
    run.py headlesschrome --nounit --grid true
    run.py --interpreter "py -2" chrome --suite javascript

To run just the unit tests, run::

    python utest/run.py
    
To full list of options run::

    python atest/run.py --help

Travis CI integration
---------------------
`Travis CI`_ is used to automatically test all new pull request to the
repository. The detailed information about execution matrix can be found
from the `.travis.yam`_. Generally speaking the test are automatically run
by using Chrome browser and by using supported Python and Robot Framework
versions. But in Travis only the latest released Selenium version is used.

.. _browser driver: https://github.com/robotframework/SeleniumLibrary#browser-drivers
.. _PATH: https://en.wikipedia.org/wiki/PATH_(variable)
.. _robotstatuschecker: https://github.com/robotframework/statuschecker/
.. _Travis CI: https://travis-ci.org/robotframework/SeleniumLibrary
.. _.travis.yam: https://github.com/robotframework/SeleniumLibrary/blob/master/.travis.yml
.. _Selenium Grid: https://github.com/SeleniumHQ/selenium/wiki/Grid2
