========================
SeleniumLibrary 3.0.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.0.0rc1 is a new release with
with Python 3 support and and rewritten architecture. There are two  major difference to the beta3
release:  1) There is cleaner API for extending the SeleniumLibrary. 2) The library documenation
has been rewritten and unified. There are also many other smaller bigger enhancements.

All issues targeted for SeleniumLibrary v3.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.0.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.0.0rc1 was released on Wednesday November 15, 2017.

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

To ease support for Python 3.3, the support for Python 2.6 was dropped (`#620`_, alpha 1).

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

The new architecture should not change how the keywords are used in Robot
Framework test data. But causes changes how the SeleniumLibrary can be
used to build new libraries. We have deprecated many private methods and have
created many new public methods or attributes which should make the extending
more easier in the future.

Enhance project documentation in README (`#873`_, beta 1)
---------------------------------------------------------
The project documentation, expect keyword documentation, has been rewritten to
better serve user of the SeleniumLibrary. Also documentation was enahnced in:
(`#924`_, beta 3)

Document that Jython and PyPy are supported but IronPython is not (`#879`_, beta 3)
-----------------------------------------------------------------------------------
The current release was automatically tested with Python 2.7, Python 3.3
and Python 3.6. The Jython, PyPy and IronPython compatibility was tested
manually. We found that SeleniumLibrary supports Jython and PyPy, but
IronPython is not supported.

Next steps are add the Jython and PyPy testing in CI.

Externally useful attributes should be declared public and documented. (`#882`_, rc 1)
--------------------------------------------------------------------------------------
The library public API was enhanced. The public API contains methods to find single element
or find multiple elemeent. The browser attribute was renamed to driver and BrowserCache
was renamed to WebDriverCache. Also some of the internal methods where renamed from
browser to driver. Also sphinx style definitions where added to most used methods
to ease IDE support. The change is not visible in the keyword level.

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

Cleanup and enhance keyword documentation (`#925`_, rc 1)
---------------------------------------------------------
Whole keyword documentaion has been rewritten and formatted to use the Robot Framework
library documentation format. The new documentation should describe better what the
keywords are actually doing and make the keyword usage more easier.

Clean up keywords related to alerts (`#933`_, rc 1)
---------------------------------------------------
The logic of alert releated kewyord has been rewritten. The alert keywords logic, in previous
releases was not not cleanr and contained many obvious bugs. Because of this many of the
alert keywords has been deprecated and new keywords have been created to provide better
interface for handling alters. See the keyword documentation and the issue for details
about the change.

Backwards incompatible changes
==============================


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
2.8.7.

In next release, it is planned to drop the support for Robot Framework 2.8.7.

Increase the required selenium version to latest selenium 2 version (`#704`_, alpha 1)
--------------------------------------------------------------------------------------
The minimum required Selenium version is now updated to 2.53.6,
which is the latest Selenium 2 release.

Use booleans arguments like in Robot Framework (`#719`_, alpha 1)
-----------------------------------------------------------------
The boolean arguments are handled in similar way as in Robot
Framework. More details in library `Boolean arguments`_ documentation.

Modify Get Webelements not to raise exception when no elements are found (`#805`_, beta 3)
------------------------------------------------------------------------------------------
The Get Webelements keyword does not anymore fail if the keyword does not find any elements.

Remove SeleniumLibrary profile for Firefox (`#883`_, beta 3)
------------------------------------------------------------
The Firefox profile was removed from the SeleniumLibrary and
Selenium default profile is used instead. Although this should
not cause any problems, there is low risk for some backwards
incompatible change.

Cleaning up locating windows (`#966`_, rc 1)
--------------------------------------------
Like alter in keywords, the logic of selecting windows did contains inconsistency. This logic has
been now refactored to be consistent and some of the supported ways to selecting window has been
dropped. But now the documentation how the window can be located is enhanced and it should be
clear how locating windown works.

`Get Selected List Values/Labels` keywords should not fail if list has no selections (`#977`_, rc 1)
----------------------------------------------------------------------------------------------------
The Get Selected List Values/Labels keywords do not anymore fail if the list has not no selections.
This chnage was done to unify how the Get* type of keywords works.

Remove unused expiry argument from `Add Cookie` keyword (`#847`_, alpha 1)
--------------------------------------------------------------------------
The expiry argument was removed in alpha 1 because it was not used. But the
expiry argument was added back in the (`#891`_, rc 1)

Some checkbox keywords work also with radio buttons (`#962`_, rc 1)
-------------------------------------------------------------------
Some of the checkbox keywords did work also with radio buttons in previous released. This is
changed in this release and checkbox keywords only work with radio buttons.


`Set Screenshot Directory` is inconsistent with other `Set ...` keywords (`#985`_, rc 1)
----------------------------------------------------------------------------------------
The other Set type of keywords replace the previosus value but the `Set Screenshot Directory`
keyword tries to restore the previous value when the scope end. Restoring the previous value
is good idea, but it did have a bug and it was poorly documented. Automatically restoring the
original value might be a good feature, but it should be used consistently, be documented better,
and obviously also fixed. All that is way too much work in release 3.0.0 and instead we'll remove
this functionality from


`Wait Until Element Is Enabled` should also check `readonly` status (`#958`_, rc 1)
-----------------------------------------------------------------------------------
The `Wait Until Element Is Enabled` now also checks the element `readonly` status.

Make it an error to unregister a locator strategy that hasn't been registered (`#961`_, rc 1)
---------------------------------------------------------------------------------------------
Now an exception is raised if `Unregister` keyword is used to unregister a locator strategy
which was not registered.

Deprecated features
===================

Deprecate `Select From List` and `Unselect From List` (`#988`_, rc 1)
---------------------------------------------------------------------
`Select From List` and `Unselect From List` keywords try to select/unselect items both by values
and labels. This makes their implementation complex and slow, and the code also seems to have
some subtle bugs.

In addition to these keywords, we have dedicated keywords `(Un)select From List By Label`,
`(Un)select From List By Value` and `(Un)select From List By Index` which are much more simple.
We've decided to deprecate Select From List and Unselect From List keywords in favor of these
label/value/index specific keywords.

Enhancements to getting and validating elements counts (`#949`_, rc 1)
----------------------------------------------------------------------
In the previous releases the where different ways to count or verify how many elements
the page did contain: `Locator Should Match X Times`, `Xpath Should Match X Times` and
`Get Matching Xpath Count`. Those keywords are now silently deprecated and user should now
use `Page Should Contain Element` keyword with limit argument or the `Get Matching Locator Count`
keyword.


Acknowledgements
================

Many thanks to "thaffenden" to add `Get Locations` keyword. "davidshepherd7"  to fixing issue
when getting window information and switching windows on browsers that do not support javascript.

Many thanks to  "wappowers" who added 'Get Cookie' keyword and added 'expiry' as value that
can be set with 'Add Cookie' keyword.

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
    * - `#882`_
      - enhancement
      - high
      - Externally useful attributes should be declared public and documented.
      - rc 1
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
    * - `#925`_
      - enhancement
      - high
      - Cleanup and enhance keyword documentation
      - rc 1
    * - `#933`_
      - enhancement
      - high
      - Clean up keywords related to alerts
      - rc 1
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
    * - `#891`_
      - bug
      - medium
      - Fix setting cookie expiry date
      - rc 1
    * - `#898`_
      - bug
      - medium
      - "Set Selenium Speed" doesn't work when called before opening browser in release 3.0.0b1
      - beta 3
    * - `#934`_
      - bug
      - medium
      - Regressions in `Dismiss Alert` and `Confirm Action` compared to 1.8
      - rc 1
    * - `#990`_
      - bug
      - medium
      - Bugs finding table cells when row has both `td` and `th` elements
      - rc 1
    * - `#502`_
      - enhancement
      - medium
      - Capture Page Screenshot should not overwrite if file already exist
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
    * - `#805`_
      - enhancement
      - medium
      - Modify Get Webelements not to raise exception when no elements are found
      - beta 3
    * - `#851`_
      - enhancement
      - medium
      - Add keyword that checks focus
      - alpha 1
    * - `#883`_
      - enhancement
      - medium
      - Remove SeleniumLibrary profile for Firefox
      - beta 3
    * - `#932`_
      - enhancement
      - medium
      - Add keyword to get all cookie information
      - rc 1
    * - `#942`_
      - enhancement
      - medium
      - Support configurable timeout with alert related keywords
      - rc 1
    * - `#966`_
      - enhancement
      - medium
      - Cleaning up locating windows
      - rc 1
    * - `#977`_
      - enhancement
      - medium
      - `Get Selected List Values/Labels` keywords should not fail if list has no selections
      - rc 1
    * - `#987`_
      - enhancement
      - medium
      - New `Unselect All From List` keyword
      - rc 1
    * - `#988`_
      - enhancement
      - medium
      - Deprecate `Select From List` and `Unselect From List`
      - rc 1
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
    * - `#962`_
      - bug
      - low
      - Some checkbox keywords work also with radio buttons
      - rc 1
    * - `#985`_
      - bug
      - low
      - `Set Screenshot Directory` is inconsistent with other `Set ...` keywords
      - rc 1
    * - `#715`_
      - enhancement
      - low
      - Support returning int from `Get Matching Xpath Count`
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
    * - `#943`_
      - enhancement
      - low
      - `Wait For Condition` should validate that condition contains `return`
      - rc 1
    * - `#949`_
      - enhancement
      - low
      - Enhancements to getting and validating element counts
      - rc 1
    * - `#958`_
      - enhancement
      - low
      - `Wait Until Element Is Enabled` should also check `readonly` status
      - rc 1
    * - `#961`_
      - enhancement
      - low
      - Make it an error to unregister a locator strategy that hasn't been registered
      - rc 1

Altogether 50 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.0>`__.

.. _#479: https://github.com/robotframework/SeleniumLibrary/issues/479
.. _#777: https://github.com/robotframework/SeleniumLibrary/issues/777
.. _#620: https://github.com/robotframework/SeleniumLibrary/issues/620
.. _#771: https://github.com/robotframework/SeleniumLibrary/issues/771
.. _#873: https://github.com/robotframework/SeleniumLibrary/issues/873
.. _#879: https://github.com/robotframework/SeleniumLibrary/issues/879
.. _#882: https://github.com/robotframework/SeleniumLibrary/issues/882
.. _#908: https://github.com/robotframework/SeleniumLibrary/issues/908
.. _#923: https://github.com/robotframework/SeleniumLibrary/issues/923
.. _#924: https://github.com/robotframework/SeleniumLibrary/issues/924
.. _#925: https://github.com/robotframework/SeleniumLibrary/issues/925
.. _#933: https://github.com/robotframework/SeleniumLibrary/issues/933
.. _#176: https://github.com/robotframework/SeleniumLibrary/issues/176
.. _#435: https://github.com/robotframework/SeleniumLibrary/issues/435
.. _#546: https://github.com/robotframework/SeleniumLibrary/issues/546
.. _#652: https://github.com/robotframework/SeleniumLibrary/issues/652
.. _#779: https://github.com/robotframework/SeleniumLibrary/issues/779
.. _#790: https://github.com/robotframework/SeleniumLibrary/issues/790
.. _#816: https://github.com/robotframework/SeleniumLibrary/issues/816
.. _#891: https://github.com/robotframework/SeleniumLibrary/issues/891
.. _#898: https://github.com/robotframework/SeleniumLibrary/issues/898
.. _#934: https://github.com/robotframework/SeleniumLibrary/issues/934
.. _#990: https://github.com/robotframework/SeleniumLibrary/issues/990
.. _#502: https://github.com/robotframework/SeleniumLibrary/issues/502
.. _#673: https://github.com/robotframework/SeleniumLibrary/issues/673
.. _#703: https://github.com/robotframework/SeleniumLibrary/issues/703
.. _#704: https://github.com/robotframework/SeleniumLibrary/issues/704
.. _#719: https://github.com/robotframework/SeleniumLibrary/issues/719
.. _#722: https://github.com/robotframework/SeleniumLibrary/issues/722
.. _#805: https://github.com/robotframework/SeleniumLibrary/issues/805
.. _#851: https://github.com/robotframework/SeleniumLibrary/issues/851
.. _#883: https://github.com/robotframework/SeleniumLibrary/issues/883
.. _#932: https://github.com/robotframework/SeleniumLibrary/issues/932
.. _#942: https://github.com/robotframework/SeleniumLibrary/issues/942
.. _#966: https://github.com/robotframework/SeleniumLibrary/issues/966
.. _#977: https://github.com/robotframework/SeleniumLibrary/issues/977
.. _#987: https://github.com/robotframework/SeleniumLibrary/issues/987
.. _#988: https://github.com/robotframework/SeleniumLibrary/issues/988
.. _#592: https://github.com/robotframework/SeleniumLibrary/issues/592
.. _#759: https://github.com/robotframework/SeleniumLibrary/issues/759
.. _#847: https://github.com/robotframework/SeleniumLibrary/issues/847
.. _#962: https://github.com/robotframework/SeleniumLibrary/issues/962
.. _#985: https://github.com/robotframework/SeleniumLibrary/issues/985
.. _#715: https://github.com/robotframework/SeleniumLibrary/issues/715
.. _#794: https://github.com/robotframework/SeleniumLibrary/issues/794
.. _#920: https://github.com/robotframework/SeleniumLibrary/issues/920
.. _#943: https://github.com/robotframework/SeleniumLibrary/issues/943
.. _#949: https://github.com/robotframework/SeleniumLibrary/issues/949
.. _#958: https://github.com/robotframework/SeleniumLibrary/issues/958
.. _#961: https://github.com/robotframework/SeleniumLibrary/issues/961
.. _Dynamic library API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Boolean arguments: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Boolean%20arguments
