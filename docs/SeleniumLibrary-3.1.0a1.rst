=======================
SeleniumLibrary 3.1.0a1
=======================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.1.0a1 is a new pre release with
support for headless Chrome and Firefox and and allows to pass desired capabilities
to local browsers also when using `Open Browser` keyword.

All issues targeted for SeleniumLibrary v3.1.0 can be found
from the `issue tracker`_.


If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.1.0a1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Add option to start browser headless in Open Browser keyword (`#1014`_, alpha 1)
--------------------------------------------------------------------------------
The `Open Browser` keyword supports starting Chrome and Firefox browsers in headless
mode. This can done be setting the `browser` argument to `headlessfirefox` or
`headlesschrome` values.


Backwards incompatible changes
==============================

Allow Open Browser keyword to pass capabilities also for local browsers (`#550`_, alpha 1)
------------------------------------------------------------------------------------------
The `Open Browser` keyword `desired_capabilities` argument can now be used to configure
a browser when starting a local browser. In the previous releases, the `desired_capabilities`
argument was only used when also the `remote_url` argument was provided. Now this is changed
and `desired_capabilities` argument can be also used configure the browser when running
locally.

Remove deprecated browser attribute from the library public API.  (`#1036`_, alpha 1)
-------------------------------------------------------------------------------------
During the 3.0.0 pre release phase, we did changed some of the public API arguments names,
but we wanted to provide backwards support for the early adopters be keeping some of the
old public API attributes. This attribute was deprecated during pre releases and it
should have been removed during the 3.0.0 final release, but that was forgotten.
The `browser` public API attribute is now removed in this release.


Acknowledgements
================

Many thanks to rubygeek whi adding a `message` param to `Title Should Be` to display custom error message.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1014`_
      - enhancement
      - critical
      - Add option to start browser headless in Open Browser keyword
      - alpha 1
    * - `#1007`_
      - enhancement
      - high
      - Document how to extend the library
      - alpha 1
    * - `#1042`_
      - enhancement
      - medium
      - Add Message attribute to the Page Title Should Be function
      - alpha 1
    * - `#550`_
      - enhancement
      - medium
      - Allow Open Browser keyword to pass capabilities also for local browsers
      - alpha 1
    * - `#1036`_
      - enhancement
      - low
      - Remove deprecated browser attribute from the library public API.
      - alpha 1
    * - `#1040`_
      - enhancement
      - low
      - Move WebDriverCache and WebDriverCreator under same module
      - alpha 1

Altogether 6 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.1.0>`__.

.. _#1014: https://github.com/robotframework/SeleniumLibrary/issues/1014
.. _#1007: https://github.com/robotframework/SeleniumLibrary/issues/1007
.. _#1042: https://github.com/robotframework/SeleniumLibrary/issues/1042
.. _#550: https://github.com/robotframework/SeleniumLibrary/issues/550
.. _#1036: https://github.com/robotframework/SeleniumLibrary/issues/1036
.. _#1040: https://github.com/robotframework/SeleniumLibrary/issues/1040
