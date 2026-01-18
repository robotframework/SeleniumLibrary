========================
SeleniumLibrary 6.0.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.0.0rc1 is a new release with enhancements to locators and bug fixes on how run on failure functionality is executed. Starting with version 6.0 SeleniumLibrary requires Selenium 4.0+. If you wish to use Selenium version 3.x you must use SeleniumLibrary version 5 or prior.

All issues targeted for SeleniumLibrary v6.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.0.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.0.0rc1 was released on Friday December 31, 2021. SeleniumLibrary supports
Python 3.7+, Selenium 4.0.0+ and Robot Framework 3.2.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.0.0


.. contents::
   :depth: 2
   :local:

Most important bug fixes
========================

Improve run on failure functionality (`#1716`_)
-------------------------------------------------
When run on failure keyword is capture page screenshot
execute is method and not as keyword. This change was made
due to a conflict when another library has a keyword named
capture page screenshot. In that case Robot Framework does
the choice based on the library search order and may select
the other libraries keyword.

This is a backwards incompatable change. Most user should
not see any difference expect for how the log is displayed.
For more information see `#1715`_.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1474`_
      - enhancement
      - medium
      - Support 'data-' attributes as locators
    * - `#1716`_
      - bug
      - medium
      - Improve run on failure functionality

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.0.0>`__.

