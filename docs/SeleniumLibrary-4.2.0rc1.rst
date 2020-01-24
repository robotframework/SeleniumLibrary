========================
SeleniumLibrary 4.2.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.2.0rc1 is a new pre-release with
embedding screenshot to log.html and possibility add executable_path in the Open
Browser keyword. Also the Open Browser options argument supports defining complex
Python data object, like example dictionary. The most important fixes are in the
Press Keys keyword and when EventFiringWebDriver is used with WebElements as
locators.

All issues targeted for SeleniumLibrary v4.2.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.2.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.2.0rc1 was released on Thursday January 25, 2020. SeleniumLibrary supports
Python 2.7 and 3.5+, Selenium 3.141.0 and Robot Framework 3.1.2. This is last release which
contains new development for Python 2.7 and users should migrate to Python 3.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Fix Press Keys to support multiple key pressing  (`#1489`_, rc 1)
-----------------------------------------------------------------
Fixes Press Keys keyword to send multiple keys with in single keyword. When multiple keys where send
keyword did clear the previous keys from a input field. Now this issue is fixed.

When EventFiringWebDriver is enabled, elements from `Get WebElement(s)` keywords are not recoginized as instance of WebElement  (`#1538`_, rc 1)
------------------------------------------------------------------------------------------------------------------------------------------------
When EventFiringWebDriver is enabled, WebElements could not be used as locators in keywords. This raised and exception.
This problem is not fixed and using EventFiringWebDriver and WebElements as locators is possible.

Input Password keyword should also prevent password being visible from the Selenium logging (`#1454`_, rc 1)
------------------------------------------------------------------------------------------------------------
Input Password keyword  suppress the Selenium logging and the password is not anymore visible in the log.html
file. Please note that password is visible if Robot Framework logging reveals the variable content.

Open Browser keyword options argument does not support parsing complex structures. (`#1530`_, rc 1)
---------------------------------------------------------------------------------------------------
The options argument did not support dictionary objects or other complex Python object in the Open Browser
keyword. Example dictionaries where used to enable mobile emulation in the Chrome browser. After this
enhancement complex object are supported in the options argument.

Backwards incompatible changes
==============================

Raise minimum required Selenium version to 3.14 to ease support for Selenium 4 (`#1493`_, rc 1)
-----------------------------------------------------------------------------------------------
The minimum required Selenium version to 3.14 to ease support Selenium 4 in the future.


Drop Robot Framework 3.0.x support (`#1513`_, rc 1)
---------------------------------------------------
SeleniumLibrary supports Robot Framework 3.1.2 and older versions are not anymore supported.

Acknowledgements
================

When EventFiringWebDriver is enabled, elements from `Get WebElement(s)` keywords are not recoginized as instance of WebElement  (`#1538`_, rc 1)
-----------------------------------------------------------------------------------------------------------------------------------------------
Many thanks for rasjani providing PR to fix EventFiringWebDriver and using WebElements are locators.

If JavaScript code is long then Execute JavaScrpt will fail in windows (`#1524`_, rc 1)
---------------------------------------------------------------------------------------
Many thanks to lmartorella improving of the Execute JavaScript keyword to work better
in Windows OS.

'Handle Alert' keyword treats all exceptions as timeout (`#1500`_, rc 1)
------------------------------------------------------------------------
Many thanks to Zeckie improving error message in the Handle Alert keyword.

Close Browser does not delete alias (`#1416`_, rc 1)
----------------------------------------------------
Many thanks to anton264 improving closing browser functionality so that browser alias is deleted.

add ability of embedding screenshots as base64 encoded images in the ... (`#1497`_, rc 1)
-----------------------------------------------------------------------------------------
Many thanks to bitcoder for enabling embedding screenshot in to the log.html file.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1493`_
      - enhancement
      - critical
      - Raise minimum required Selenium version to 3.14 to ease support for Selenium 4
      - rc 1
    * - `#1489`_
      - bug
      - high
      - Fix Press Keys to support multiple key pressing 
      - rc 1
    * - `#1538`_
      - bug
      - high
      - When EventFiringWebDriver is enabled, elements from `Get WebElement(s)` keywords are not recoginized as instance of WebElement 
      - rc 1
    * - `#1454`_
      - enhancement
      - high
      - Input Password keyword should also prevent password being visible from the Selenium logging
      - rc 1
    * - `#1513`_
      - enhancement
      - high
      - Drop Robot Framework 3.0.x support
      - rc 1
    * - `#1530`_
      - enhancement
      - high
      - Open Browser keyword options argument does not support parsing complex structures.
      - rc 1
    * - `#1496`_
      - bug
      - medium
      - Fix Create WebDriver examples 
      - rc 1
    * - `#1524`_
      - bug
      - medium
      - If JavaScript code is long then Execute JavaScrpt will fail in windows
      - rc 1
    * - `#1473`_
      - enhancement
      - medium
      - Open Browser keyword and Selenium options with Windows path needs double escaping
      - rc 1
    * - `#1483`_
      - enhancement
      - medium
      - add support to embed screenshots in reports
      - rc 1
    * - `#1500`_
      - enhancement
      - medium
      - 'Handle Alert' keyword treats all exceptions as timeout
      - rc 1
    * - `#1536`_
      - enhancement
      - medium
      - Add possibility to configure executable_path in the Open Browser keywords
      - rc 1
    * - `#1416`_
      - bug
      - low
      - Close Browser does not delete alias
      - rc 1

Altogether 13 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.2.0>`__.

.. _#1493: https://github.com/robotframework/SeleniumLibrary/issues/1493
.. _#1489: https://github.com/robotframework/SeleniumLibrary/issues/1489
.. _#1538: https://github.com/robotframework/SeleniumLibrary/issues/1538
.. _#1454: https://github.com/robotframework/SeleniumLibrary/issues/1454
.. _#1513: https://github.com/robotframework/SeleniumLibrary/issues/1513
.. _#1530: https://github.com/robotframework/SeleniumLibrary/issues/1530
.. _#1496: https://github.com/robotframework/SeleniumLibrary/issues/1496
.. _#1524: https://github.com/robotframework/SeleniumLibrary/issues/1524
.. _#1473: https://github.com/robotframework/SeleniumLibrary/issues/1473
.. _#1483: https://github.com/robotframework/SeleniumLibrary/issues/1483
.. _#1500: https://github.com/robotframework/SeleniumLibrary/issues/1500
.. _#1536: https://github.com/robotframework/SeleniumLibrary/issues/1536
.. _#1416: https://github.com/robotframework/SeleniumLibrary/issues/1416
