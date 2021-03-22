=====================
SeleniumLibrary 5.1.2
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.1.2 is a new release with
bug fixs type type conversion bugs with Robot Framework 4.0.

All issues targeted for SeleniumLibrary v5.1.2 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.1.2

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.1.2 was released on Monday March 22, 2021. SeleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.2.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.2


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

"Element Attribute Should Have Value" no longer supports ${None} (`#1708`_)
---------------------------------------------------------------------------
There was bugs in type conversion definitions with Robot Framework 4.0.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1708`_
      - bug
      - high
      - "Element Attribute Should Have Value" no longer supports ${None}

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.1.2>`__.

.. _#1708: https://github.com/robotframework/SeleniumLibrary/issues/1708
