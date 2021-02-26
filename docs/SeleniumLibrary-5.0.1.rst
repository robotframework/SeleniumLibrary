=====================
SeleniumLibrary 5.0.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 5.0.1 is a new release with
bug fixes to stub file and using sting NONE to disable run on failure functionality.

All issues targeted for SeleniumLibrary v5.0.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==5.0.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 5.0.1 was released on Friday February 26, 2021. SeleniumLibrary supports
Python 3.6+, Selenium 3.141.0+ and Robot Framework 3.1.2+.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================
Not supported syntax in __init__.pyi (`#1685`_)
-----------------------------------------------
The stub file contained invalid Python syntax and prevented proper IDE usage.

Register Keyword to Run on Failure Bug or Doc fix (`#1686`_)
------------------------------------------------------------
There was regression in 5.0.0 release and string NONE could not be used
to disable run on failure functionality.

Add missing methods to stub file (`#1690`_)
-------------------------------------------
All missing methods in stub file are now defined.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1685`_
      - bug
      - high
      - Not supported syntax in __init__.pyi
    * - `#1686`_
      - bug
      - high
      - Register Keyword to Run on Failure Bug or Doc fix
    * - `#1690`_
      - bug
      - high
      - Add missing methods to stub file

Altogether 3 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av5.0.1>`__.

.. _#1685: https://github.com/robotframework/SeleniumLibrary/issues/1685
.. _#1686: https://github.com/robotframework/SeleniumLibrary/issues/1686
.. _#1690: https://github.com/robotframework/SeleniumLibrary/issues/1690
