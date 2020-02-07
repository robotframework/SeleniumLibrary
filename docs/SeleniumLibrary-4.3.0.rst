=====================
SeleniumLibrary 4.3.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.3.0 is a new release with
fixing Open Browser keyword for Ie browser.

All issues targeted for SeleniumLibrary v4.3.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.3.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.3.0 was released on Friday February 7, 2020. SeleniumLibrary supports
Python 2.7 and 3.5+, Selenium 3.141.0 and Robot Framework 3.1.2. This is last release which
contains new development for Python 2.7 and users should migrate to Python 3.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Opening IE browser is not possible in SeleniumLibrary 4.2.0 (`#1548`_, rc 1)
----------------------------------------------------------------------------
Open Browser keyword had bug which prevented using IE browser. With IE browser
SeleniumLibrary tried to use wrong browser driver executable, geckodriver, instead
of IEDriverServer.exe.

Acknowledgements
================

Add Wait Until Location Does Not Contain and Wait Until Location Is Not keywords.  (`#1544`_, rc 1)
---------------------------------------------------------------------------------------------------
Many thanks to acaovilla for implementing Wait Until Location Does Not Contain and
Wait Until Location Is Not keywords for SeleniumLibrary.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1548`_
      - bug
      - critical
      - Opening IE browser is not possible in SeleniumLibrary 4.2.0
    * - `#1544`_
      - enhancement
      - medium
      - Add Wait Until Location Does Not Contain and Wait Until Location Is Not keywords. 

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.3.0>`__.

.. _#1548: https://github.com/robotframework/SeleniumLibrary/issues/1548
.. _#1544: https://github.com/robotframework/SeleniumLibrary/issues/1544
