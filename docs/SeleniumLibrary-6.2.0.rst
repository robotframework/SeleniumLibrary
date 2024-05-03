=====================
SeleniumLibrary 6.2.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.2.0 is a new release with
compatibility fixes for recent selenium versions and some bug fixes.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.2.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.2.0 was released on Friday November 24, 2023. SeleniumLibrary supports
Python 3.8 through 3.11, Selenium 4.12.0 through 4.15.2 and
Robot Framework 5.0.1 and 6.1.1.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Remove deprecated headless option for chrome and firefox. (`#1858`_)
  If one specified either `headlesschrome` or `headlessfirefox` as the browser within the
  Open Browser keyword, then the library would handle setting this option with the underlying
  Selenium driver. But the methods to do so were depracted and then removed in Selenium
  v4.13.0. Thus one was not getting a headless browser in these instances. This resolves that
  issue.

- Resolve issue with service log_path now log_output. (`#1870`_)
  Selenium changed the arguments for the service log within v4.13.0. This change allows for a
  seamless usage across versions before and after v4.13.0.

- Execute JavaScript converts arguments to strings with robot==6.1 (`#1843`_)
  If any ARGUMENTS were passed into either the `Execute Javascript` or `Execute Async Javascript`
  then they were converted to strings even if they were of some other type. This has been
  corrected within this release.

Acknowledgements
================

I want to thank the following for helping to get out this release,

- `René Rohner <https://github.com/Snooz82>`_ for pointing out that Create Webdriver had a
  mutable default value (`#1817`_)
- `Kieran Trautwein <https://github.com/trauty-is-me>`_ for resolving the issue with
  deprecated headless option for chrome and firefox. (`#1858`_)
- `Nicholas Bollweg <https://github.com/bollwyvl>`_ for assisting in resolving the issue
  with service log_path now log_output. (`#1870`_)
- `Igor Kozyrenko <https://github.com/ikseek>`_ for reporting the argument issue with Execute
  JavaScript and `René Rohner <https://github.com/Snooz82>`_for resolving it. (`#1843`_)
- `Robin Matz <https://github.com/robinmatz>`_ for improving the documentation on page load
  timeout (`#1821`_)
- `Dor Blayzer <https://github.com/Dor-bl>`_ for reporting and fixing the SeleniumLibrary CI badge. ()

and **Yuri Verweij, Lisa Crispin, and Tatu Aalto**.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1817`_
      - bug
      - critical
      - Create Webdriver has mutable default value
    * - `#1858`_
      - bug
      - critical
      - Remove deprecated headless option for chrome and firefox.
    * - `#1870`_
      - bug
      - critical
      - Resolve issue with service log_path now log_output.
    * - `#1843`_
      - bug
      - high
      - Execute JavaScript converts arguments to strings with robot==6.1
    * - `#1821`_
      - enhancement
      - medium
      - Improve documentation on page load timeout
    * - `#1872`_
      - ---
      - medium
      - fix: Selenium CI badge show wrong status

Altogether 6 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.2.0>`__.

.. _#1817: https://github.com/robotframework/SeleniumLibrary/issues/1817
.. _#1858: https://github.com/robotframework/SeleniumLibrary/issues/1858
.. _#1870: https://github.com/robotframework/SeleniumLibrary/issues/1870
.. _#1843: https://github.com/robotframework/SeleniumLibrary/issues/1843
.. _#1821: https://github.com/robotframework/SeleniumLibrary/issues/1821
.. _#1872: https://github.com/robotframework/SeleniumLibrary/issues/1872
