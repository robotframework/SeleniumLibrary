Unit testing
============
Requirements
------------
Before running the test, install the dependencies::

    pip install -r requirements-dev.txt

Unit Tests
----------
Units tests are written by using the Python default `unittest`_ framework.
Unit test can be executed by running::

    python utest/run.py

The utest directory contains everything needed to run SeleniumLibrary unit tests.
This includes:
 - Unit test in `test` folder.
 - Unit test runner: `run.py`

Unit test are executed using the interpreter which starts the `run.py` script.

.. _unittest: https://docs.python.org/3/library/unittest.html
