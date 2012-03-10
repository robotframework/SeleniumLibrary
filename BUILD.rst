Selenium2Library Developer Information
======================================


Directory Layout
----------------

MANIFEST.in
	File that controls what gets included in a distribution

setup.py
	Setup script (uses setuptools)

demo/
    Demo web app, acceptance tests, and scripts

doc/
    Scripts to build keyword and readme documentation

src/
    Library source code

test/
    Unit and acceptance tests for Selenium2Library


Unit and Acceptance Tests
-------------------------

The test directory contains everything needed to run Selenium2Library 
tests with Robot Framework. This includes:

- Unit tests under `unit` directory.
- Acceptance tests written with Robot Framework under `acceptance` 
  directory
- A very simple httpserver.py which is used to serve the html for tests in
  `resources/testserver`
- A collection of simple html files under 'resources/html' directory
- Start-up scripts for executing the tests

To run unit and acceptance tests, run::

	python test/run_tests.py python|jython ff|ie|chrome [options]

The first argument to the script defines the interpreter to be used
to run Robot. The second argument defines the browser to be used,
using the same browser tokens that you would use in your Robot
tests.

Due to the structure of the tests, the directory containg the test
case files (`acceptance`) is always given to Robot as test data path.
To run only a subset of test cases, Robot command line arguments
--test, --suite, --include and --exclude may be used.

Examples::

	# Run all tests with Python and Firefox
	python test/run_tests.py python ff
	# Run only test suite `javascript` with Jython and Internet Explorer
	python test/run_tests.py jython ie -s javascript

To run just the unit tests, run::

	python test/run_unit_tests.py


Building a Distribution
-----------------------

To build a distribution, run::

	python build_dist.py

This script will:

- Generate source distribution packages in .tar.gz and .zip formats
- Generate build distribution packages for Windows x86 and x64
- Generate a demo distribution package in .zip format.
- Re-generate keyword documentation in doc folder


Building Keyword Documentation
------------------------------

The keyword documentation will get built automatically by build_dist.py,
but if you need to generate it apart from a distribution build, run::

	python doc/generate.py


Building Readme Files
---------------------

The readme files get distributed in reStructuredText format (.rst),
so there isn't any reason to build them except to verify how they
are parsed by the reStructuredText parser. To build them, run::

	python doc/generate_readmes.py


Pushing Code to GitHub
----------------------

Assuming the remote has been setup and named `origin` (it is 
setup and named `origin` automatically if you cloned the existing
GitHub repo), run::

	git push origin master


Pushing Keyword Documentation
-----------------------------

The keyword documentation is hosted using GitHub Pages. There is a branch
in the repo called `gh-pages` that contains nothing but the keyword documentation.

First, switch to the `gh-pages` branch::

	git checkout gh-pages

Next, pull the keyword documentation you generated in the master branch and commit it::

	git checkout master doc/Selenium2Library.html
	git add .
	git commit

Then, push it to the remote::

	git push origin gh-pages

Last, you probably want to switch back to the master branch::

	git checkout master
