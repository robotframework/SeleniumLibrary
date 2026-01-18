=====================
SeleniumLibrary 6.1.2
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.1.2 is a hotfix release
focused on bug fixes for setting configuration options when using a remote Edge
or Safari Browser.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.1.2

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.1.2 was released on Saturday September 9, 2023. SeleniumLibrary supports
Python 3.7+, Selenium 4.3+ and Robot Framework 4.1.3 or higher.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Missing "Options" setup in EDGE browser for remote url execution (`#1844`_, rc 1)

  The browser options if given within the ``Open Browser`` or `Create WebDriver`` keyword were not being
  passed to either a remote Edge or remote Safari browser. This has been fixed within this release.

Acknowledgements
================

- I want to thank @ap0087105 for pointing out the library was missing "Options" setup within Edge and
  Safari remote url execution (`#1844`_, rc 1)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1844`_
      - bug
      - high
      - Missing "Options" setup in EDGE browser for remote url execution
      - rc 1

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.2>`__.

.. _#1844: https://github.com/robotframework/SeleniumLibrary/issues/1844
