=====================
SeleniumLibrary 6.8.0
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.8.0 is a new release with
screenshot enhancements and minor bug and documentation fixes. This version
adds support for Python 3.14.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.8.0

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.8.0 was released on Saturday October 4, 2025. SeleniumLibrary supports
Python 3.8 through 3.14, Selenium 4.28.1 through 4.34.2 and
Robot Framework 6.1.1 and 7.3.2.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.8.0
.. _Selenium Documentation: https://www.selenium.dev/documentation/selenium_manager/

.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Option to return embed screenshot while using Capture Page Screenshot (`#1923`_).
  One is now given the additional option to return the screenshot as base64 string to be used
  elsewhere in the log html. If the screenshot root directory is specified as `BASE64`
  then the screenshot string is returned. See the `Capture Page Screenshot` keyword doc
  for more information and example to place returned image in the log file.
- Update README.rst 'Browser drivers' section (`#1938`_)
  With the (long past) addition of Selenium Manager within the selenium package, the documentation
  on browser drivers was outdated and incorrect. This works to correct that. For more
  information about Selenium Manager and handling browsers and drivers see the
  `Selenium Documentation`_ on the topic.
- Loosen restriction on the upper Python version allowing Python 3.14 (`#1949`_)

Acknowledgements
================

I want to thank the following people for helping getting out this release ..

- `Hrutvik Jagtap <https://github.com/hsj51>`_  and `Shiva Prasad Adirala <https://github.com/adiralashiva8>`_
  for contributing to the base64 image screenshot functionality (`#1923`_)
- `Corey Goldberg <https://github.com/cgoldberg>`_ for updating the README concerning Selenium Manager (`#1938`_)
- `DetachHead <https://github.com/DetachHead>`_ for reporting the deprecated `is_string` error messages (`#1940`_)
- `Rudolf <https://github.com/Houbein>`_ for pushing for the addition of Python 3.14 (`#1949`_)

I also want to thank `Yuri Verweij <https://github.com/yuriverweij>`_, `Lassi Heikkinen <https://github.com/Brownies>`_,
and `Tatu Aalto <https://github.com/aaltat>`_ for their ongoing contributions and support.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1923`_
      - enhancement
      - high
      - Return base64 image in case of EMBED
    * - `#1938`_
      - enhancement
      - high
      - Update README.rst 'Browser drivers' section
    * - `#1940`_
      - enhancement
      - high
      - remove usages of deprecated `is_string`
    * - `#1949`_
      - enhancement
      - high
      - Python 3.14
    * - `#1939`_
      - ---
      - ---
      - Return screenshot as base64 string and embed into log

Altogether 5 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.8.0>`__.

.. _#1923: https://github.com/robotframework/SeleniumLibrary/issues/1923
.. _#1938: https://github.com/robotframework/SeleniumLibrary/issues/1938
.. _#1940: https://github.com/robotframework/SeleniumLibrary/issues/1940
.. _#1949: https://github.com/robotframework/SeleniumLibrary/issues/1949
.. _#1939: https://github.com/robotframework/SeleniumLibrary/issues/1939
