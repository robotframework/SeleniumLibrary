=====================
SeleniumLibrary 6.1.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.1.0 is a new release with
some enhancements around timeouts, broadening edge support and removing
deprecated Opera support, and bug fixes.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.1.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.1.0 was released on Wednesday May 3, 2023. SeleniumLibrary supports
Python 3.7+, Selenium 4.0+ and Robot Framework 4.1.3 or higher.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Set Page Load Timeout
---------------------
The ability to set the page load timeout value was added (`#1535`_). This can be done on the Library import.
For example, one could set it to ten seconds, as in,

.. sourcecode:: robotframework

   *** Setting ***
   Library           SeleniumLibrary    page_load_timeout=10 seconds

In addition there are two addition keywords (``Set Selenium Page Load Timeout`` and ``Get Selenium Page Load Timeout``)
which allow for changing the page load timeout within a script. See the keyword documentation for more information.

Duration of mouse movements within Action Chains
------------------------------------------------
Actions chains allow for building up a series of interactions including mouse movements. As to simulate an acutal
user moving the mouse a default duration (250ms) for pointer movements is set. This change (`#1768`_) allows for
the action chain duration to be modified. This can be done on the Library import, as in,

.. sourcecode:: robotframework

   *** Setting ***
   Library           SeleniumLibrary    action_chain_delay=100 milliseconds

or with the setter keyword ``Set Action Chain Delay``. In addition one can get the current duretion with the
new keyword ``Get Action Chain Delay``. See the keyword documentation for more information.

Timeout documentation updated
-----------------------------
The keyword documentation around timeouts was enhanced (`#1738`_) to clarify what the default timeout is
and that the default is used if ``None`` is specified. The changes are, as shown in **bold**,

    The default timeout these keywords use can be set globally either by using the Set Selenium Timeout
    keyword or with the timeout argument when importing the library. **If no default timeout is set
    globally, the default is 5 seconds. If None is specified for the timeout argument in the keywords,
    the default is used.** See time format below for supported timeout syntax.

Edge webdriver under Linux
--------------------------
The executable path to the edge browser has been changed (`#1698`_) so as to support both Windows and
Linux/Unix/MacOS OSes. One should not notice any difference under Windows but under Linux/*nix one will
no longer get an error message saying the Windows executable is missing.

Bug fixes
=========

``None`` argument not correctly converted
-----------------------------------------
There were some issues when using ``None`` as a parameter under certain arguments within the
SeleniumLibrary(`#1733`_). This was due to the type hinting and argument conversions. The underlying
issue was resolved within the PythonLibCore to which we have upgraded to PythonLibCore v3.0.0.

Deprecated features
===================

- Support for the Opera browser was removed from the underlying Selenium Python
  bindings and thus we have removed the deprecated opera support. (`#1786`_)
- *Internal Only:* The library's acceptance tests removed a deprecated rebot
  option. (`#1793`_)

Upcoming Depreciation of Selenium2Library
=========================================

**Please Take Note** - The SeleniumLibrary Team will be depreciating and removing the Selenium2Library
package in an upcoming release. When the underlying Selenium project transitioned, over six years ago,
from distinguishing between the "old" selenium (Selenium 1) and the "new" WebDriver Selenium 2 into
a numerically increasing versioning, this project decided to use the original SeleniumLibrary package
name. As a convenience the Selenium2Library package was made a wrapper around the SeleniumLibrary
package. Due to the issues around upgrading packages and the simple passage of time, it is time to 
depreciate and remove the Selenium2Library package.

*If you are still installing the Selenium2Libary package please transition over, as soon as possible,
to installing the SeleniumLibrary package instead.*

Acknowledgements
================

- `@0xLeon <https://github.com/0xLeon>`_ for suggesting and
  `@robinmatz <https://github.com/robinmatz>`_ for enhancing the page
  load timeout; adding an API to set page load timeout. (`#1535`_)
- `@johnpp143 <https://github.com/johnpp143>`_ for reporting the action chains timeout
  as fixed and unchangeable. `@rasjani <https://github.com/rasjani>`_ for enhancing
  the library import and adding keywords allowing for user to set the Action Chain's
  duration. (`#1768`_)
- `Dave Martin <https://github.com/sparkymartin>`_ for enhancing the documentation
  around Timeouts. (`#1738`_)
- `@tminakov <https://github.com/tminakov>`_ for pointing out the issue around the
  None type and `Tato Aalto <https://github.com/aaltat>`_  and `Pekka Klärck <https://github.com/pekkaklarck>`_
  for enhancing the core and PLC resolving an issue with types. (`#1733`_)
- `@remontees <https://github.com/remontees>`_ for adding support for Edge webdriver under Linux. (`#1698`_)
- `Lassi Heikkinen <https://github.com/Brownies>`_ for assisting in removing deprecated
  opera support (`#1786`_), for enhancing the acceptance tests (`#1788`_), for
  fixing the tests on firefox (`#1808`_), and for removing the deprecated rebot option (`#1793`_).
- `@dotlambda <https://github.com/dotlambda>`_ for pointing out that the
  RemoteDriverServerException was removed from Selenium (`#1804`_)
- `@DetachHead <https://github.com/DetachHead>`_ for fixing `StringIO` import as it was
  removed in robot 5.0 (`#1753`_)

In addition to the acknowledgements above I want to personally thank **Jani Mikkonen** as a co-maintainer of
the SeleniumLibrary and all the support he has given over the years. I also want to thank **Tatu Aalto** for
his continued support and guidance of and advice concerning the SeleniumLibrary. Despite "leaving" the
project, he still is actively helping me to which I again say Kiitos! As I talked about in our Keynote
talk at RoboCon 2023 I have been working on building up the SeleniumLibrary team. I want to acknowledge
the following people who have stepped up and have been starting to take a larger development and
leadership role with the SeleniumLibrary,

**Lassi Heikkinen, Lisa Crispin, Yuri Verweij, and Robin Matz**

Their active participation has made this library significantly better and I appreciate their contributions
and participation.  -- `Ed Manlove <https://github.com/emanlove>`_

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1733`_
      - bug
      - high
      - The Wait Until * keywords don't support a None value for the error parameter
    * - `#1535`_
      - enhancement
      - high
      - Add API to set page load timeout
    * - `#1698`_
      - enhancement
      - high
      - Update webdrivertools.py
    * - `#1738`_
      - enhancement
      - high
      - Suggestion for clarifying documentation around Timeouts
    * - `#1768`_
      - enhancement
      - high
      - Keywords which uses action chains are having a default 250ms timeout which cannot be overriden.
    * - `#1786`_
      - ---
      - high
      - Remove deprecated opera support
    * - `#1785`_
      - bug
      - medium
      - Review Page Should Contain documentation
    * - `#1796`_
      - bug
      - medium
      - atest task loses python interpreter when running with virtualenv under Windows
    * - `#1788`_
      - enhancement
      - medium
      - Acceptance tests: rebot option `--noncritical` is deprecated since RF 4
    * - `#1795`_
      - enhancement
      - medium
      - Microsoft edge webdriver
    * - `#1808`_
      - enhancement
      - medium
      - Fix tests on firefox
    * - `#1789`_
      - ---
      - medium
      - Review workaround for selenium3 bug tests
    * - `#1804`_
      - ---
      - medium
      - RemoteDriverServerException was removed from Selenium
    * - `#1794`_
      - bug
      - low
      - Documentation timing
    * - `#1806`_
      - enhancement
      - low
      - Remove remote driver server exception
    * - `#1807`_
      - enhancement
      - low
      - Rf v5 v6
    * - `#1815`_
      - enhancement
      - low
      - Updated `Test Get Cookie Keyword Logging` with Samesite attribute
    * - `#1753`_
      - ---
      - low
      - fix `StringIO` import as it was removed in robot 5.0
    * - `#1793`_
      - ---
      - low
      - Remove deprecated rebot option

Altogether 19 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.1.0>`__.

.. _#1733: https://github.com/robotframework/SeleniumLibrary/issues/1733
.. _#1535: https://github.com/robotframework/SeleniumLibrary/issues/1535
.. _#1698: https://github.com/robotframework/SeleniumLibrary/issues/1698
.. _#1738: https://github.com/robotframework/SeleniumLibrary/issues/1738
.. _#1768: https://github.com/robotframework/SeleniumLibrary/issues/1768
.. _#1786: https://github.com/robotframework/SeleniumLibrary/issues/1786
.. _#1785: https://github.com/robotframework/SeleniumLibrary/issues/1785
.. _#1796: https://github.com/robotframework/SeleniumLibrary/issues/1796
.. _#1788: https://github.com/robotframework/SeleniumLibrary/issues/1788
.. _#1795: https://github.com/robotframework/SeleniumLibrary/issues/1795
.. _#1808: https://github.com/robotframework/SeleniumLibrary/issues/1808
.. _#1789: https://github.com/robotframework/SeleniumLibrary/issues/1789
.. _#1804: https://github.com/robotframework/SeleniumLibrary/issues/1804
.. _#1794: https://github.com/robotframework/SeleniumLibrary/issues/1794
.. _#1806: https://github.com/robotframework/SeleniumLibrary/issues/1806
.. _#1807: https://github.com/robotframework/SeleniumLibrary/issues/1807
.. _#1815: https://github.com/robotframework/SeleniumLibrary/issues/1815
.. _#1753: https://github.com/robotframework/SeleniumLibrary/issues/1753
.. _#1793: https://github.com/robotframework/SeleniumLibrary/issues/1793
