=====================
SeleniumLibrary 6.1.3
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.1.3 is a hotfix release
that fixes an issue with remote browsers when options are not provided.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.1.3

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.1.3 was released on Thursday October 12, 2023. SeleniumLibrary supports
Python 3.8+, Selenium 4.3+ and Robot Framework 4.1.3 or higher.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.3


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Remote browser fails when no options provided (`#1855`_)

  For several of the remote browsers we need to initialize the options if none are provided.
  In addition the deprecated and removed from selenium desired_capabilities have been removed
  from SeleniumLibrary v6.1.3.

Acknowledgements
================

- I want to thank Tero Lempiäinen for pointing out this issue (`#1855`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1855`_
      - bug
      - critical
      - Remote browser fails when no options provided

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.3>`__.

.. _#1855: https://github.com/robotframework/SeleniumLibrary/issues/1855
