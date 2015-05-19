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
- A copy of statuschecker.py for checking logged messages after the
  execution, which requires the tests to run with log level DEBUG

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


Debugging Selenium2Library
--------------------------

In the course of debugging the Selenium2Library one might need to set a
breakpoint using `pdb`_. Since Robot Framework hijacks the console output
one should use the folowing code to redirect output back to stdout for
debugging purposes.

        import pdb,sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()


Testing Third-Party Packages
----------------------------

Sometimes in the process of developing and testing Selenium2Library
one needs to determine whether or not an issue is within Selenium2Library
or if it lies within a third-party package like Selenium or Robot Framework.
Here are some hints for writing quick, short unit tests against Selenium
and Robot Framework.

Testing Selenium
~~~~~~~~~~~~~~~~
First create a test directory and create an isolated Python environment
using virtualenv::

	~$ mkdir se-bug
	~$ cd se-bug
	~/se-bug$ virtualenv -p /usr/bin/python2.6 --no-site-packages clean-python26-env

Activate the virtual environment::

	 ~/se-bug$ source clean-python26-env/bin/activate

Install the version of Selenium for which you wish to test. In the following
case we are going to check Selenium version 2.25.0.

	(clean-python26-env) ~/se-bug$ easy_install selenium==2.25.0

Create a test file, in this case ~/se-bug/testExeJS.py::

	import unittest
	from selenium import webdriver
	
	class ExecuteJavascriptTestCase(unittest.TestCase):
	
	    def setUp(self):
	        self.driver = webdriver.Firefox()
	
	    def test_exe_javascript(self):
	        driver = self.driver
	        driver.get("http://www.google.com")
	        url = driver.execute_script("return [ document.location ];")
	        print('Finished')
		self.assertEqual(url[0]['href'], u"http://www.google.com/")
	
	    def tearDown(self):
	        self.driver.close()
	    
	if __name__ == "__main__":
	    unittest.main()

Breaking down this example test case we see in the setUp and tearDown
methods we initiate and close the Firefox webdriver, respectively.
In the one test, text_exe_javascript, we perform steps to verify or
disprove the issue we are experiencing is with Selenium only. (In
`this case`_ the browser was hanging after the execute_script call and
not returning; thus I printed 'Finished' to help show where the test
progressed to.)

An important part of the above test case, and all unit tests, is the
line "self.assertEqual(...". This is one example of the method's
available to check for errors or failures. For example, you can check
for trueness or falseness of a stament by using assertTrue() and
assertFalse(). Or you can for inclusiveness and exclussiveness by using
assertIn() and assertNotIn(), respectively. For more information about
unittest see `Python's unittest documentation`_. The last two lines
allow this test to be run from the command line.

To run the unittest type::

    	(clean-python26-env) ~/se-bug$ python testExeJS.py

In this example I removed the troubled selenium version and reinstalled a
previous version, re-running the test case to verfiy selenium was the
problem and not Selenium2Library::

	(clean-python26-env) ~/se-bug$ rm -Rf clean-python26-env/lib/python2.6/site-packages/selenium-2.25.0-py2.6.egg
	(clean-python26-env) ~/se-bug$ easy_install selenium==2.24.0
	(clean-python26-env) ~/se-bug$ python testExeJS.py
	Finished
	.
	----------------------------------------------------------------------
	Ran 1 test in 6.198s
	
	OK
	(clean-python26-env) ~/se-bug$

If you discover an issue with Selenium it is helpful to `report it`_ to
the Selenium developers.


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


.. _pdb: http://docs.python.org/2/library/pdb.html
.. _downloads section on GitHub: https://github.com/rtomac/robotframework-selenium2library/downloads
.. _PyPI: http://pypi.python.org
.. _.pypirc file: http://docs.python.org/distutils/packageindex.html#the-pypirc-file
.. _this case: http://code.google.com/p/selenium/issues/detail?id=4375
.. _report it: http://code.google.com/p/selenium/issues/list
.. _Python's unittest documentation: http://docs.python.org/library/unittest.html
