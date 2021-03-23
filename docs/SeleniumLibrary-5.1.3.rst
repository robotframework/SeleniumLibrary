=====================
SeleniumLibrary 5.1.3
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.1.3 is a new release with
bug fixes to Execute JavaScript and Execute Async JavaScript type hints with RF 4.0.

All issues targeted for SeleniumLibrary v5.1.3 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.1.3

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.1.3 was released on Tuesday March 23, 2021. seleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.2.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.3


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Execute JavaScript has wrong type definition (`#1711`_)
-------------------------------------------------------
Execute JavaScript had invalid type definition if argument
did contain WebElement. This is not fixed and WebElements can
be used as arguments. Many thanks for  Avatar Vincenzo Gasparo
for providing PR to fix the issue.

Same bug was also found in the Execute Async JavaScript keyword.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1711`_
      - bug
      - critical
      - Execute JavaScript has wrong type definition

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.3>`__.

.. _#1711: https://github.com/robotframework/SeleniumLibrary/issues/1711
