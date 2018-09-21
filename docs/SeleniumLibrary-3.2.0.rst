=====================
SeleniumLibrary 3.2.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.2.0 is a new release with
enhancements and bug fixes. Example JavaScript keywords now supports arguments
and Open Browser keyword provides support for headless Chrome and Firefox with
Selenium Grid.

All issues targeted for SeleniumLibrary v3.2.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.2.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.2.0 was released on Friday September 21, 2018.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.2.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

ElementFinder can't raise correct exception if locator contains characters like ö ä å  (`#1084`_)
-------------------------------------------------------------------------------------------------
If element was not found and locator example contained ö character, then incorrect exception was
raised by the library. This bug is now fixed and correct exception is not raised.

Headless Firefox and Chrome not working over selenium grid (`#1098`_)
---------------------------------------------------------------------
The Open Browser keyword supports headless Chrome and Firefox also when Selenium Grid is used.

Backwards incompatible changes
==============================

Remove Python 3.3 support from SeleniumLibrary (`#1141`_)
---------------------------------------------------------
Robot Framework 3.1 will drop support for Python 3.3 and therefore the SeleniumLibrary 3.2 also
drops support for Python 3.3. SeleniumLibrary supports Python 2.7 and 3.4 or newer.

Drop support for Selenium 2 and increase the required Selenium 3.4 version. (`#1142`_)
--------------------------------------------------------------------------------------
Support for Selenium 2 was dropped and minimum required Selenium version was raised to 3.4.0.

Passing attribute name as part of the locator is deprecated since SeleniumLibrary 3.0. Remove the support. (`#1185`_)
---------------------------------------------------------------------------------------------------------------------
Removed support passing attribute name as part of the locator. This is not anymore supported
::

   | ${id}= | Get Element Attribute | css:h1@id |

Instead this is only supported
::

   | ${id}= | Get Element Attribute | css:h1 | id |

Remove deprecated support for Set Screenshot Directory persist argument (`#1186`_)
----------------------------------------------------------------------------------
Deprecated persist argument was removed from Screenshot Directory keyword.

Remove deprecated aliases support from Select Window keyword (`#1187`_)
-----------------------------------------------------------------------
Deprecated aliases  "None", "null" and the empty string for selecting the main window
and alias "self" for selecting the current window where removed.

Deprecated features
===================
All silently deprecated keyword in 3.0 should be deprecated with warning. (`#963`_, rc 1)
-----------------------------------------------------------------------------------------
During the 3.0 several keywords where silently deprecated. In this release, using those
keywords will display an warning. The next release will remote the deprecated keywords.

Acknowledgements
================
Many thanks for Tania Bhullar providing PR for adding message argument to Location Should Be keyword (`#1090`_).
Many thanks for Dmitriy Robota for providing PR to Add scroll Element into view Keyword (`#763`_). Many
thanks to DanielPBak fixing documentation bug for custom locator (`#1177`_). And last but not for least,
many thanks to Marcin Koperski for providing PR to expose Selenium session id as a keyword. (`#1136`_).

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#963`_
      - enhancement
      - critical
      - All silently deprecated keyword in 3.0 should be deprecated with warning.
    * - `#1084`_
      - bug
      - high
      - ElementFinder can't raise correct exception if locator contains characters like ö ä å
    * - `#1098`_
      - enhancement
      - high
      - Headless Firefox and Chrome not working over selenium grid
    * - `#1141`_
      - enhancement
      - high
      - Remove Python 3.3 support from SeleniumLibrary
    * - `#1142`_
      - enhancement
      - high
      - Drop support for Selenium 2 and increase the required Selenium 3.4 version.
    * - `#1183`_
      - bug
      - medium
      - Update documentation: SeleniumLibrary is not thread safe
    * - `#1073`_
      - enhancement
      - medium
      - Create `Element Attribute Should Be   locator   attribute   value`
    * - `#1090`_
      - enhancement
      - medium
      - Add message to Location Should Be keyword
    * - `#1185`_
      - enhancement
      - medium
      - Passing attribute name as part of the locator is deprecated since SeleniumLibrary 3.0. Remove the support.
    * - `#1186`_
      - enhancement
      - medium
      - Remove deprecated support for Set Screenshot Directory persist argument
    * - `#1187`_
      - enhancement
      - medium
      - Remove deprecated aliases support from Select Window keyword
    * - `#323`_
      - enhancement
      - medium
      - Allow arguments to be passed into JavaScript scripts
    * - `#757`_
      - enhancement
      - medium
      - Keyword to wait that windows is open
    * - `#763`_
      - enhancement
      - medium
      - Add scroll Element into view Keyword from ExtendedSelenium2Library
    * - `#905`_
      - enhancement
      - medium
      - Support holding shift and control when using `Click Element`
    * - `#1177`_
      - bug
      - low
      - Fix documentation bug for custom locator
    * - `#1136`_
      - enhancement
      - low
      - Expose Selenium session id as a keyword.

Altogether 17 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.2.0>`__.

.. _#963: https://github.com/robotframework/SeleniumLibrary/issues/963
.. _#1084: https://github.com/robotframework/SeleniumLibrary/issues/1084
.. _#1098: https://github.com/robotframework/SeleniumLibrary/issues/1098
.. _#1141: https://github.com/robotframework/SeleniumLibrary/issues/1141
.. _#1142: https://github.com/robotframework/SeleniumLibrary/issues/1142
.. _#1183: https://github.com/robotframework/SeleniumLibrary/issues/1183
.. _#1073: https://github.com/robotframework/SeleniumLibrary/issues/1073
.. _#1090: https://github.com/robotframework/SeleniumLibrary/issues/1090
.. _#1185: https://github.com/robotframework/SeleniumLibrary/issues/1185
.. _#1186: https://github.com/robotframework/SeleniumLibrary/issues/1186
.. _#1187: https://github.com/robotframework/SeleniumLibrary/issues/1187
.. _#323: https://github.com/robotframework/SeleniumLibrary/issues/323
.. _#757: https://github.com/robotframework/SeleniumLibrary/issues/757
.. _#763: https://github.com/robotframework/SeleniumLibrary/issues/763
.. _#905: https://github.com/robotframework/SeleniumLibrary/issues/905
.. _#1177: https://github.com/robotframework/SeleniumLibrary/issues/1177
.. _#1136: https://github.com/robotframework/SeleniumLibrary/issues/1136
