========================
SeleniumLibrary 6.5.0rc1
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.5.0rc1 is a new release with
keyword and keyword documentation translations.

All issues targeted for SeleniumLibrary v6.5.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.5.0rc1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.5.0rc1 was released on Monday June 10, 2024. SeleniumLibrary supports
Python 3.8 through 3.11, Selenium 4.20.0 and 4.21.0 and
Robot Framework 5.0.1, 6.1.1 and 7.0.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.5.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Translation documentation (`#1907`_)
  This brings in the ability to translate both the keyword names as well as
  the keyword documentation. Details on how to create translations can be found
  within the keyword documenation. In addtion the introduction of the selib tool
  allows for further enhancement like ``transform`` which will run Robotidy
  alongside a (future) SeleniumLibrary transformer to automatically handle keyword
  deprecations.

Acknowledgements
================

I want to thank

- jeromehuewe for noting the unspecified upper supported Python version (`#1903`_)
- `Tatu Aalto <https://github.com/aaltat>`_ for all the work around bringing in
  the translation documentation functionality and the selib tool (`#1907`_)

I also want to thank `Yuri Verweij <https://github.com/yuriverweij>`_ for his continued
collaboration on maintaining the SeleniumLibrary.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1903`_
      - enhancement
      - medium
      - Specify supported Python version
      - rc�1
    * - `#1907`_
      - enhancement
      - medium
      - Translation documentation
      - rc�1

Altogether 2 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.5.0>`__.

.. _#1903: https://github.com/robotframework/SeleniumLibrary/issues/1903
.. _#1907: https://github.com/robotframework/SeleniumLibrary/issues/1907
