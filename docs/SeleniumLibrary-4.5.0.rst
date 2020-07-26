=====================
SeleniumLibrary 4.5.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.5.0 is a new release with
providing better supporting for Robot Framework 3.2 and the enhancement in the
dynamic library API. There are also other enhancement and fixes in the release.

All issues targeted for SeleniumLibrary v4.5.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.5.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.5.0 was released on Sunday July 26, 2020. SeleniumLibrary supports
Python 2.7 and 3.6+, Selenium 3.141.0+ and Robot Framework 3.1.2+. This is the last release
which contains new development for Python 2.7 and users should migrate to Python 3.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update to latest PythonLIbCore because it does not work with SeleniumTestability plugin  (`#1577`_, rc 2)
---------------------------------------------------------------------------------------------------------
`PythonLibCore`_ did contain a bug which prevented SeleniumLibrary to work SeleniumTestability plugin.
This is now fixed in PythonLibCore side and SeleniumLibrary contains updated PythonLibCore

Update PythonLibCore (`#1564`_, rc 1)
-------------------------------------
SeleniumLibrary relies on `PythonLibCore`_ to handle Robot Framework dynamic library API requirements.
The PythonLibCore has been enhanced to support Robot Framework 3.2 dynamic library API changes. This
provides automatic argument type conversion and better support for the language server protocol.

Raise minimum required Robot Framework to 3.1 (`#1494`_, rc 1)
--------------------------------------------------------------
This was already announced in the previous releases, but it was not enforced during the installation time.
Now this is enforced in installation time.

Use PythonLibCore official 2.0.2 release.  (`#1585`_, rc 3)
-----------------------------------------------------------
This release uses official 2.0.2 release from PythonLibCore.

Acknowledgements
================

Small error in 'Get Cookie' keyword documentation (`#1555`_, rc 1)
------------------------------------------------------------------
Many thanks to Ryan Mori for fixing the bug in the Get Cookie keyword documentation.

"Wait Until Location Is" error message reads "Location did not is <url> in <wait time>" (`#1559`_, rc 1)
--------------------------------------------------------------------------------------------------------
Many thanks to testventure for fixing wait until location is error message.

Wait Until Page Contains add option Limit (`#1543`_, rc 1)
----------------------------------------------------------
Many thanks to Marcin Koperski for adding limit argument to Wait Until Page Does Not Contain Element
and Wait Until Page Contains Element keywords.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1614`_
      - bug
      - high
      - Overwriding the EMBED in the screenshot keywords creates EMBED folder
    * - `#1617`_
      - bug
      - high
      - Choose File not working when running against a remote machine.
    * - `#1612`_
      - enhancement
      - high
      - Update PythonLibCore to 2.1.0
    * - `#1601`_
      - bug
      - medium
      - Fix typo in extending documentation
    * - `#1604`_
      - bug
      - medium
      - Fix doc bugs in page should not * keywords. 

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.5.0>`__.

.. _#1614: https://github.com/robotframework/SeleniumLibrary/issues/1614
.. _#1617: https://github.com/robotframework/SeleniumLibrary/issues/1617
.. _#1612: https://github.com/robotframework/SeleniumLibrary/issues/1612
.. _#1601: https://github.com/robotframework/SeleniumLibrary/issues/1601
.. _#1604: https://github.com/robotframework/SeleniumLibrary/issues/1604
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore