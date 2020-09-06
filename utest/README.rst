Unit testing
============
Requirements
------------
Before running the test, install the dependencies::

    pip install -r requirements-dev.txt

Unit Tests
----------
Units tests are written by using the `pytest`_  framework.
Unit test can be executed by running::

    python utest/run.py

The utest directory contains everything needed to run SeleniumLibrary unit tests.
This includes:

- Unit test in `test` folder.
- Unit test runner: `run.py`

Unit test are executed using the interpreter which starts the `run.py` script.

ApprovalTests
-------------
For unit test, it is possible to use `ApprovalTests`_ framework. ApprovalTests
provides an easy and visual way to compare strings in unit tests. For more
details, please read `ApprovalTests`_ documentation and `ApprovalTests blog post`_.

The downside of ApprovalTests is that SeleniumLibrary is mainly developed
in Linux and therefore unit tests using ApprovalTests are skipped in Windows
OS. This needs to be done until ApprovalTests issue `#41`_ is fixed.
To skip tests, mark test as:
`@unittest.skipIf(WINDOWS, reason='ApprovalTest do not support different line feeds')`


.. _pytest: https://docs.pytest.org/en/latest/
.. _ApprovalTests: https://github.com/approvals/ApprovalTests.Python
.. _ApprovalTests blog post: http://blog.approvaltests.com/
.. _#41: https://github.com/approvals/ApprovalTests.Python/issues/41
