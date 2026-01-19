========================
SeleniumLibrary 6.7.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.7.0rc1 is a new release with
some minor enhancements and bug fixes.

All issues targeted for SeleniumLibrary v6.7.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.7.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.7.0rc1 was released on Sunday December 29, 2024. SeleniumLibrary supports
Python 3.8 through 3.13, Selenium 4.24.0 through 4.27.1 and
Robot Framework 6.1.1 and 7.1.1.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.7.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Fixed _find_by_data_locator when more than one colon was within the locator. If one
  used the data strategy and the locator had additional colon in it the locator parser
  would incorrectly parse the locator. This has been fixed in this release. (`#1924`_)
- Make SeleniumLibrary support one or more translations from same localisation project (`#1917`_)

Acknowledgements
================

We want to thank

- `Markus Leben <https://github.com/markus-leben>`_ for discovering, reporting, and fixing
  the _find_by_data_locator issue (`#1924`_)
- `The Great Simo <https://github.com/TheGreatSimo>`_ and `Pavel <https://github.com/PavelMal>`_
  for updating the requirements (`#1849`_)
- `iarmhi <https://github.com/iarmhi>`_ for correcting an error the docs (`#1913`_)

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1924`_
      - bug
      - high
      - Fix _find_by_data_locator
    * - `#1917`_
      - enhancement
      - high
      - Make SeleniumLibrary support one or more tranlsation from same localisation project
    * - `#1849`_
      - ---
      - medium
      - Update the rerequirements
    * - `#1913`_
      - bug
      - low
      - Remove unneeded 'send_' in docs
    * - `#1925`_
      - ---
      - ---
      - Latest Versions Oct2024

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.7.0>`__.

.. _#1924: https://github.com/robotframework/SeleniumLibrary/issues/1924
.. _#1917: https://github.com/robotframework/SeleniumLibrary/issues/1917
.. _#1849: https://github.com/robotframework/SeleniumLibrary/issues/1849
.. _#1913: https://github.com/robotframework/SeleniumLibrary/issues/1913
.. _#1925: https://github.com/robotframework/SeleniumLibrary/issues/1925
