=======================
SeleniumLibrary 3.0.0b3
=======================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.0.0b3 is a new release with
Python 3 support and rewritten architecture. The new architecture should be
mostly invisible from the Robot Framework test date point of view. But there
are many changes in internal methods and classes, which may affect users
who have written libraries extending SeleniumLibrary private methods and
classes. There are also many other smaller bigger enhancements.

All issues targeted for SeleniumLibrary v3.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.0.0b3

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.0.0b3 was released on Thursday September 28, 2017.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Python 3 support (`#479`_, alpha 1)
-----------------------------------
The SeleniunLibrary was was enhanced to support Python 3.3 or newer.
More precisely, the currently supported Python versions are 2.7, 3.3 and newer.
Installation on Python 3 works exactly as it does for Python 2, and the
recommended installation method is with pip.

To ease support for Python 3.3, the support for Python 2.6 was dropped.

Change library name from Selenium2Library to SeleniumLibrary (`#777`_, alpha 1)
-------------------------------------------------------------------------------
Because Selenium moved from version 2 to version 3, we felt that the old name,
Selenium2Library, did not anymore describe what the library supports and
helps user to achieve. Therefore we renamed the original SeleniumLibrary to
OldSeleniumLibrary. Then the Selenium2Libary was renamed to SeleniumLibrary
and new Selenium2Library was created. The new Selenium2Library is just a wrapper
for the SeleniumLibrary and is meant only to ease migration from
Selenium2Library to SeleniumLibrary.


Create better architecture for Selenium2Library (`#771`_, alpha 1)
------------------------------------------------------------------
The old architecture did contained many practices which are against good
coding practices and made the development of the library slower or more
difficult. The old architecture made also hard to define clear API interface
for the user who are building their own libraries on top of the
SeleniumLibrary.

The new architecture relies on the Robot Framework `Dynamic library API`_,
`PythonLibCore`_ and using context object to share common methods
between different classes and methods. Because of the new architecture, many
 private methods or classes have been changed or removed totally.

Enhance project documentation in README (`#873`_, beta 1)
---------------------------------------------------------
The project documentation, expect keyword documentation, has been rewritten to
better serve user of the SeleniumLibrary.

Document that Jython and PyPy are supported but IronPython is not (`#879`_, beta 3)
-----------------------------------------------------------------------------------
The current release was automatically tested with Python 2.7, Python 3.3
and Python 3.6. The Jython, PyPy and IronPython compatibility was tested
manually. We found that SeleniumLibrary supports Jython and PyPy, but
IronPython is not supported.

Next steps are add the Jython and PyPy testing in CI.

New `strategy:value` syntax to specify locator strategy in addition to current `strategy=value` (`#908`_, beta 3)
-----------------------------------------------------------------------------------------------------------------
New `strategy:value` syntax to specify locator strategy in addition to
current `strategy=value`. The current locator strategy causes problems with
Robot Framework keyword argument syntax, because then the equal sing must
be escaped, example `xpath\=//div | &{kw_args} |`. The locator syntax is
aimed to ease the transition when the keyword arguments are in future taken
in use.

Tables should be located using same logic as other elements (`#923`_, beta 3)
-----------------------------------------------------------------------------
The previous releases, the table keywords locator strategy did differ greatly
from the rest of keywords which did interact with elements in the browsers.
This is now changed and tables can be located with same locator
strategies which can be used for the rest of the library.

Enhance general library documentation in keyword docs (`#924`_, beta 3)
-----------------------------------------------------------------------
Library documentation, excluding individual keyword documentation, has
been rewritten.

Backwards incompatible changes
==============================

Create better architecture for Selenium2Library (`#771`_, alpha 1)
------------------------------------------------------------------
The new architecture should not change how the keywords are used in Robot
Framework test data. But causes changes how the SeleniumLibrary can be
used to build new libraries. We have deprecated many private methods and have
created many new public methods or attributes which should make the extending
more easier in the future.

Return value of `Register keyword to run on failure` cannot always be used to restore original state (`#176`_, beta 3)
----------------------------------------------------------------------------------------------------------------------
In this release the keyword returned by the `Register keyword to run on
failure` keyword can be always used to restore the original state. User
do not anymore need to have special logic in Robot Framework test data
to restore the `Run On Failure` keyword.

Capture Page Screenshot should not overwrite if file already exist  (`#502`_, alpha 1)
--------------------------------------------------------------------------------------
The `Capture Page Screenshot` keyword now verifies from the file system
that screenshot file does not exist in the file system. If the file
exist, it will create new index in the file name until it find a file
name which does not exist.

If the filename does not contain index, the filename is always
overwritten.

Update required Robot Framework version to 2.8 (`#703`_, alpha 1)
-----------------------------------------------------------------
The minimum requires Robot Framework version is now updated to
2.8.7

Increase the required selenium version to latest selenium 2 version (`#704`_, alpha 1)
--------------------------------------------------------------------------------------
The minimum required Selenium version is now updated to 2.53.6,
which is the latest Selenium 2 release.

Use booleans arguments like in Robot Framework (`#719`_, alpha 1)
-----------------------------------------------------------------
The boolean arguments are handled in similar way as in Robot
Framework. More details in library `Boolean arguments`_ documentation.

Remove SeleniumLibrary profile for Firefox (`#883`_, beta 3)
------------------------------------------------------------
The Firefox profile was removed from the SeleniumLibrary and
Selenium default profile is used instead. Although this should
not cause any problems, there is low risk for some backwards
incompatible change.

Other backwards incompatible changes
------------------------------------

- New `strategy:value` syntax to specify locator strategy in addition to current `strategy=value` (`#908`_, beta 3)
- Drop Python 2.6 support (`#620`_, alpha 1)
- Remove unused expiry argument from `Add Cookie` keyword (`#847`_, alpha 1)
- Modify Get Webelements not to raise exception when no elements are found (`#805`_, beta 3)
- Drop Python 2.6 support (`#620`_, alpha 1)

Deprecated features
===================
- Change library name from Selenium2Library to SeleniumLibrary (`#777`_, alpha 1)
- Externally useful attributes should be declared public and not start with an underscore (`#882`_, beta 3)

Acknowledgements
================

Many thanks to "thaffenden" to add `Get Locations` keyword. "davidshepherd7"  to fixing issue
when getting window information and switching windows on browsers that do not support javascript.
Many thanks to many other contributors who have helped to make this release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#479`_
      - enhancement
      - critical
      - Python 3 support
      - alpha 1
    * - `#777`_
      - enhancement
      - critical
      - Change library name from Selenium2Library to SeleniumLibrary
      - alpha 1
    * - `#620`_
      - enhancement
      - high
      - Drop Python 2.6 support
      - alpha 1
    * - `#771`_
      - enhancement
      - high
      - Create better architecture for Selenium2Library
      - alpha 1
    * - `#873`_
      - enhancement
      - high
      - Enhance project documentation in README
      - beta 1
    * - `#879`_
      - enhancement
      - high
      - Document that Jython and PyPy are supported but IronPython is not
      - beta 3
    * - `#908`_
      - enhancement
      - high
      - New `strategy:value` syntax to specify locator strategy in addition to current `strategy=value`
      - beta 3
    * - `#923`_
      - enhancement
      - high
      - Tables should be located using same logic as other elements
      - beta 3
    * - `#924`_
      - enhancement
      - high
      - Enhance general library documentation in keyword docs
      - beta 3
    * - `#176`_
      - bug
      - medium
      - Return value of `Register keyword to run on failure` cannot always be used to restore original state
      - beta 3
    * - `#435`_
      - bug
      - medium
      - Note version added to recently added keywords.
      - beta 2
    * - `#546`_
      - bug
      - medium
      - HTML5 specialized text fields not recognized as text fields
      - alpha 1
    * - `#652`_
      - bug
      - medium
      - Handling alerts sometimes fails with Chrome
      - alpha 1
    * - `#779`_
      - bug
      - medium
      - Acceptance test do not work in windows
      - alpha 1
    * - `#790`_
      - bug
      - medium
      - Cannot switch windows on browsers which don't support javascript
      - alpha 1
    * - `#816`_
      - bug
      - medium
      - Modify Capture Page Screenshot keyword not fail if browser is not open.
      - beta 3
    * - `#898`_
      - bug
      - medium
      - "Set Selenium Speed" doesn't work when called before opening browser in release 3.0.0b1
      - beta 3
    * - `#502`_
      - enhancement
      - medium
      - Capture Page Screenshot should not overwrite if file already exist
      - alpha 1
    * - `#574`_
      - enhancement
      - medium
      - Add function to capture console logs from selenium browser.
      - alpha 1
    * - `#673`_
      - enhancement
      - medium
      - Support locating elements using element class
      - alpha 1
    * - `#703`_
      - enhancement
      - medium
      - Update required Robot Framework version to 2.8
      - alpha 1
    * - `#704`_
      - enhancement
      - medium
      - Increase the required selenium version to latest selenium 2 version
      - alpha 1
    * - `#719`_
      - enhancement
      - medium
      - Use booleans arguments like in Robot Framework
      - alpha 1
    * - `#722`_
      - enhancement
      - medium
      - Enhance `Get List Items` to support returning values or labels
      - alpha 1
    * - `#851`_
      - enhancement
      - medium
      - Add keyword that checks focus
      - alpha 1
    * - `#882`_
      - enhancement
      - medium
      - Externally useful attributes should be declared public and not start with an underscore
      - beta 3
    * - `#883`_
      - enhancement
      - medium
      - Remove SeleniumLibrary profile for Firefox
      - beta 3
    * - `#592`_
      - bug
      - low
      - Deprecation warning from Selenium when using `Select/Unselect Frame`
      - alpha 1
    * - `#759`_
      - bug
      - low
      - Change link in help `Get Alert Message` to `Dismiss Alert`
      - alpha 1
    * - `#847`_
      - bug
      - low
      - Remove unused expiry argument from `Add Cookie` keyword
      - alpha 1
    * - `#794`_
      - enhancement
      - low
      - Extend xpath detection to support xpath starting with (//
      - alpha 1
    * - `#920`_
      - enhancement
      - low
      - Better names for `Current Frame Contains`, `Focus` and `Simulate`
      - beta 3
    * - `#805`_
      - enhancement
      - ---
      - Modify Get Webelements not to raise exception when no elements are found
      - beta 3

Altogether 33 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.0>`__.

.. _#479: https://github.com/robotframework/SeleniumLibrary/issues/479
.. _#777: https://github.com/robotframework/SeleniumLibrary/issues/777
.. _#620: https://github.com/robotframework/SeleniumLibrary/issues/620
.. _#771: https://github.com/robotframework/SeleniumLibrary/issues/771
.. _#873: https://github.com/robotframework/SeleniumLibrary/issues/873
.. _#879: https://github.com/robotframework/SeleniumLibrary/issues/879
.. _#908: https://github.com/robotframework/SeleniumLibrary/issues/908
.. _#923: https://github.com/robotframework/SeleniumLibrary/issues/923
.. _#924: https://github.com/robotframework/SeleniumLibrary/issues/924
.. _#176: https://github.com/robotframework/SeleniumLibrary/issues/176
.. _#435: https://github.com/robotframework/SeleniumLibrary/issues/435
.. _#546: https://github.com/robotframework/SeleniumLibrary/issues/546
.. _#652: https://github.com/robotframework/SeleniumLibrary/issues/652
.. _#779: https://github.com/robotframework/SeleniumLibrary/issues/779
.. _#790: https://github.com/robotframework/SeleniumLibrary/issues/790
.. _#816: https://github.com/robotframework/SeleniumLibrary/issues/816
.. _#898: https://github.com/robotframework/SeleniumLibrary/issues/898
.. _#502: https://github.com/robotframework/SeleniumLibrary/issues/502
.. _#574: https://github.com/robotframework/SeleniumLibrary/issues/574
.. _#673: https://github.com/robotframework/SeleniumLibrary/issues/673
.. _#703: https://github.com/robotframework/SeleniumLibrary/issues/703
.. _#704: https://github.com/robotframework/SeleniumLibrary/issues/704
.. _#719: https://github.com/robotframework/SeleniumLibrary/issues/719
.. _#722: https://github.com/robotframework/SeleniumLibrary/issues/722
.. _#851: https://github.com/robotframework/SeleniumLibrary/issues/851
.. _#882: https://github.com/robotframework/SeleniumLibrary/issues/882
.. _#883: https://github.com/robotframework/SeleniumLibrary/issues/883
.. _#592: https://github.com/robotframework/SeleniumLibrary/issues/592
.. _#759: https://github.com/robotframework/SeleniumLibrary/issues/759
.. _#847: https://github.com/robotframework/SeleniumLibrary/issues/847
.. _#794: https://github.com/robotframework/SeleniumLibrary/issues/794
.. _#920: https://github.com/robotframework/SeleniumLibrary/issues/920
.. _#805: https://github.com/robotframework/SeleniumLibrary/issues/805
.. _Dynamic library API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Boolean arguments: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Boolean%20arguments