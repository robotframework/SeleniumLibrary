=======================
SeleniumLibrary 4.0.0a2
=======================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.0.0a2 is a new pre release with
Open Browser keyword to support Selenium options and service_log_path and bug fixes.

All issues targeted for SeleniumLibrary v4.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.0.0a2

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.0.0a2 was released on Thursday July 4, 2019. SeleniumLibrary supports
Python 2.7 and 3.4+, Selenium 3.8.2 and Robot Framework 3.0.4 and 3.1.2.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.0.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

SeleniumLibrary by creating plugin API.  (`#1292`_, alpha 1)
------------------------------------------------------------
SeleniumLibrary 4.0 introduces a plugin API, which allows adding
or modifying keywords directly in to the SeleniumLibrary. It also
offers more wider access to the SeleniumLibrary internal methods.

More details can be found from the `plugin API`_ documentation.


Selenium EventFiringWebdriver (`#1303`_, alpha 1)
-------------------------------------------------
SeleniumLibrary offers support for `Selenium EventFiringWebdriver`_ allowing
users to import the EventFiringWebdriver class in to the SeleniumLibrary.
More details can be found from the Selenium and SeleniumLibrary
`EventFiringWebdriver documentation`_

Open Browser keyword could take in Selenium browser specific options (`#1331`_, alpha 2)
----------------------------------------------------------------------------------------
`Open Browser` keyword provides now native way to define browser specific Selenium options.
This enhancement brings `Open Browser` keyword closer to what `Create WebDriver` keyword can do,
but with cleaner API and by using single argument. Refer to the Selenium documentation
which browser support Selenium options.

Enhance Open Browser keywords to support Selenium service_log_path argument (`#1333`_, alpha 2)
-----------------------------------------------------------------------------------------------
In the past browser driver where not logged, expect for Firefox, to a file. Now the it is possible
to define file where browser driver logs are created. This enhancement and the `#1331`_ aims
to replace `Create WebDriver` keyword.


Backwards incompatible changes
==============================

Remove deprecated attributes of unofficial public API (`#1346`_, alpha 1)
-------------------------------------------------------------------------
The Selenium2Library 1.8 and older did not have public API, but
it did have some methods which could be considered as part of a unofficial
API. The SeleniumLibrary 3.0 created new public API and in the same time
tried to keep as much as possible of the unofficial API in place. In
same time with 3.0 release the old API was deprecated. The SeleniumLibrary
4.0 removes the unofficial and deprecated API.

Drop Robot Framework 2.9 support in SeleniumLibrary. (`#1304`_, alpha 1)
------------------------------------------------------------------------
SeleniumLibrary does not anymore support Robot Framework 2.9 or older
releases. Users are encouraged to migrate Robot Framework 3.0 or 3.1.

Raise minimum supported Selenium version to 3.8.1 (`#1305`_, alpha 1)
---------------------------------------------------------------------
Minimum supported Selenium version has been raised to 3.8.1.

Remove keywords which where officially deprecated in previos releases. (`#1274`_, alpha 1)
------------------------------------------------------------------------------------------
SeleniumLibrary has removed keyword which where loudly deprecated in the previous releases.
User are encouraged to use the new keywords.

Update SeleniumLibrary is_truthy and is_falsy to follow Robot Framework 3.1  (`#1308`_, alpha 1)
------------------------------------------------------------------------------------------------
In previous SeleniumLibrary releases, string 0 was considered as true when evaluating
boolean type. This is now changed and string 0 is considered as false.

It should be possible to configure Open Browser keyword to not always open a new browser. (`#1319`_, alpha 2)
-------------------------------------------------------------------------------------------------------------
In the past `Open Browser` keyword did always open a new browser. With this enhancement
new browser only opened if aliases are different for each `Open Browser` keyword.

`Choose File` keyword should not fail if file does not exist.  (`#1402`_, alpha 2)
----------------------------------------------------------------------------------
In the past `Choose File` keyword only accepted strings which point to a file in the
file system. Now this is changed and SeleniumLibrary does not anymore perform checks
does the file exist, instead it is leaved for the underlying Selenium to device is the
input string a file, folder or something which is not acceptable.

Deprecated features
===================

Deprecate loudly all silently deprecated keywords  (`#1273`_, alpha 1)
----------------------------------------------------------------------
All keywords which where silently deprecated in the previous release, will now
cause a deprecated warning.

Acknowledgements
================

Also there has been many contributions from the community. Special thanks
to all that provided an contribution to the project. Here is a list of
contributions which have made pull request in to this release.

I would like to remind that providing code or updating documentation is
not the only way to contribute. There has been lot of issues raised in
the project issue tracker and feedback has been provided in the
user group and in slack. I am grateful from all the feedback.

Wait For Location To Contain  (`#1108`_, alpha 1)
-------------------------------------------------
Many thanks to acaovilla who provided Wait Until Location Contains keyword in the
RoboCon sprints.

Add Wait Until Location Is keyword (`#1297`_, alpha 1)
------------------------------------------------------
Many thanks to acaovilla who provided Wait Until Location Is keyword. Sometime after
the RoboCon.

Allow setting and getting window.innerWidth and window.innerHeight CSS properties (`#1363`_, alpha 1)
-----------------------------------------------------------------------------------------------------
Many thanks to ciccioman3, who enhanced the Set Window Size and Get Window Size keywords
to support window.innerWidth and window.innerHeight css attributes.

Update readme to mention https://github.com/Omenia/webdrivermanager (`#1301`_, alpha 1)
---------------------------------------------------------------------------------------
Many thanks to rasjani, who updated documentation to mention scripted browser driver
installation.

Enhance EXTENDING_SELENIUMLIBRARY.rst readability.  (`#1372`_, alpha 2)
-----------------------------------------------------------------------
many thanks to humbienri who enhanced the EXTENDING_SELENIUMLIBRARY.rst documentation.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1292`_
      - enhancement
      - critical
      - Allow extending SeleniumLibrary by creating plugin API. 
      - alpha 1
    * - `#1303`_
      - enhancement
      - critical
      - Add support event_firing_webdriver
      - alpha 1
    * - `#1304`_
      - enhancement
      - critical
      - Drop Robot Framework 2.9 support in SeleniumLibrary.
      - alpha 1
    * - `#1305`_
      - enhancement
      - critical
      - Raise minimum supported Selenium version to 3.8.1
      - alpha 1
    * - `#1331`_
      - enhancement
      - high
      - Open Browser keyword could take in Selenium browser specific options
      - alpha 2
    * - `#1333`_
      - enhancement
      - high
      - Enhance Open Browser keywords to support Selenium service_log_path argument
      - alpha 2
    * - `#1284`_
      - bug
      - medium
      - Default Capabilities not set correctly if remote_url and desired_capabilities are given
      - alpha 1
    * - `#1307`_
      - bug
      - medium
      - Get Cookies keyword will fail if the Selenium get_cookie method return value contains more keys than: name, value, path, domain, secure, httpOnly and expiry
      - alpha 1
    * - `#1380`_
      - bug
      - medium
      - Selenium version number can also contain letters
      - alpha 2
    * - `#1108`_
      - enhancement
      - medium
      - Propose new keyword:  Wait For Location To Contain 
      - alpha 1
    * - `#1273`_
      - enhancement
      - medium
      - Deprecate loudly all silently deprecated keywords 
      - alpha 1
    * - `#1274`_
      - enhancement
      - medium
      - Remove keywords which where officially deprecated in previos releases.
      - alpha 1
    * - `#1297`_
      - enhancement
      - medium
      - Add Wait Until Location Is keyword
      - alpha 1
    * - `#1308`_
      - enhancement
      - medium
      - Update SeleniumLibrary is_truthy and is_falsy to follow Robot Framework 3.1 
      - alpha 1
    * - `#1319`_
      - enhancement
      - medium
      - It should be possible to configure Open Browser keyword to not always open a new browser.
      - alpha 2
    * - `#1330`_
      - enhancement
      - medium
      - Input Text and Input Password keywords should be configurable if they clear the input element before keywords types the text in
      - alpha 1
    * - `#1336`_
      - enhancement
      - medium
      - Deprecate sizzle selector strategy 
      - alpha 1
    * - `#1346`_
      - enhancement
      - medium
      - Remove deprecated attributes of public API
      - alpha 1
    * - `#1363`_
      - enhancement
      - medium
      - Allow setting and getting window.innerWidth and window.innerHeight CSS properties
      - alpha 1
    * - `#1372`_
      - enhancement
      - medium
      - Enhance EXTENDING_SELENIUMLIBRARY.rst readability. 
      - alpha 2
    * - `#1379`_
      - enhancement
      - medium
      - When browser is closed and there is an error, the default run on failure functionality, Capture Page Screenshot, is run and it causes second exception
      - alpha 2
    * - `#1402`_
      - enhancement
      - medium
      - `Choose File` keyword should not fail if file does not exist. 
      - alpha 2
    * - `#449`_
      - bug
      - low
      - Update documentation on Choose File to show that it supports remote uploading
      - alpha 1
    * - `#1279`_
      - enhancement
      - low
      - Webdriver tools browser_alias may not be needed
      - alpha 1
    * - `#1301`_
      - enhancement
      - low
      - Update readme to mention https://github.com/Omenia/webdrivermanager
      - alpha 1

Altogether 25 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.0.0>`__.

.. _#1292: https://github.com/robotframework/SeleniumLibrary/issues/1292
.. _#1303: https://github.com/robotframework/SeleniumLibrary/issues/1303
.. _#1304: https://github.com/robotframework/SeleniumLibrary/issues/1304
.. _#1305: https://github.com/robotframework/SeleniumLibrary/issues/1305
.. _#1331: https://github.com/robotframework/SeleniumLibrary/issues/1331
.. _#1333: https://github.com/robotframework/SeleniumLibrary/issues/1333
.. _#1284: https://github.com/robotframework/SeleniumLibrary/issues/1284
.. _#1307: https://github.com/robotframework/SeleniumLibrary/issues/1307
.. _#1380: https://github.com/robotframework/SeleniumLibrary/issues/1380
.. _#1108: https://github.com/robotframework/SeleniumLibrary/issues/1108
.. _#1273: https://github.com/robotframework/SeleniumLibrary/issues/1273
.. _#1274: https://github.com/robotframework/SeleniumLibrary/issues/1274
.. _#1297: https://github.com/robotframework/SeleniumLibrary/issues/1297
.. _#1308: https://github.com/robotframework/SeleniumLibrary/issues/1308
.. _#1319: https://github.com/robotframework/SeleniumLibrary/issues/1319
.. _#1330: https://github.com/robotframework/SeleniumLibrary/issues/1330
.. _#1336: https://github.com/robotframework/SeleniumLibrary/issues/1336
.. _#1346: https://github.com/robotframework/SeleniumLibrary/issues/1346
.. _#1363: https://github.com/robotframework/SeleniumLibrary/issues/1363
.. _#1372: https://github.com/robotframework/SeleniumLibrary/issues/1372
.. _#1379: https://github.com/robotframework/SeleniumLibrary/issues/1379
.. _#1402: https://github.com/robotframework/SeleniumLibrary/issues/1402
.. _#449: https://github.com/robotframework/SeleniumLibrary/issues/449
.. _#1279: https://github.com/robotframework/SeleniumLibrary/issues/1279
.. _#1301: https://github.com/robotframework/SeleniumLibrary/issues/1301
.. _plugin API: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _EventFiringWebdriver documentation: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _Selenium EventFiringWebdriver: https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html
