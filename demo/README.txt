SeleniumLibrary Demo 
====================

Introduction
------------

This directory contains an easily executable demo test suite for Robot
Framework using SeleniumLibrary. ``httpserver`` directory contains a simple
standalone HTTP server and even simpler application that is used as a system
under test in the demo. Actual test case files are under ``login_tests``
directory. A script for running the tests is also provided.

Running The Demo 
----------------

The demo needs to be run from command line. You must specify which test case
file is to be executed by giving the file as an argument. To run all the 
tests, the directory can be given as an argument. For example::

    python rundemo.py login_tests

executes all test cases and::

    python rundemo.py login_tests/simple_login.html

executes only the specified test case file.

By default, the tests cases are run using Firefox browser, this can be changed
by using variable `browser` from command line, for example::

    python rundemo.py --variable browser:*iexplore

runs the test cases using Internet Explorer. Please refer to library
documentation for a list of supported browsers.

It is possible to add a delay between each keyword by giving a non-zero value
for variable `delay` from command line, for example::

  python rundemo.py --variable delay:2 login_tests



Structure of the test cases
---------------------------

A few useful features of Robot Framework are demonstrated through these test
cases. First, the test cases `Valid Login`, `Higher level valid login`, `Even
higher level valid login` and `Highest level valid login` show how to use user
keywords to create essentially same test case in more abstract terms. Second,
the test cases in `invalid_login.html` demonstrate the use of keywords to do
data-driven testing.

