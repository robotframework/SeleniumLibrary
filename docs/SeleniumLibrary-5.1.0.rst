=====================
SeleniumLibrary 5.1.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.1.0 is a new release with
enhancements to properly support argument conversion enhancements in Robot
Framework 4.0. Support for Robot Framework 3.1 is dropped.

All issues targeted for SeleniumLibrary v5.1.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.1.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.1.0 was released on Friday February 26, 2021. SeleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.2.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Offer support for Robot Framework 4.0 (`#1692`_)
------------------------------------------------
There was several issues to support Robot Framework 4.0 enhanced argument conversion. These issues
should be now fixed.

Drop support for RF 3.1 (`#1693`_)
----------------------------------
Support for Robot Framework 3.1 is dropped. It will most likely work, but official support
is not offered anymore, because RF 4.0 is soon ready.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1692`_
      - bug
      - critical
      - Offer support for Robot Framework 4.0
    * - `#1693`_
      - enhancement
      - critical
      - Drop support for RF 3.1

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.0>`__.

.. _#1692: https://github.com/robotframework/SeleniumLibrary/issues/1692
.. _#1693: https://github.com/robotframework/SeleniumLibrary/issues/1693
