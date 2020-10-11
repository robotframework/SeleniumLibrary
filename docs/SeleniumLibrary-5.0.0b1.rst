=======================
SeleniumLibrary 5.0.0b1
=======================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.0.0b1 is a new release with
chained locators support and improving autocompletion from Python IDE. Support
for Python 2 ja Jython is dropped in this release. Compared to Alpha 3, this release
relies more to Robot Framework to perform type conversions.

All issues targeted for SeleniumLibrary v5.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.0.0b1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.0.0b1 was released on Sunday October 11, 2020. SeleniumLibrary supports
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

Remove deprecated keywords  (`#1655`_, alpha 3)
-----------------------------------------------
Select Window and Locator Should Match X Times have been removed.

Boolean arguments are converted by Robot Framework (`#1676`_, beta 1)
---------------------------------------------------------------------
Boolean argument handling is not anymore done by the SeleniumLibrary. Instead library
relies on the Robot Framework and type hints to perform conversion correctly.

.. _stub file: https://www.python.org/dev/peps/pep-0484/#stub-files


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1444`_
      - enhancement
      - critical
      - Drop Python 2 support
      - alpha 1
    * - `#1451`_
      - enhancement
      - critical
      - Drop Jython support
      - alpha 1
    * - `#1575`_
      - enhancement
      - critical
      - Selenium 4 has deprecated all find_element_by_* methods, therefore move using find_element(By.*)
      - alpha 1
    * - `#1657`_
      - enhancement
      - critical
      - Add type hints to methods which are keywords
      - alpha 3
    * - `#1649`_
      - bug
      - high
      - Also add stub file to distribution
      - alpha 2
    * - `#1512`_
      - enhancement
      - high
      - Support of list of locator-strings to use different strategies and WebElement as entry point.
      - alpha 1
    * - `#1588`_
      - enhancement
      - high
      - Implement better IDE support for SeleniumLibrary
      - alpha 1
    * - `#1655`_
      - enhancement
      - high
      - Remove deprecated keywords 
      - alpha 3
    * - `#1676`_
      - enhancement
      - high
      - Boolean arguments are converted by Robot Framework
      - beta 1
    * - `#1021`_
      - bug
      - medium
      - Some keywords do not work if text argument is not string
      - alpha 3

Altogether 10 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.0.0>`__.

.. _#1444: https://github.com/robotframework/SeleniumLibrary/issues/1444
.. _#1451: https://github.com/robotframework/SeleniumLibrary/issues/1451
.. _#1575: https://github.com/robotframework/SeleniumLibrary/issues/1575
.. _#1657: https://github.com/robotframework/SeleniumLibrary/issues/1657
.. _#1649: https://github.com/robotframework/SeleniumLibrary/issues/1649
.. _#1512: https://github.com/robotframework/SeleniumLibrary/issues/1512
.. _#1588: https://github.com/robotframework/SeleniumLibrary/issues/1588
.. _#1655: https://github.com/robotframework/SeleniumLibrary/issues/1655
.. _#1676: https://github.com/robotframework/SeleniumLibrary/issues/1676
.. _#1021: https://github.com/robotframework/SeleniumLibrary/issues/1021
