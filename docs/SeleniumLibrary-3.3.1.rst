=====================
SeleniumLibrary 3.3.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.3.1 is a new hotfix release with
two fixes.

All issues targeted for SeleniumLibrary v3.3.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.3.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.3.1 was released on Friday January 4, 2019. SeleniumLibrary supports
Python 2.7 and 3.4+, Selenium 3.4+ (Although the supported Selenium version depends on
the use browser version) and Robot Framework 2.9.2, 3.0.4 and 3.1.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.3.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Open Browser fails if desired capabilities is a dict (`#1277`_)
---------------------------------------------------------------
The SeleniumLibrary 3.3.0 introduced a bug which causes `Open Browser` to fail
when desired_capabilities argument was defined as a dictionary.

When using remote_url and not defining desired_capabilities the Open Browser keyword fails (`#1280`_)
-----------------------------------------------------------------------------------------------------
The SeleniumLibrary 3.3.0 introduced a bug which made desired_capabilities argument
mandatory when remote_url argument was also defined in the `Open Browser` keyword.
The desired_capabilities is an optional parameter and if it is not defined, the
`Selenium browser specific capabilities`_ is used instead.

There is small possibility that this change is backwards incompatible, because in the
3.2.0 release the Selenium browser specific capabilities and user defined
desired_capabilities where joined. In this release, if the user defined desired_capabilities
are found, then they are used as is and are not joined with the Selenium browser
specific capabilities. Now users must define all capabilities which are needed to
launch the browser. This change is done to because of the problems found in the `#1243`_.


Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1277`_
      - bug
      - critical
      - Open Browser fails if desired capabilities is a dict
    * - `#1280`_
      - bug
      - critical
      - When using remote_url and not defining desired_capabilities the Open Browser keyword fails

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.3.1>`__.

.. _#1277: https://github.com/robotframework/SeleniumLibrary/issues/1277
.. _#1280: https://github.com/robotframework/SeleniumLibrary/issues/1280
.. _Selenium browser specific capabilities: https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.desired_capabilities.html#module-selenium.webdriver.common.desired_capabilities
.. _#1243: https://github.com/robotframework/SeleniumLibrary/issues/1243
