SeleniumLibrary
===============

.. image:: https://api.travis-ci.org/robotframework/SeleniumLibrary.png
    :target: http://travis-ci.org/robotframework/SeleniumLibrary

.. image:: https://img.shields.io/pypi/v/robotframework-seleniumlibrary.svg?label=version
    :target: https://pypi.python.org/pypi/robotframework-seleniumlibrary

.. image:: https://img.shields.io/pypi/l/robotframework-seleniumlibrary.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0

Introduction
------------

SeleniumLibrary is a web testing library for `Robot Framework`_ that utilizes
the popular Selenium_ tool internally. See the `keyword documentation`_
for available keywords and `wiki`_ for some more general information
about the library.

SeleniumLibrary is based on the `old SeleniumLibrary`_ that was forked to
Selenium2Library and then later renamed back to SeleniumLibrary.

The new SeleniumLibrary is currently in pre-release phase. The final
SeleniumLibrary 3.0 release is planned for early September.

The Selenium2Library 1.8.0 keyword `documentation is also available`_

Installation
------------

The recommended installation method is using pip_::

    pip install --pre robotframework-seleniumlibrary

Notice that ``--pre`` is needed to get the current SeleniumLibrary,
not the `old SeleniumLibrary`_, until the final SeleniumLibrary 3.0
is released.

To install the old Selenium2Library, use this command instead::

    pip install robotframework-selenium2library

See `INSTALL.rst`_ for more details about installation.

Usage
-----

To write tests with Robot Framework and SeleniumLibrary,
SeleniumLibrary must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.

A demo project illustrating how to use this library can be found from:
https://bitbucket.org/robotframework/webdemo

Differences between SeleniumLibrary versions
============================================

Selenium versions
-----------------

There are three main version of Selenium: `Selenium Remote Control`_ (RC or Selenium
1), `Selenium 2`_ and `Selenium 3`_.

The Selenium RC works only with major browsers that has JavaScript enabled. It
also requires a selenium server which automatically launches and kills browsers.
The Selenium RC is not anymore maintained by the Selenium.

The Selenium 2 supports Selenium RC and Selenium WebDirver. Selenium WebDriver
does not need separate server to launch and kill servers and it has simpler
and more concise API then Selenium RC.

The Selenium 3 supports only Selenium WebDirver and has started to adopt
the `W3C WebDriver`_ specification. If excluding the dropped Selenium RC
support, Selenium 3 is a drop in replacement for Selenium 2.

Selenium support in Robot Framework
-----------------------------------

The SeleniumLibrary version up to 2.9.2 supports only the Selenium RC.

The Selenium2Library versions up to 1.8.0 and from SeleniumLibrary 3.0.0
version onwards supports Selenium 2 and 3

Python support
--------------

The SeleniumLibrary version up to 2.9.2 and the Selenium2Library
versions up to 1.8.0 supports only Python 2

Starting from SeleniumLibrary 3.0.0 version onwards Python 2 and Python 3.3+ are
supported.

History
-------

The SeleniumLibrary up to 2.9.2 version was actively developed by using the
Selenium RC. When the Selenium 2 reached mature enough state, the Selenium2Library
was forked from SeleniumLibary and modified to use the Selenium WebDriver. The
SeleniumLibrary, with Selenium RC support, active development ended
when Selenium RC was deprecated.

When Selenium 3 was released it was adopted by the Selenium2Library
because Selenium 3 is a drop in replacement for Selenium 2. Also the
Selenium2Library relies only on the WebDriver technology and it did not
need any changes to support Selenium 3.

In release 3.0.0, it was decided to rename the Selenium2Library back to
SeleniumLibrary. This was done because the name more resembles what the library
supports and enables.

Support
-------

Best places to ask for support:

- `robotframework-users`_ mailing list
- ``#seleniumlibrary`` channel on `Robot Framework Slack`_

When asking for help or reporting problems, please include the following
information:

- Full description of what you are trying to do and expected outcome
- Version number of SeleniumLibrary, Selenium, and Robot Framework
- Version number of the browser and the browser driver
- Traceback or other debug output containing error information

.. _Robot Framework: http://robotframework.org
.. _Selenium: http://seleniumhq.org
.. _Old SeleniumLibrary: https://github.com/robotframework/OldSeleniumLibrary/
.. _pip: http://pip-installer.org
.. _Wiki: https://github.com/robotframework/SeleniumLibrary/wiki
.. _Keyword Documentation: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
.. _INSTALL.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/INSTALL.rst
.. _BUILD.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/BUILD.rst
.. _Robot Framework User Guide: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
.. _Selenium Remote Control: http://www.seleniumhq.org/projects/remote-control/
.. _Selenium 2: http://www.seleniumhq.org/projects/webdriver/
.. _Selenium 3: http://www.seleniumhq.org/projects/webdriver/
.. _W3C WebDriver: https://www.w3.org/TR/webdriver/
.. _robotframework-users: http://groups.google.com/group/robotframework-users
.. _Robot Framework Slack: https://robotframework-slack-invite.herokuapp.com/
.. _documentation is also available: http://robotframework.org/SeleniumLibrary/Selenium2Library.html
