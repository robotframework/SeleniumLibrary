========================
SeleniumLibrary 6.3.0rc2
========================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 6.3.0rc2 is a new release with
enhancements including minimizing browesr window, waiting on expected conditions,
getting element attribute or properties and bug fixes.

All issues targeted for SeleniumLibrary v6.3.0 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --pre --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==6.3.0rc2

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 6.3.0rc2 was released on Tuesday April 16, 2024. SeleniumLibrary supports
Python 3.8 through 3.11, Selenium 4.14.0 through 4.19.0 and
Robot Framework 5.0.1, 6.1.1 and 7.0.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.3.0


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

- Added ``Minimize Browser Window`` keyword (`#1741`_, rc 1)
  New keyword which minimizes the current browser window.

- Add keywords to fetch differentiated element Attribute or Property (`#1822`_, rc 1)
  The older ``Get Element Attribute`` keyword uses the Selenium getAttribute() method which,
  as `this SauceLabs article <https://saucelabs.com/resources/blog/selenium-4-new-element-attribute-and-property-methods>`_ describes
  "did not actually retrieve the Attribute value." Instead it "figured out what the user
  was most likely interested in between the Attribute value and the Property values and
  returned it." This would mean sometimes it might return an unexpected result. Selenium 4
  introduced newer methods which returns either the attribute or the property as specifically
  asked for.

  It is recommend that one transition to these newer ``Get DOM Attribute`` and ``Get Property``
  keywords.

- Incorporate the expected conditions of Selenium  (`#1827`_, rc 2)
  A new keyword that allows for one to wait on an expected condition.

- Remove deprecation of Press Key keyword (`#1892`_, rc 2)
  The Press Keys keyword was introduced to replace Press Key. Press Key in turn was deprecated
  but I (Ed Manlove failed to remove). Its been noted that both keywords use different underlying
  methods for sending or pressing keys and either one will work in differing situations. So
  instead of removing Press Key, it has been reinstated as a library keyword.

Acknowledgements
================

- `Luciano Martorella <https://github.com/lmartorella>`_ contributing the new
  minimize keyword (`#1741`_, rc 1)
- `Yuri Verweij <https://github.com/yuriverweij>`_  and `Lisa Crispin <https://lisacrispin.com/>`_
  for reviewing changes and addition to Attribute or Property keywords (`#1822`_, rc 1)
- `Noam Manos <https://github.com/manosnoam>`_ for reporting the issues where
  the Open Browser 'Options' object has no attribute '' (`#1877`_, rc 1)
- Yuri for helping update the contribution guide (`#1881`_, rc 1)
- All those who have commented on the deprecation of Press Key keyword (`#1892`_, rc 2)
- Yuri and Lisa for assisting with the addition of Wait For Expected Condition keyword
  and for the Robot Framework Foundation for the ecosystem support (`#1827`_, rc 2)

and **Yuri Verweij, Lisa Crispin, and Tatu Aalto** for their continued support of the library development.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
      - Added
    * - `#1741`_
      - enhancement
      - high
      - Added minimize keyword
      - rc�1
    * - `#1822`_
      - enhancement
      - high
      - Add keywords to fetch differentiated element Attribute or Property
      - rc�1
    * - `#1827`_
      - enhancement
      - high
      - Incorporate the expected conditions of Selenium 
      - rc�2
    * - `#1892`_
      - ---
      - high
      - Remove deprecation of Press Key keyword
      - rc�2
    * - `#1877`_
      - enhancement
      - medium
      - Open Browser 'Options' object has no attribute ''
      - rc�1
    * - `#1881`_
      - ---
      - medium
      - Update contribution guide
      - rc�1

Altogether 6 issues. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av6.3.0>`__.

.. _#1741: https://github.com/robotframework/SeleniumLibrary/issues/1741
.. _#1822: https://github.com/robotframework/SeleniumLibrary/issues/1822
.. _#1827: https://github.com/robotframework/SeleniumLibrary/issues/1827
.. _#1892: https://github.com/robotframework/SeleniumLibrary/issues/1892
.. _#1877: https://github.com/robotframework/SeleniumLibrary/issues/1877
.. _#1881: https://github.com/robotframework/SeleniumLibrary/issues/1881
