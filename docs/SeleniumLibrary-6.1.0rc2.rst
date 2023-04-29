========================
SeleniumLibrary 6.1.0rc2
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.1.0rc2 is a new release with
**UPDATE** enhancements and bug fixes. **ADD more intro stuff...**

All issues targeted for SeleniumLibrary v6.1.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.1.0rc2

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.1.0rc2 was released on Saturday April 29, 2023. SeleniumLibrary supports
Python 3.7+, Selenium 4.0+ and Robot Framework 4.1.3 or higher.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

**EXPLAIN** or remove these.

-  Add API to set page load timeout (`#1535`_)  (`#1754`_)
- Update webdrivertools.py (`#1698`_)
- Added clarifying information about timeouts (`#1740`_)
- Users can now modify ActionChains() duration. (`#1812`_)
- Remove deprecated opera support (`#1786`_)

Deprecated features
===================

**EXPLAIN** or remove these.

- Remove deprecated opera support (`#1786`_)
- fix `StringIO` import as it was removed in robot 5.0 (`#1753`_)
- Remove deprecated rebot option (`#1793`_)

Acknowledgements
================

**EXPLAIN** or remove these.

-  Add API to set page load timeout (`#1535`_)  (`#1754`_)
- Update webdrivertools.py (`#1698`_)
- Added clarifying information about timeouts (`#1740`_)
- Users can now modify ActionChains() duration. (`#1812`_)
- Remove deprecated opera support (`#1786`_)
- Microsoft edge webdriver (`#1795`_)
- RemoteDriverServerException was removed from Selenium (`#1804`_)
- Review workaround for slenium3 bug tests (`#1789`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1754`_
      - enhancement
      - critical
      -  Add API to set page load timeout (`#1535`_) 
    * - `#1698`_
      - enhancement
      - high
      - Update webdrivertools.py
    * - `#1740`_
      - enhancement
      - high
      - Added clarifying information about timeouts
    * - `#1812`_
      - enhancement
      - high
      - Users can now modify ActionChains() duration.
    * - `#1786`_
      - ---
      - high
      - Remove deprecated opera support
    * - `#1797`_
      - bug
      - medium
      - Fix windowns utest running
    * - `#1798`_
      - bug
      - medium
      - Use python interpreter that executed atest/run.py instead of python
    * - `#1795`_
      - enhancement
      - medium
      - Microsoft edge webdriver
    * - `#1804`_
      - ---
      - medium
      - RemoteDriverServerException was removed from Selenium
    * - `#1794`_
      - bug
      - low
      - Documentation timing
    * - `#1806`_
      - enhancement
      - low
      - Remove remote driver server exception
    * - `#1807`_
      - enhancement
      - low
      - Rf v5 v6
    * - `#1815`_
      - enhancement
      - low
      - Updated `Test Get Cookie Keyword Logging` with Samesite attribute
    * - `#1753`_
      - ---
      - low
      - fix `StringIO` import as it was removed in robot 5.0
    * - `#1793`_
      - ---
      - low
      - Remove deprecated rebot option
    * - `#1734`_
      - ---
      - ---
      - Update PLC to 3.0.0
    * - `#1785`_
      - ---
      - ---
      - Review Page Should Contain documentation
    * - `#1788`_
      - ---
      - ---
      - Acceptance tests: rebot option `--noncritical` is deprecated since RF 4
    * - `#1789`_
      - ---
      - ---
      - Review workaround for slenium3 bug tests
    * - `#1808`_
      - ---
      - ---
      - Fix tests on firefox

Altogether 20 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.0>`__.

.. _#1754: https://github.com/robotframework/SeleniumLibrary/issues/1754
.. _#1698: https://github.com/robotframework/SeleniumLibrary/issues/1698
.. _#1740: https://github.com/robotframework/SeleniumLibrary/issues/1740
.. _#1812: https://github.com/robotframework/SeleniumLibrary/issues/1812
.. _#1786: https://github.com/robotframework/SeleniumLibrary/issues/1786
.. _#1797: https://github.com/robotframework/SeleniumLibrary/issues/1797
.. _#1798: https://github.com/robotframework/SeleniumLibrary/issues/1798
.. _#1795: https://github.com/robotframework/SeleniumLibrary/issues/1795
.. _#1804: https://github.com/robotframework/SeleniumLibrary/issues/1804
.. _#1794: https://github.com/robotframework/SeleniumLibrary/issues/1794
.. _#1806: https://github.com/robotframework/SeleniumLibrary/issues/1806
.. _#1807: https://github.com/robotframework/SeleniumLibrary/issues/1807
.. _#1815: https://github.com/robotframework/SeleniumLibrary/issues/1815
.. _#1753: https://github.com/robotframework/SeleniumLibrary/issues/1753
.. _#1793: https://github.com/robotframework/SeleniumLibrary/issues/1793
.. _#1734: https://github.com/robotframework/SeleniumLibrary/issues/1734
.. _#1785: https://github.com/robotframework/SeleniumLibrary/issues/1785
.. _#1788: https://github.com/robotframework/SeleniumLibrary/issues/1788
.. _#1789: https://github.com/robotframework/SeleniumLibrary/issues/1789
.. _#1808: https://github.com/robotframework/SeleniumLibrary/issues/1808
