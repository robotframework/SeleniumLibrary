========================
SeleniumLibrary 4.4.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.4.0rc1 is a new release with
providing better supporting for Robot Framework 3.2 and the enhancement in the
dynamic library API. There are also other enhancement and fixes in the release.

All issues targeted for SeleniumLibrary v4.4.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.4.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.4.0rc1 was released on Saturday April 18, 2020. SeleniumLibrary supports
Python 2.7 and 3.6+, Selenium 3.141.0+ and Robot Framework 3.1.2+. This is, again, last release
which contains new development for Python 2.7 and users should migrate to Python 3.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Update PythonLibCore (`#1564`_, rc 1)
-------------------------------------
SeleniumLibrary relies on `PythonLibCore`_ to handle Robot Framework dynamic library API requirements.
The PythonLibCore has been enhanced to support Robot Framework 3.2 dynamic library API changes. This
provides automatic argument type conversion and better support for the language server protocol.

Raise minimum required Robot Framework to 3.1 (`#1494`_, rc 1)
--------------------------------------------------------------
This was already announced in the previous releases, but it was not enforced during the installation time.
Now this is enforced in installation time.

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
      - Added
    * - `#1494`_
      - enhancement
      - critical
      - Raise minimum required Robot Framework to 3.1
      - rc 1
    * - `#1564`_
      - enhancement
      - critical
      - Update PythonLibCore
      - rc 1
    * - `#1555`_
      - bug
      - medium
      - Small error in 'Get Cookie' keyword documentation
      - rc 1
    * - `#1559`_
      - bug
      - medium
      - "Wait Until Location Is" error message reads "Location did not is <url> in <wait time>"
      - rc 1
    * - `#1543`_
      - enhancement
      - medium
      - Wait Until Page Contains add option Limit
      - rc 1

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.4.0>`__.

.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _#1494: https://github.com/robotframework/SeleniumLibrary/issues/1494
.. _#1564: https://github.com/robotframework/SeleniumLibrary/issues/1564
.. _#1555: https://github.com/robotframework/SeleniumLibrary/issues/1555
.. _#1559: https://github.com/robotframework/SeleniumLibrary/issues/1559
.. _#1543: https://github.com/robotframework/SeleniumLibrary/issues/1543
