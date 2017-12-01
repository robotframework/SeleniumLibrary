=====================
SeleniumLibrary 3.0.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.0.0 is a new release with
Python 3 support and various other big enhancements such as better
public API for extending the library and highly enhanced keyword
documentation. The library architecture has also changed making it easier
to maintain and develop further.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.0.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.0.0 was released on Friday December 1, 2017.

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

Python 3 support
----------------

SeleniumLibrary was enhanced to support Python 3 (`#479`_) and at the same
time Python 2.6 support was dropped (`#620`_). More precisely, the currently
supported Python versions are 2.7, 3.3 and newer.

Name changed from Selenium2Library to SeleniumLibrary
-----------------------------------------------------

Because Selenium moved from version 2 to version 3, we felt that the old name,
Selenium2Library, did not anymore describe what the library supports and
helps user to achieve. At the same time the old SeleniumLibrary became totally
unusable as Selenium 3 dropped support for the remote controller API it used.

In this situation we decided to rename Selenium2Library to SeleniumLibrary
(`#777`_). We also created new Selenium2Library that is just a wrapper
for SeleniumLibrary and is meant only to ease migration. For more information
see the `project pages`__.

__ https://github.com/robotframework/SeleniumLibrary/blob/master/README.rst#versions

Better documentation
--------------------

The general project documentation (`#873`_) as well as keyword documentation
(`#924`_ and `#925`_) have been enhanced heavily and in practice rewritten.

Better architecture
-------------------

The old architecture did not work too well anymore when the library had
grown so large and it made the development of the library slower or more
difficult. The old architecture also made it hard to define clear API
for the user who are building their own libraries on top of the
SeleniumLibrary.

The new architecture (`#771`_) relies on the Robot Framework `Dynamic library API`__,
PythonLibCore__ and using context object to share state and common methods
between different classes and methods. Because of the new architecture, many
private methods or classes have been changed or removed totally.

The new architecture should not change how the keywords are used in Robot
Framework test data. But new architecture causes changes how the SeleniumLibrary can
be used to build new libraries. We have deprecated many private methods and have
created many new public methods or attributes which should make the extending
more easier in the future. The public API is also documented (`#882`_).

__ http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
__ https://github.com/robotframework/PythonLibCore

New `strategy:value` syntax to specify locator strategy
-------------------------------------------------------

Nowadays the recommended syntax to specify an explicit locator strategy
is `strategy:value` like `id:example` or `css:h1` (`#908`_). The old (and
still supported) `strategy=value` syntax is problematic because Robot
Framework uses the same syntax with `named arguments`__.

__ http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#named-argument-syntax

Tables located using same logic as other elements
-------------------------------------------------

In the previous releases, the table keywords locator strategy did differ
greatly from the rest of keywords which did interact with elements in
the browsers. This is now changed and tables can be located with same
locator strategies which can be used for the rest of the library (`#923`_).

Clean-up to alert related keywords
----------------------------------

The logic of alert related keywords has been rewritten. The alert keywords
logic in previous releases was not clear and contained many obvious bugs.
Because of this many of the alert keywords has been deprecated and new
keywords have been created to provide better interface for handling alters.
See the keyword documentation and the issue `#933`_ for details about the
change.

Jython and PyPy support
-----------------------

In addition to the standard Python 2 and Python 3 interpreters, also `Jython
<http://jython.org>`_ and `PyPy <http://pypy.org>`_ are now officially
supported (`#879`_).

Backwards incompatible changes and deprecated features
======================================================

Robot Framework and Selenium minimum versions increased
-------------------------------------------------------

Nowadays the minimum supported Robot Framework version is 2.8.7 (`#703`_).
It is likely that SeleniumLibrary 3.1 raises this requirement to Robot
Framework 2.9 or even 3.0.

The minimum required Selenium version is now 2.53.6.

New architecture
----------------

The `better architecture`_ discussed above changes library internals a lot.
This should not affect tests using keywords provided by the library, but
other libraries and tools interacting with SeleniumLibrary are likely to
require an update.

How to interact with the library and how to safely extend
it is `going to be documented`__. Until that, if you are a maintainer of
a library that is broken due to these changes, please report your problems
on `robotframework-users mailing list`__, or on #seleniumlibrary channel on
the `Slack community`__.

__ https://github.com/robotframework/SeleniumLibrary/issues/1007
__ https://groups.google.com/group/robotframework-users
__ https://robotframework-slack-invite.herokuapp.com/

Attributes in programmatic API renamed
--------------------------------------

Various attributes in the programmatic API have been renamed and the
old attribute names are deprecated (`#882`_).

Keywords returning lists don't fail if there are no matches
-----------------------------------------------------------

Earlier `Get WebElememts` (`#805`_) and `Get Selected List Values/Labels`
keywords (`#977`_) failed if where were no matches. Nowadays they return
an empty list instead.

`Set Screenshot Directory` does not automatically restore old value
-------------------------------------------------------------------

Earlier `Set Screenshot Directory` keyword tried to automatically restore
the previous value when the current scope end, but this functionality was
not documented adequately and contained bugs. The functionality was removed
and, instead, the keyword returns the previous value similarly as `Set
Selenium Timeout` and other `Set ...` keywords.

Changes to locating windows
---------------------------

Locating windows has been cleaned up and documented thoroughly. As part of
the cleanup, undocumented features not considered useful were deprecated or
removed:

- Using Python `None` or string `null` or empty string as a locator to
  select the main window is deprecated. Use documented `main` (default)
  instead.
- Using `popup` to select the latest new window is deprecated. Use
  documented `new` instead.
- Using `self` to select the current window is deprecated. Use earlier
  undocumented but much more explicit `current` instead.
- Locating windows by name, title or URL is not case-insensitive anymore.
- Specifying explicit locator strategy is not case-insensitive anymore.

Such changes are obviously backwards incompatible, but because these are
undocumented features, it's very unlikely that they are used widely.

Deprecated keywords
-------------------

Various hard-to-use or badly named keywords have been "silently" deprecated
in favor of better keywords. This means that the old keywords can be still
used without warnings, but they will emit a deprecation warning staring from
SeleniumLibrary 3.1.

==================================  =================================================  =======
        Deprecated keyword                             Use instead                      Issue
==================================  =================================================  =======
Select From List                    Select From List By Label/Value/Index              `#988`_
Unselect From List                  Unselect From List By Label/Value/Index            `#988`_
Current Frame Contains              Current Frame Should Contain                       `#920`_
Get Cookie Value                    Get Cookie                                         `#932`_
List Windows                        Get Window Handles                                 `#966`_
Locator Should Match X Times        Page Should Contain Element (w/ `limit` argument)  `#949`_
XPath Should Match X Times          Page Should Contain Element (w/ `limit` argument)  `#949`_
Get Matching XPath Count            Get Element Count                                  `#949`_
Focus                               Set Focus To Element                               `#920`_
Simulate                            Simulate Event                                     `#920`_
Input Text Into Prompt              Input Text Into Alert                              `#933`_
Choose Ok On Next Confirmation      Handle Alert                                       `#933`_
Choose Cancel On Next Confirmation  Handle Alert                                       `#933`_
Confirm Action                      Handle Alert                                       `#933`_
Get Alert Message                   Handle Alert                                       `#933`_
Dismiss Alert                       Handle Alert                                       `#933`_
==================================  =================================================  =======

Other backwards incompatible changes
------------------------------------

- Bundled Firefox profile has been removed and Selenium default profile is
  used instead (`#883`_).
- `Register Keyword To Run On Failure` returns Python `None`, not
  string `No keyword`, if no keywords was previously registered (`#176`_).
- `Capture Page Screenshot` doesn't overwrite existing screenshots
  by default (`#502`_).
- Checkbox keywords don't anymore work with radio buttons (`#962`_)
- `Wait Until Element Is Enabled` checks also `readonly` status (`#958`_)
- It is an error to unregister a locator strategy that hasn't been registered
  (`#961`_).

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
    * - `#479`_
      - enhancement
      - critical
      - Python 3 support
    * - `#777`_
      - enhancement
      - critical
      - Change library name from Selenium2Library to SeleniumLibrary
    * - `#620`_
      - enhancement
      - high
      - Drop Python 2.6 support
    * - `#771`_
      - enhancement
      - high
      - Create better architecture
    * - `#873`_
      - enhancement
      - high
      - Enhance project documentation in README
    * - `#879`_
      - enhancement
      - high
      - Document that Jython and PyPy are supported but IronPython is not
    * - `#882`_
      - enhancement
      - high
      - Externally useful attributes should be declared public and documented.
    * - `#908`_
      - enhancement
      - high
      - New `strategy:value` syntax to specify locator strategy in addition to current `strategy=value`
    * - `#923`_
      - enhancement
      - high
      - Tables should be located using same logic as other elements
    * - `#924`_
      - enhancement
      - high
      - Enhance general library documentation in keyword docs
    * - `#925`_
      - enhancement
      - high
      - Cleanup and enhance keyword documentation
    * - `#933`_
      - enhancement
      - high
      - Clean up keywords related to alerts
    * - `#176`_
      - bug
      - medium
      - Return value of `Register keyword to run on failure` cannot always be used to restore original state
    * - `#435`_
      - bug
      - medium
      - Note version added to recently added keywords.
    * - `#546`_
      - bug
      - medium
      - HTML5 specialized text fields not recognized as text fields
    * - `#652`_
      - bug
      - medium
      - Handling alerts sometimes fails with Chrome
    * - `#779`_
      - bug
      - medium
      - Acceptance test do not work in windows
    * - `#790`_
      - bug
      - medium
      - Cannot switch windows on browsers which don't support javascript
    * - `#816`_
      - bug
      - medium
      - Modify Capture Page Screenshot keyword not fail if browser is not open.
    * - `#891`_
      - bug
      - medium
      - Fix setting cookie expiry date
    * - `#990`_
      - bug
      - medium
      - Bugs finding table cells when row has both `td` and `th` elements
    * - `#502`_
      - enhancement
      - medium
      - Capture Page Screenshot should not overwrite if file already exist
    * - `#673`_
      - enhancement
      - medium
      - Support locating elements using element class
    * - `#703`_
      - enhancement
      - medium
      - Update required Robot Framework version to 2.8
    * - `#704`_
      - enhancement
      - medium
      - Increase the required selenium version to latest selenium 2 version
    * - `#719`_
      - enhancement
      - medium
      - Use booleans arguments like in Robot Framework
    * - `#722`_
      - enhancement
      - medium
      - Enhance `Get List Items` to support returning values or labels
    * - `#805`_
      - enhancement
      - medium
      - Modify Get Webelements not to raise exception when no elements are found
    * - `#851`_
      - enhancement
      - medium
      - Add keyword that checks focus
    * - `#883`_
      - enhancement
      - medium
      - Remove SeleniumLibrary profile for Firefox
    * - `#932`_
      - enhancement
      - medium
      - Add keyword to get all cookie information
    * - `#942`_
      - enhancement
      - medium
      - Support configurable timeout with alert related keywords
    * - `#966`_
      - enhancement
      - medium
      - Cleaning up locating windows
    * - `#977`_
      - enhancement
      - medium
      - `Get Selected List Values/Labels` keywords should not fail if list has no selections
    * - `#987`_
      - enhancement
      - medium
      - New `Unselect All From List` keyword
    * - `#988`_
      - enhancement
      - medium
      - Deprecate `Select From List` and `Unselect From List`
    * - `#592`_
      - bug
      - low
      - Deprecation warning from Selenium when using `Select/Unselect Frame`
    * - `#759`_
      - bug
      - low
      - Change link in help `Get Alert Message` to `Dismiss Alert`
    * - `#962`_
      - bug
      - low
      - Some checkbox keywords work also with radio buttons
    * - `#985`_
      - bug
      - low
      - `Set Screenshot Directory` is inconsistent with other `Set ...` keywords
    * - `#715`_
      - enhancement
      - low
      - Support returning int from `Get Matching Xpath Count`
    * - `#794`_
      - enhancement
      - low
      - Extend xpath detection to support xpath starting with (//
    * - `#920`_
      - enhancement
      - low
      - Better names for `Current Frame Contains`, `Focus` and `Simulate`
    * - `#943`_
      - enhancement
      - low
      - `Wait For Condition` should validate that condition contains `return`
    * - `#949`_
      - enhancement
      - low
      - Enhancements to getting and validating element counts
    * - `#958`_
      - enhancement
      - low
      - `Wait Until Element Is Enabled` should also check `readonly` status
    * - `#961`_
      - enhancement
      - low
      - Make it an error to unregister a locator strategy that hasn't been registered

Altogether 47 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.0>`__.

.. _#479: https://github.com/robotframework/SeleniumLibrary/issues/479
.. _#777: https://github.com/robotframework/SeleniumLibrary/issues/777
.. _#1001: https://github.com/robotframework/SeleniumLibrary/issues/1001
.. _#998: https://github.com/robotframework/SeleniumLibrary/issues/998
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
