========================
SeleniumLibrary 6.4.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.4.0rc1 is a release candidate
with enhancements around driver configuration and logging, printing pages as pdf,
and some bug fixes.

All issues targeted for SeleniumLibrary v6.4.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.4.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.4.0rc1 was released on Sunday May 19, 2024. SeleniumLibrary supports
Python 3.8 through 3.11, Selenium 4.16.0 through 4.21.0 and
Robot Framework 5.0.1, 6.1.1 and 7.0.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.4.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Add new selenium 4 print page as PDF functionality (`#1824`_)
  The print page as pdf functionality within Selenium 4 has been added into SeleniumLibrary
  with a new keyword. See the keyword documentation for usage.
- Add driver Service Class into Open Browser (`#1900`_)
  Selenium has shifted from a couple arguments for configuring the driver settings into the new
  Service class. As with the options argument these changes allows for service class to be set
  using a simlar string format. More information can be found in the `Open Browser` keyword
  documentation and newly rearranged Introduction.
- Add warning about frame deselection when using `Page Should Contain` keyword. (`#1894`_)
  In searching through the page, the `Page Should Contain` keyword will select and search
  through frames. Thus it silently changes the frame context. Added warning within the keyword
  documentation noting as such.
- Wrong Type Hint on some keywords. (`locator: Union[WebElement, None, str]`) (`#1880`_)
  Several type hints on locator arguments denoted the argument allowed for none when indeed
  they did not. This corrects those type hints.

Deprecated features
===================

- Start Deprecation and Removal of Selenium2Library (deep) references/package (`#1826`_)
  Removed references and instructions regarding Selenium2Library; moving some to an archived
  VERSIONS.rst top level documentation.

Acknowledgements
================

- We would like to thank `René Rohner <https://github.com/Snooz82>`_ for discovering the
  incorrect type hints on some keywords. (`locator: Union[WebElement, None, str]`) (`#1880`_)
- `SamMaksymyshyn <https://github.com/SamMaksymyshyn>`_,  `Yuri Verweij <https://github.com/yuriverweij>`_
  and `Lisa Crispin <https://lisacrispin.com/>`_ for helping to model and design the new
  print page as PDF functionality (`#1824`_)
- `Tatu Aalto <https://github.com/aaltat>`_ for modeling and reviewing the added driver Service Class into Open Browser (`#1900`_)
- Start Deprecation and Removal of Selenium2Library (deep) references/package (`#1826`_)
- .. and Tatu for fixing the internal test run on Mac (`#1899`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1880`_
      - bug
      - high
      - Wrong Type Hint on some keywords. (`locator: Union[WebElement, None, str]`)
    * - `#1824`_
      - enhancement
      - high
      - Add new selenium 4 print page as PDF functionality
    * - `#1894`_
      - enhancement
      - high
      - Add warning about frame deselection when using `Page Should Contain` keyword.
    * - `#1900`_
      - enhancement
      - high
      - Add driver Service Class into Open Browser
    * - `#1826`_
      - ---
      - high
      - Start Deprecation and Removal of Selenium2Library (deep) references/package
    * - `#1899`_
      - ---
      - ---
      - Make test run on Mac

Altogether 6 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.4.0>`__.

.. _#1880: https://github.com/robotframework/SeleniumLibrary/issues/1880
.. _#1824: https://github.com/robotframework/SeleniumLibrary/issues/1824
.. _#1894: https://github.com/robotframework/SeleniumLibrary/issues/1894
.. _#1900: https://github.com/robotframework/SeleniumLibrary/issues/1900
.. _#1826: https://github.com/robotframework/SeleniumLibrary/issues/1826
.. _#1899: https://github.com/robotframework/SeleniumLibrary/issues/1899
