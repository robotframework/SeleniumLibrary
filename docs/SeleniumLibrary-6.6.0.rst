=====================
SeleniumLibrary 6.6.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.6.0 is a new release which adds
Python 3.12 support.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.6.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.6.0 was released on Friday September 6, 2024. SeleniumLibrary supports
Python 3.8 through 3.12, Selenium 4.21.0 through 4.24.0 and
Robot Framework 6.1.1 and 7.0.1.

*In addition this version of SeleniumLibrary has been tested against the upcoming Robot
Framework v7.1 release (using v7.1rc2) and was found compatible. We expect it to work
fine with the final release which should be coming out soon.*

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.6.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Support for Python 3.12 was added in this release. In addition we added Robot Framework 7.0.1
  while dropping 5.0.1 which did not officially support Python 3.12. In addition with the almost
  monthly releases of Selenium we have caught up testing against and supporting Selenium versions
  4.21.0, 4.22.0, 4.23.1, and 4.24.0. (`#1906`_)

Acknowledgements
================

- I want to thank grepwood, KotlinIsland, and Robin Mackaij for pushing support python 3.12 and
  Yuri, Tatu and Lassi for reviewing the changes. (`#1906`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1906`_
      - enhancement
      - high
      - Support python 3.12

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.6.0>`__.

.. _#1906: https://github.com/robotframework/SeleniumLibrary/issues/1906
