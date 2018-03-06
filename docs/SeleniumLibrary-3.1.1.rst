=====================
SeleniumLibrary 3.1.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.1.1 is a new hotfix release with
fixing headless Chrome and Firefox support. Also it contains one new keyword
`Element Text Should Not Be`.


All issues targeted for SeleniumLibrary v3.1.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.1.1 was released on Tuesday March 6, 2018.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Selenium version 3.10.0 causes problems headless Chrome and Firefox support because SELENIUM_VERSION handles the version number as string. (`#1075`_)
-----------------------------------------------------------------------------------------------------------------------------------------------------
Due a bug in handling the Selenium version as string, inside of a named tuple, caused determination of the
Selenium version to work incorrectly. This is because we check, is the minor version bigger than 8. If it is,
then we allow users to launch Firefox and Chrome in headless mode. But because comparison was made as strings,
the comparison started work incorrectly when Selenium reached version 3.10.0 because "8" > "10". This
is now fixed and version is converted as number inside of the named tuple.

Acknowledgements
================

Big thanks to rubygeek for creating PR for the `Element Text Should Not Be` keyword.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1075`_
      - bug
      - critical
      - Selenium version 3.10.0 causes problems headless Chrome and Firefox support because SELENIUM_VERSION handles the version number as string.
    * - `#1065`_
      - enhancement
      - medium
      - Create new keyword "Element Text Should Not Be"

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.1.1>`__.

.. _#1075: https://github.com/robotframework/SeleniumLibrary/issues/1075
.. _#1065: https://github.com/robotframework/SeleniumLibrary/issues/1065
