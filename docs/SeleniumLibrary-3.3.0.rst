=====================
SeleniumLibrary 3.3.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.3.0 is a new release with
new Press Keys keyword which has clean support for `Selenium Keys`_,
allows to capture picture from a single element and many other enhancements and
bug fixes.

All issues targeted for SeleniumLibrary v3.3.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.3.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.3.0 was released on Monday December 24, 2018. SeleniumLibrary supports
Python 2.7 and 3.4+, Selenium 3.4+ (Although the supported Selenium version depends on
the use browser version) and Robot Framework 2.9.2, 3.0.4 and 3.1.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _Selenium Keys: https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

New `Press Keys` keyword with clean support for special keys (`#1250`_)
-----------------------------------------------------------------------
New Press Keys provides clean support for Selenium Keys and it is not anymore
needed to provide the ASCII code of the key. With one keyword it is possible
to press multiple keys at the same time and send multiple key combinations
by using one keyword.

The existing Press Key keyword is silently deprecated and user are
encouraged to migrate to the new Press Keys keyword.

Wait... keywords should not fail StaleElementReferenceException (`#1270`_)
--------------------------------------------------------------------------
The Wait... keywords can fail with StaleElementReferenceException because
in between finding the element and doing action with the element (like
checking is the element displayed) the DOM may change. Finding the element
and doing something with the element are always two different Selenium
API calls, even when doing it Python way: self.find_element(locator).text
and therefore there is always small delay between the calls.

There are various reasons why the DOM may change, but the Wait ... keywords
should not fail, in middle of the waiting, if Selenium raises
StaleElementReferenceException. The Wait ... keywords have been changed
to suppress the StaleElementReferenceException and log it.

This change is also backwards incompatible if someone has relied on the
old functionality.

Get Window Titles fails with a unicode encode error for certain titles. (`#1252`_)
----------------------------------------------------------------------------------
SeleniumLibrary 3.0 introduced a bug, if the title contained non ascii character, listing
the window titles would fail. This is now fixed.

Document that Set selenium timeout also affects Execute async javascript (`#1267`_)
-----------------------------------------------------------------------------------
It was not properly documented that the Set Selenium Timeout keyword or
timeout argument in the library import affects also Execute Async Javascript
keyword.

Backwards incompatible changes
==============================

Open Browser keyword in 3.2 (and most likely 3.1 too) does not work with chromium-browser, but 3.0 works with chromium-browser.  (`#1243`_)
-------------------------------------------------------------------------------------------------------------------------------------------
In the SeleniumLibrary 3.1 release `Open Browser` keyword was changed to always add
default desired capabilities. This caused a problem with chromium-browser and
prevented the browser to open. The functionality is now changed that SeleniumLibrary
does not set the default desired capabilities. Instead SeleniumLibrary will only set the
desired capabilities defined by the user, or lest's the Selenium to set the default
desired capabilities.

Drop Robot Framework 2.8 support in SeleniumLibrary 3.3.0. (`#1197`_)
---------------------------------------------------------------------
Robot Framework 2.8 is not anymore supported by the SeleniumLibrary.

The next major release will also drop support Robot Framework 2.9.


Change loglevel to TRACE in keywords which log html source (`#1259`_)
---------------------------------------------------------------------
SeleniumLibrary had many keywords, which would log the html source
if they would fail. By default that logging was done in INFO level.
But with the current dynamic applications, logging the html source
provides little or none value for the users and it can increase the
log.html size drastically. Therefore it was decided to change the
default logging level to TRACE.



Deprecated features
===================

Deprecate support for the phantomjs  (`#1251`_)
-----------------------------------------------
Support for phantomjs has been long deprecated in the Selenium side. Now
it is also deprecated in the SeleniumLibrary side. Users should migrate
their tests to use headless Chrome or Firefox.

Acknowledgements
================

Also there has been many contributions from the community. Special thanks
to all that provided an contribution to the project. Here is a list of
contributions which have made in to the this release.

I would like to remind that providing PR is not the only way to contribute.
There has been lot of issues raised in the project issue tracker and
feedback has been provided in the user group and in slack. I am grateful
from all the feedback.


Typo in Location Should Be documentation (`#1215`_)
---------------------------------------------------
Cyril Bonté provided PR to fix a bug in the documentation.

Add keyword to mimic add blocker functionality (`#1239`_)
---------------------------------------------------------
SergiuTudos provided a PR, which add's a keyword to mimic
add blocker functionality.

`Get Cookies` should support returning cookies as objects and have better logging (`#979`_)
-------------------------------------------------------------------------------------------
Jani Mikkonen provided a PR to enhanced the Get Cookies keyword, with
as_dict argument. Now it is possible configure keyword to return cookies
in string and dictionary format.

Change loglevel to TRACE in keywords which log html source (`#1259`_)
---------------------------------------------------------------------
Joao Coelho provided a PR to change the loglevel from INFO to TRACE
by default.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1243`_
      - bug
      - critical
      - Open Browser keyword in 3.2 (and most likely 3.1 too) does not work with chromium-browser, but 3.0 works with chromium-browser. 
    * - `#1252`_
      - bug
      - high
      - Get Window Titles fails with a unicode encode error for certain titles.
    * - `#1267`_
      - bug
      - high
      - Document that Set selenium timeout also affects Execute async javascript
    * - `#1197`_
      - enhancement
      - high
      - Drop Robot Framework 2.8 support in SeleniumLibrary 3.3.0.
    * - `#1250`_
      - enhancement
      - high
      - New `Press Keys` keyword with clean support for special keys
    * - `#1251`_
      - enhancement
      - high
      - Deprecate support for the phantomjs 
    * - `#1270`_
      - enhancement
      - high
      - Wait... keywords should not fail StaleElementReferenceException
    * - `#1215`_
      - bug
      - medium
      - Typo in Location Should Be documentation
    * - `#1181`_
      - enhancement
      - medium
      - Capture Elemen picture
    * - `#1208`_
      - enhancement
      - medium
      - Consistency reasons add `modifier` argument for all click keywords. 
    * - `#1239`_
      - enhancement
      - medium
      - Add keyword to mimic add blocker functionality
    * - `#1265`_
      - enhancement
      - medium
      - Update PythonLibcore to latest in master
    * - `#979`_
      - enhancement
      - medium
      - `Get Cookies` should support returning cookies as objects and have better logging
    * - `#1207`_
      - bug
      - low
      - Fix typo in README.rst
    * - `#1235`_
      - enhancement
      - low
      - Add ESC to Click Element modifier alias
    * - `#1259`_
      - enhancement
      - low
      - Change loglevel to TRACE in keywords which log html source

Altogether 16 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.3.0>`__.

.. _#1243: https://github.com/robotframework/SeleniumLibrary/issues/1243
.. _#1252: https://github.com/robotframework/SeleniumLibrary/issues/1252
.. _#1267: https://github.com/robotframework/SeleniumLibrary/issues/1267
.. _#1197: https://github.com/robotframework/SeleniumLibrary/issues/1197
.. _#1250: https://github.com/robotframework/SeleniumLibrary/issues/1250
.. _#1251: https://github.com/robotframework/SeleniumLibrary/issues/1251
.. _#1270: https://github.com/robotframework/SeleniumLibrary/issues/1270
.. _#1215: https://github.com/robotframework/SeleniumLibrary/issues/1215
.. _#1181: https://github.com/robotframework/SeleniumLibrary/issues/1181
.. _#1208: https://github.com/robotframework/SeleniumLibrary/issues/1208
.. _#1239: https://github.com/robotframework/SeleniumLibrary/issues/1239
.. _#1265: https://github.com/robotframework/SeleniumLibrary/issues/1265
.. _#979: https://github.com/robotframework/SeleniumLibrary/issues/979
.. _#1207: https://github.com/robotframework/SeleniumLibrary/issues/1207
.. _#1235: https://github.com/robotframework/SeleniumLibrary/issues/1235
.. _#1259: https://github.com/robotframework/SeleniumLibrary/issues/1259
