=====================
SeleniumLibrary 3.1.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.1.0 is a new pre release with
support for headless Chrome and Firefox and and allows to pass desired capabilities
to local browsers also when using `Open Browser` keyword.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.1.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.1.0 was released on Thursday February 15, 2018.

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
`headlesschrome` values. Using the headless mode requires Selenium 3.8.0 or greater.

Backwards incompatible changes
==============================

Allow Open Browser keyword to pass capabilities also for local browsers (`#550`_, alpha 1)
------------------------------------------------------------------------------------------
The `Open Browser` keyword `desired_capabilities` argument can now be used to configure
a browser when starting a local browser. In the previous releases, the `desired_capabilities`
argument was used only when the `remote_url` argument was provided. Now this now is changed
and `desired_capabilities` argument can be also used to configure browser running locally.

Remove deprecated browser attribute from the library public API.  (`#1036`_, alpha 1)
-------------------------------------------------------------------------------------
During the 3.0.0 prerelease phase, we did changed some of the public API arguments names.
But we wanted to provide backwards support for the early adopters by keeping some of the
old public API attributes in place. This attribute was deprecated during prereleases and it
should have been removed during the 3.0.0 final release, but that was forgotten.
The `browser` public API attribute is now removed in this release.


Acknowledgements
================

Many thanks to rubygeek for adding a `message` param to `Title Should Be` keyword to display
custom error message.

Many thanks to rubygeek, for providing the PR for the ignore case enhancement.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1014`_
      - enhancement
      - critical
      - Add option to start browser headless in Open Browser keyword
    * - `#1007`_
      - enhancement
      - high
      - Document how to extend the library
    * - `#1042`_
      - enhancement
      - medium
      - Add Message attribute to the Page Title Should Be function
    * - `#550`_
      - enhancement
      - medium
      - Allow Open Browser keyword to pass capabilities also for local browsers
    * - `#849`_
      - enhancement
      - medium
      - Verify string regardless of case
    * - `#1036`_
      - enhancement
      - low
      - Remove deprecated browser attribute from the library public API.
    * - `#1040`_
      - enhancement
      - low
      - Move WebDriverCache and WebDriverCreator under same module

Altogether 7 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.1.0>`__.

.. _#1014: https://github.com/robotframework/SeleniumLibrary/issues/1014
.. _#1007: https://github.com/robotframework/SeleniumLibrary/issues/1007
.. _#1042: https://github.com/robotframework/SeleniumLibrary/issues/1042
.. _#550: https://github.com/robotframework/SeleniumLibrary/issues/550
.. _#849: https://github.com/robotframework/SeleniumLibrary/issues/849
.. _#1036: https://github.com/robotframework/SeleniumLibrary/issues/1036
.. _#1040: https://github.com/robotframework/SeleniumLibrary/issues/1040
