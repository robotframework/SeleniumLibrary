Versions
--------

SeleniumLibrary has over the years lived under SeleniumLibrary and
Selenium2Library names and different library versions have supported
different Selenium and Python versions. This is summarized in the table
below and the History_ section afterwards explains the project history
a bit more.

==================================  ==========================  ==========================  ===============
             Project                     Selenium Version             Python Version         Comment
==================================  ==========================  ==========================  ===============
SeleniumLibrary 2.9.2 and earlier   Selenium 1 and 2            Python 2.5-2.7              The original SeleniumLibrary using Selenium RC API.
Selenium2Library 1.8.0 and earlier  Selenium 2 and 3            Python 2.6-2.7              Fork of SeleniumLibrary using Selenium WebDriver API.
SeleniumLibrary 3.0 and 3.1         Selenium 2 and 3            Python 2.7 and 3.3+         Selenium2Library renamed and with Python 3 support and new architecture.
SeleniumLibrary 3.2                 Selenium 3                  Python 2.7 and 3.4+         Drops Selenium 2 support.
SeleniumLibrary 4.0                 Selenium 3                  Python 2.7 and 3.4+         Plugin API and support for event friging webdriver.
SeleniumLibrary 4.1                 Selenium 3                  Python 2.7 and 3.5+         Drops Python 3.4 support.
SeleniumLibrary 4.2                 Selenium 3                  Python 2.7 and 3.5+         Supports only Selenium 3.141.0 or newer.
SeleniumLibrary 4.4                 Selenium 3 and 4            Python 2.7 and 3.6+         New PythonLibCore and dropped Python 3.5 support.
SeleniumLibrary 5.0                 Selenium 3 and 4            Python 3.6+                 Python 2 and Jython support is dropped.
SeleniumLibrary 5.1                 Selenium 3 and 4            Python 3.6+                 Robot Framework 3.1 support is dropped.
Selenium2Library 3.0                Depends on SeleniumLibrary  Depends on SeleniumLibrary  Thin wrapper for SeleniumLibrary 3.0 to ease transition.
==================================  ==========================  ==========================  ===============

History
-------

SeleniumLibrary originally used the Selenium Remote Controller (RC) API.
When Selenium 2 was introduced with the new but backwards incompatible
WebDriver API, SeleniumLibrary kept using Selenium RC and separate
Selenium2Library using WebDriver was forked. These projects contained
mostly the same keywords and in most cases Selenium2Library was a drop-in
replacement for SeleniumLibrary.

Over the years development of the old SeleniumLibrary stopped and also
the Selenium RC API it used was deprecated. Selenium2Library was developed
further and replaced the old library as the de facto web testing library
for Robot Framework.

When Selenium 3 was released in 2016, it was otherwise backwards compatible
with Selenium 2, but the deprecated Selenium RC API was removed. This had two
important effects:

- The old SeleniumLibrary could not anymore be used with new Selenium versions.
  This project was pretty much dead.
- Selenium2Library was badly named as it supported Selenium 3 just fine.
  This project needed a new name.

At the same time when Selenium 3 was released, Selenium2Library was going
through larger architecture changes in order to ease future maintenance and
to make adding Python 3 support easier. With all these big internal and
external changes, it made sense to rename Selenium2Library back to
SeleniumLibrary. This decision basically meant following changes:

- Create separate repository for the `old SeleniumLibrary`_ to preserve
  its history since Selenium2Library was forked.
- Rename Selenium2Library project and the library itself to SeleniumLibrary_.
- Add new Selenium2Library_ project to ease transitioning from Selenium2Library
  to SeleniumLibrary.

All new development is happenning in the SeleniumLibrary project.

Installation of legacy Selenium2Library
---------------------------------------
To install the last legacy Selenium2Library_ version, use this command::

    pip install robotframework-selenium2library==1.8.0

.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium2Library: https://github.com/robotframework/Selenium2Library
.. _Old SeleniumLibrary: https://github.com/robotframework/OldSeleniumLibrary
