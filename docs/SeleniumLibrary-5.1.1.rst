=====================
SeleniumLibrary 5.1.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.1.1 is a new release with
bug fixes to Open Browser keyword ff_profile_dir argument type conversion.

All issues targeted for SeleniumLibrary v5.1.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.1.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.1.1 was released on Sunday March 14, 2021. SeleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.2.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Open Browser Firefox profile path argument types are not correct (`#1703`_)
---------------------------------------------------------------------------
Open Browser keyword ff_profile_dir argument did convert argument incorrectly
if the argument value was Python FirefoxProfile instance. This is now fixed
in this release.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1703`_
      - bug
      - high
      - Open Browser Firefox profile path argument types are not correct

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.1>`__.

.. _#1703: https://github.com/robotframework/SeleniumLibrary/issues/1703
