=====================
SeleniumLibrary 6.7.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.7.1 is a new release with
one minor change - downgrade the requirements on the click dependency.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.7.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.7.1 was released on Wednesday February 26, 2025. SeleniumLibrary supports
Python 3.8 through 3.13, Selenium 4.24.0 through 4.27.1 and
Robot Framework 6.1.1 and 7.1.1.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.7.1


.. contents::
   :depth: 2
   :local:

Changes
=======

- Downgrade the requirement on click to `click>=8.0`. (`#1932`_)

Acknowledgements
================

I want to thank Oliver Boehmer for raising up this issue and Pekka Klärck and Tatu Aalto for
consultation and review. (`#1932`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1932`_
      - ---
      - medium
      - Downgrade requirements on click to `click>=8.0`

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.7.1>`__.

.. _#1932: https://github.com/robotframework/SeleniumLibrary/issues/1932
