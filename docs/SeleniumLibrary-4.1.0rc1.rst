========================
SeleniumLibrary 4.1.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 4.1.0rc1 is a new release with
making URL argument optional in Open Browser keyword and allowing configuring
how Click Element clicks the element. There are two major fixes in the release,
Table Keywords searched elements also outside of the table and if output
directory contained { and }  characters the Open Browser and Capture *
Screenshot keywords would fail.


All issues targeted for SeleniumLibrary v4.1.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==4.1.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 4.1.0rc1 was released on Sunday October 13, 2019. SeleniumLibrary
supports Python 2.7 and 3.5+, Selenium 3.8.2 and Robot Framework 3.0.4 and 3.1.2.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

"Table Should Contain" does not work properly (`#1482`_, rc 1)
--------------------------------------------------------------
The Table Header Should Contain , Table Footer Should Contain and Table Should Contain
keywords also searched from whole page and not only from the table. This also caused
performance hit, if the page contained lots of elements.

Many thanks for Pawci3oo spotting the problem.

Drop Python 3.4 support in SeleniumLibrary 4.1 (`#1409`_, rc 1)
---------------------------------------------------------------
SeleniumLibrary 4.1 has dropped support for Python 3.4, because Python 3.4 is in
end of life.

SeleniumLibrary aims to raise minimum supported Python 3.6 and it is likely next
major release drops support for Python 3.5. At least Python 3.5 support is dropped
when Python 3.5 reaches end of life in 2020.

Acknowledgements
================

Update Open Browser keyword documentation to better demonstrate how to use Selenium options (`#1461`_, rc 1)
------------------------------------------------------------------------------------------------------
Open Browser keyword documentation was updated to provide better examples how to use
Selenium Options. Many thanks to JonKoser for providing the PR.

Should have an ActionChain click for Click Element keyword (`#1463`_, rc 1)
---------------------------------------------------------------------------
Click Element now also supports clicking element with ActionChain click. This is
configurable option in the keyword and must be enabled with the action_chain argument.

Many thanks to JonKoser for providing the PR.

Users should not be required to define a URL to Open Browser keyword. (`#1464`_, rc 1)
--------------------------------------------------------------------------------------
The url argument is not optional in the Open Browser keyword. This helps users who
do not want to navigate browser when the browser is opened.

Many thanks to JonKoser for providing the PR.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1482`_
      - bug
      - critical
      - "Table Should Contain" does not work properly
      - rc 1
    * - `#1409`_
      - enhancement
      - high
      - Drop Python 3.4 support in SeleniumLibrary 4.1
      - rc 1
    * - `#1452`_
      - bug
      - medium
      - If output dir contains multiple { and } characters pairs, then opening browser with Firefox will fail.
      - rc 1
    * - `#1461`_
      - enhancement
      - medium
      - Update Open Browser keyword documentation to better demonstrate how to use Selenium options
      - rc 1
    * - `#1463`_
      - enhancement
      - medium
      - Should have an ActionChain click for Click Element keyword
      - rc 1
    * - `#1464`_
      - enhancement
      - medium
      - Users should not be required to define a URL to Open Browser keyword.
      - rc 1

Altogether 6 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av4.1.0>`__.

.. _#1482: https://github.com/robotframework/SeleniumLibrary/issues/1482
.. _#1409: https://github.com/robotframework/SeleniumLibrary/issues/1409
.. _#1452: https://github.com/robotframework/SeleniumLibrary/issues/1452
.. _#1461: https://github.com/robotframework/SeleniumLibrary/issues/1461
.. _#1463: https://github.com/robotframework/SeleniumLibrary/issues/1463
.. _#1464: https://github.com/robotframework/SeleniumLibrary/issues/1464
