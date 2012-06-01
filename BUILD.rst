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


Pushing Code to GitHub
----------------------

Assuming the remote has been setup and named `origin` (it is 
setup and named `origin` automatically if you cloned the existing
GitHub repo), run::

	git push origin master


Building a Distribution
-----------------------

To build a distribution, run::

	python build_dist.py <python 2.6 path> <python 2.7 path>

This script will:

- Generate source distribution packages in .tar.gz and .zip formats
- Generate Python eggs for Python 2.6 and 2.7
- Generate binary installers for Windows x86 and x64 (if run on Windows)
- Generate a demo distribution package in .zip format.
- Re-generate keyword documentation in doc folder

Note: The Windows installers will only be built if the script is run on
a Windows machine. If the rest of the distribution has been built on
a non-Windows machine and you want to build just the Windows installers,
use the --winonly flag::

	python build_dist.py --winonly <python 2.6 path> <python 2.7 path>


Publishing a New Release
------------------------

Build the distribution, this time with the --release flag::

	python build_dist.py --release <python 2.6 path> <python 2.7 path>

In addition to building the distribution, this will:

- Register the release/version with PyPI
- Upload the binaries to PyPI for the new release/version

After building and releasing to PyPI:

- Upload dist packages to the `downloads section on GitHub`_ (all dist packages except the eggs)
- Publish the keyword documentation (see `Pushing Keyword Documentation`_)
- Tag the release (see `Tagging a Release`_)

Note: To publish a release, you will need to:

- Register an account on PyPI_ and be given rights to the package by a package owner
- Setup your `.pypirc file`_ (goes in the root of your home directory)


Tagging a Release
-----------------

It's our policy to tag each release. To do so, run::

	git tag -a v<ver> -m "<ver> release"
	git push --tags
	
E.g.::

	git tag -a v1.0.0 -m "1.0.0 release"
	git push --tags


Pushing Keyword Documentation
-----------------------------

The keyword documentation is hosted using GitHub Pages. There is a branch
in the repo called `gh-pages` that contains nothing but the keyword documentation.

First, switch to the `gh-pages` branch::

	git checkout gh-pages

If you get an error like "pathspec 'gh-pages' did not match any file(s) known to git",
run the following to setup the upstream configuration for the gh-pages branch::

	git checkout -t origin/gh-pages

Next, pull the keyword documentation you generated in the master branch and commit it::

	git checkout master doc/Selenium2Library.html
	git add doc/Selenium2Library.html
	git commit

Then, push it to the remote::

	git push origin gh-pages

Last, you probably want to switch back to the master branch::

	git checkout master


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


.. _downloads section on GitHub: https://github.com/rtomac/robotframework-selenium2library/downloads
.. _PyPI: http://pypi.python.org
.. _.pypirc file: http://docs.python.org/distutils/packageindex.html#the-pypirc-file
