=====================
SeleniumLibrary 5.0.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.0.0 is a new release with
chained locators support and improving autocompletion from Python IDE. Support
for Python 2 ja Jython is dropped in this release.

All issues targeted for SeleniumLibrary v5.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.0.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.0.0 was released on Saturday January 30, 2021. SeleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.1.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Selenium 4 has deprecated all find_element_by_* methods, therefore move using find_element(By.*) (`#1575`_, alpha 1)
--------------------------------------------------------------------------------------------------------------------
SeleniumLibrary now uses find_element(By.*) methods to locate elements, instead of the deprecated find_element_by_*
methods. This will result less warning messages in the outputs.

Many thanks for Badari to providing PR to make the change.

Support of list of locator-strings to use different strategies and WebElement as entry point. (`#1512`_, alpha 1)
-----------------------------------------------------------------------------------------------------------------
SeleniumLibrary offers support chain different types locators together. Example: Get WebElements xpath://a >> css:.foo
is not possible.

There is small change the separator string is a backwards incompatible change, in that case, locator can be
provided as a list.

Many thanks for Badari for providing the initial PR for implementing the chained locators.

Implement better IDE support for SeleniumLibrary (`#1588`_, alpha 1)
--------------------------------------------------------------------
SeleniumLibrary now provides Python `stub file`_/.pyi file for the SeleniumLibrary instance. This
offers better automatic completions from Python IDE.

Backwards incompatible changes
==============================

Support of list of locator-strings to use different strategies and WebElement as entry point. (`#1512`_, alpha 1)
-----------------------------------------------------------------------------------------------------------------
SeleniumLibrary offers support chain different types locators together. Example: Get WebElements xpath://a >> css:.foo
is not possible.

There is small change the separator string is a backwards incompatible change, in that case, locator can be
provided as a list.

Many thanks for Badari for providing the initial PR for implementing the chained locators.

Implement better IDE support for SeleniumLibrary (`#1588`_, alpha 1)
--------------------------------------------------------------------
SeleniumLibrary now provides Python `stub file`_/.pyi file for the SeleniumLibrary instance. This
offers better automatic completions from Python IDE.

Remove deprecated keywords  (`#1655`_, alpha 3)
-----------------------------------------------
Select Window and Locator Should Match X Times have been removed.

Boolean arguments are converted by Robot Framework (`#1676`_, beta 1)
---------------------------------------------------------------------
Boolean argument handling is not anymore done by the SeleniumLibrary. Instead library
relies on the Robot Framework and type hints to perform conversion correctly.


Drop Python 2 and Jython support (`#1444`_) (`#1451`_)
------------------------------------------------------
Support for Python 2 is dropped in this release. This also means that Jython is not anymore supported.
Many thanks for hugovk for providing help in this task.

Acknowledgements
================

This release also contained nice enhancements from the community.

Drag And Drop does not work with event firing (`#1653`_)
--------------------------------------------------------
Ed Manlove fixed bug (which is actually Selenium bug), if Event Firing WebDriver is used,
all keywords that used Selenium Action Chains did fail. Now there is a workaround and
keywords do work normally with Event Firing WebDriver.

Fix typo in locator documentation (`#1660`_)
--------------------------------------------
robco  fixed documentation bug int he locator documentation.

Support of list of locator-strings to use different strategies and WebElement as entry point. (`#1512`_)
--------------------------------------------------------------------------------------------------------
badari412 provided initial implementation and inspiration for the list of locator-strings implementation.

Fix README (`#1665`_)
---------------------
I think someone did provide fix fow this, but I have lost track who that person was and I am sorry about that.
If you want your name to be mentioned, please send us a PR to fix this doc.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1444`_
      - enhancement
      - critical
      - Drop Python 2 support
    * - `#1451`_
      - enhancement
      - critical
      - Drop Jython support
    * - `#1575`_
      - enhancement
      - critical
      - Selenium 4 has deprecated all find_element_by_* methods, therefore move using find_element(By.*)
    * - `#1657`_
      - enhancement
      - critical
      - Add type hints to methods which are keywords
    * - `#1649`_
      - bug
      - high
      - Also add stub file to distribution
    * - `#1653`_
      - bug
      - high
      - Drag And Drop does not work with event firing
    * - `#1660`_
      - bug
      - high
      - Fix typo in locator documentation
    * - `#1512`_
      - enhancement
      - high
      - Support of list of locator-strings to use different strategies and WebElement as entry point.
    * - `#1588`_
      - enhancement
      - high
      - Implement better IDE support for SeleniumLibrary
    * - `#1655`_
      - enhancement
      - high
      - Remove deprecated keywords 
    * - `#1676`_
      - enhancement
      - high
      - Boolean arguments are converted by Robot Framework
    * - `#1021`_
      - bug
      - medium
      - Some keywords do not work if text argument is not string
    * - `#1665`_
      - bug
      - medium
      - Fix README
    * - `#1652`_
      - enhancement
      - medium
      - Add support for xpath starting with ((//

Altogether 14 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.0.0>`__.

.. _#1444: https://github.com/robotframework/SeleniumLibrary/issues/1444
.. _#1451: https://github.com/robotframework/SeleniumLibrary/issues/1451
.. _#1575: https://github.com/robotframework/SeleniumLibrary/issues/1575
.. _#1657: https://github.com/robotframework/SeleniumLibrary/issues/1657
.. _#1649: https://github.com/robotframework/SeleniumLibrary/issues/1649
.. _#1653: https://github.com/robotframework/SeleniumLibrary/issues/1653
.. _#1660: https://github.com/robotframework/SeleniumLibrary/issues/1660
.. _#1512: https://github.com/robotframework/SeleniumLibrary/issues/1512
.. _#1588: https://github.com/robotframework/SeleniumLibrary/issues/1588
.. _#1655: https://github.com/robotframework/SeleniumLibrary/issues/1655
.. _#1676: https://github.com/robotframework/SeleniumLibrary/issues/1676
.. _#1021: https://github.com/robotframework/SeleniumLibrary/issues/1021
.. _#1665: https://github.com/robotframework/SeleniumLibrary/issues/1665
.. _#1652: https://github.com/robotframework/SeleniumLibrary/issues/1652
