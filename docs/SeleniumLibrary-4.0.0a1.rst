=======================
SeleniumLibrary 4.0.0a1
=======================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.0.0a1 is a new release with
new plugin API and support for Selenium EventFiringWebdriver.There are also
other enhancements and bug fixes.

All issues targeted for SeleniumLibrary v4.0.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.0.0a1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.0.0a1 was released on Thursday April 18, 2019. SeleniumLibrary supports
Python 2.7 and 3.4+, Selenium 3.8.2 and
Robot Framework 3.0.4 and 3.1.1.

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

Deprecated features
===================

Deprecate loudly all silently deprecated keywords  (`#1273`_, alpha 1)
----------------------------------------------------------------------
All keywords which where silently deprecated in the previous release, will now
cause a deprecated warning.

Deprecate sizzle selector strategy  (`#1336`_, alpha 1)
-------------------------------------------------------
Sizzle selector is deprecated.

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

Altogether 18 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.0.0>`__.

.. _#1292: https://github.com/robotframework/SeleniumLibrary/issues/1292
.. _#1303: https://github.com/robotframework/SeleniumLibrary/issues/1303
.. _#1304: https://github.com/robotframework/SeleniumLibrary/issues/1304
.. _#1305: https://github.com/robotframework/SeleniumLibrary/issues/1305
.. _#1284: https://github.com/robotframework/SeleniumLibrary/issues/1284
.. _#1307: https://github.com/robotframework/SeleniumLibrary/issues/1307
.. _#1108: https://github.com/robotframework/SeleniumLibrary/issues/1108
.. _#1273: https://github.com/robotframework/SeleniumLibrary/issues/1273
.. _#1274: https://github.com/robotframework/SeleniumLibrary/issues/1274
.. _#1297: https://github.com/robotframework/SeleniumLibrary/issues/1297
.. _#1308: https://github.com/robotframework/SeleniumLibrary/issues/1308
.. _#1330: https://github.com/robotframework/SeleniumLibrary/issues/1330
.. _#1336: https://github.com/robotframework/SeleniumLibrary/issues/1336
.. _#1346: https://github.com/robotframework/SeleniumLibrary/issues/1346
.. _#1363: https://github.com/robotframework/SeleniumLibrary/issues/1363
.. _#449: https://github.com/robotframework/SeleniumLibrary/issues/449
.. _#1279: https://github.com/robotframework/SeleniumLibrary/issues/1279
.. _#1301: https://github.com/robotframework/SeleniumLibrary/issues/1301
.. _plugin API: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _EventFiringWebdriver documentation: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _Selenium EventFiringWebdriver: https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html
