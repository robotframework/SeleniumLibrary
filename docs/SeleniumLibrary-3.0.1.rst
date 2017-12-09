=====================
SeleniumLibrary 3.0.1
=====================


.. default-role:: code


SeleniumLibrary_ is a web testing library for `Robot Framework`_ that utilizes
the Selenium_ tool internally. SeleniumLibrary 3.0.1 is a new release with
one bugfix. The release 3.0.0 contained bug with `Wait Until Element Is Not Visible`
keyword, if element was not in the DOM, the element was considered as visible.

All issues targeted for SeleniumLibrary v3.0.1 can be found
from the `issue tracker`_.

If you have pip_ installed, just run

::

   pip install --upgrade robotframework-seleniumlibrary

to install the latest available release or use

::

   pip install robotframework-seleniumlibrary==3.0.1

to install exactly this version. Alternatively you can download the source
distribution from PyPI_ and install it manually.

SeleniumLibrary 3.0.1 was released on Saturday December 9, 2017.

.. _Robot Framework: http://robotframework.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium: http://seleniumhq.org
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.1


.. contents::
   :depth: 2
   :local:

Most important enhancements
===========================

Change between 1.8.0 and 3.0.0 when using Wait Until Element Is Not Visible. In 3.0.0 element is consider visible if the element does not exist in the DOM. (`#1008`_)
----------------------------------------------------------------------------------------------------------------------------------------------------------------------
In the 1.8.0 release the element is considered as not visible when the element does not
exist in  the DOM. But there was a change in the 3.0.0 release and element is considered
as visible if the element is not int he DOM. This is now fixed and element is not
visible also when the element is not in the DOM.

Full list of fixes and enhancements
===================================

.. list-table::
    :header-rows: 1

    * - ID
      - Type
      - Priority
      - Summary
    * - `#1008`_
      - bug
      - critical
      - Change between 1.8.0 and 3.0.0 when using Wait Until Element Is Not Visible. In 3.0.0 element is consider visible if the element does not exist in the DOM.

Altogether 1 issue. View on the `issue tracker <https://github.com/robotframework/SeleniumLibrary/issues?q=milestone%3Av3.0.1>`__.

.. _#1008: https://github.com/robotframework/SeleniumLibrary/issues/1008
