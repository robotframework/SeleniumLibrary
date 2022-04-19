SeleniumLibrary
===============

.. contents::

Introduction
------------

SeleniumLibrary_ is a web testing library for `Robot Framework`_ that
utilizes the Selenium_ tool internally. The project is hosted on GitHub_
and downloads can be found from PyPI_.

SeleniumLibrary works with Selenium 3 and 4. It supports Python 3.6 or
newer. In addition to the normal Python_ interpreter, it works also
with PyPy_.

SeleniumLibrary is based on the `old SeleniumLibrary`_ that was forked to
Selenium2Library_ and then later renamed back to SeleniumLibrary.
See the Versions_ and History_ sections below for more information about
different versions and the overall project history.

.. image:: https://img.shields.io/pypi/v/robotframework-seleniumlibrary.svg?label=version
   :target: https://pypi.python.org/pypi/robotframework-seleniumlibrary
   
.. image:: https://img.shields.io/pypi/dm/robotframework-seleniumlibrary.svg
   :target: https://pypi.python.org/pypi/robotframework-seleniumlibrary

.. image:: https://img.shields.io/pypi/l/robotframework-seleniumlibrary.svg
   :target: https://www.apache.org/licenses/LICENSE-2.0

.. image:: https://github.com/robotframework/SeleniumLibrary/workflows/SeleniumLibrary%20CI/badge.svg
    :target: https://github.com/robotframework/SeleniumLibrary/actions?query=workflow%3A%22SeleniumLibrary+CI%22

Keyword Documentation
---------------------
See `keyword documentation`_ for available keywords and more information
about the library in general.

Installation
------------

The recommended installation method is using pip_::

    pip install --upgrade robotframework-seleniumlibrary

Running this command installs also the latest Selenium and Robot Framework
versions, but you still need to install `browser drivers`_ separately.
The ``--upgrade`` option can be omitted when installing the library for the
first time.

Those migrating from Selenium2Library_ can install SeleniumLibrary so that
it is exposed also as Selenium2Library::

    pip install --upgrade robotframework-selenium2library

The above command installs the normal SeleniumLibrary as well as a new
Selenium2Library version that is just a thin wrapper to SeleniumLibrary.
That allows importing Selenium2Library in tests while migrating to
SeleniumLibrary.

To install the last legacy Selenium2Library_ version, use this command instead::

    pip install robotframework-selenium2library==1.8.0

With recent versions of ``pip`` it is possible to install directly from the
GitHub_ repository. To install latest source from the master branch, use
this command::

    pip install git+https://github.com/robotframework/SeleniumLibrary.git

Please note that installation will take some time, because ``pip`` will
clone the SeleniumLibrary_ project to a temporary directory and then
perform the installation.

See `Robot Framework installation instructions`_ for detailed information
about installing Python and Robot Framework itself. For more details about
using ``pip`` see `its own documentation <pip_>`__.

Browser drivers
---------------

After installing the library, you still need to install browser and
operating system specific browser drivers for all those browsers you
want to use in tests. These are the exact same drivers you need to use with
Selenium also when not using SeleniumLibrary. More information about
drivers can be found from `Selenium documentation`__.

The general approach to install a browser driver is downloading a right
driver, such as ``chromedriver`` for Chrome, and placing it into
a directory that is in PATH__. Drivers for different browsers
can be found via Selenium documentation or by using your favorite
search engine with a search term like ``selenium chrome browser driver``.
New browser driver versions are released to support features in
new browsers, fix bug, or otherwise, and you need to keep an eye on them
to know when to update drivers you use.

Alternatively, you can use a tool called WebdriverManager__ which can
find the latest version or when required, any version of appropriate
webdrivers for you and then download and link/copy it into right
location. Tool can run on all major operating systems and supports
downloading of Chrome, Firefox, Opera & Edge webdrivers.

Here's an example:

.. code:: bash

      pip install webdrivermanager
      webdrivermanager firefox chrome --linkpath /usr/local/bin



__ https://seleniumhq.github.io/selenium/docs/api/py/index.html#drivers
__ https://en.wikipedia.org/wiki/PATH_(variable)
__ https://github.com/omenia/webdrivermanager

Usage
-----

To use SeleniumLibrary in Robot Framework tests, the library needs to
first be imported using the ``Library`` setting as any other library.
The library accepts some import time arguments, which are documented
in the `keyword documentation`_ along with all the keywords provided
by the library.

When using Robot Framework, it is generally recommended to write as
easy-to-understand tests as possible. The keywords provided by
SeleniumLibrary is pretty low level, though, and often require
implementation-specific arguments like element locators to be passed
as arguments. It is thus typically a good idea to write tests using
Robot Framework's higher-level keywords that utilize SeleniumLibrary
keywords internally. This is illustrated by the following example
where SeleniumLibrary keywords like ``Input Text`` are primarily
used by higher-level keywords like ``Input Username``.

.. code:: robotframework

    *** Settings ***
    Documentation     Simple example using SeleniumLibrary.
    Library           SeleniumLibrary

    *** Variables ***
    ${LOGIN URL}      http://localhost:7272
    ${BROWSER}        Chrome

    *** Test Cases ***
    Valid Login
        Open Browser To Login Page
        Input Username    demo
        Input Password    mode
        Submit Credentials
        Welcome Page Should Be Open
        [Teardown]    Close Browser

    *** Keywords ***
    Open Browser To Login Page
        Open Browser    ${LOGIN URL}    ${BROWSER}
        Title Should Be    Login Page

    Input Username
        [Arguments]    ${username}
        Input Text    username_field    ${username}

    Input Password
        [Arguments]    ${password}
        Input Text    password_field    ${password}

    Submit Credentials
        Click Button    login_button

    Welcome Page Should Be Open
        Title Should Be    Welcome Page


The above example is a slightly modified version of an example in a
`demo project`_ that illustrates using Robot Framework and SeleniumLibrary.
See the demo for more examples that you can also execute on your own
machine. For more information about Robot Framework test data syntax in
general see the `Robot Framework User Guide`_.

Extending SeleniumLibrary
-------------------------
Before creating your own library which extends the ``SeleniumLibrary``, please consider would
the extension be also useful also for general usage. If it could be useful also for general
usage, please create a new issue describing the enhancement request and even better if the
issue is backed up by a pull request.

If the enhancement is not generally useful, example solution is domain specific, then the
SeleniumLibrary offers public APIs which can be used to build its own plugins and libraries.
Plugin API allows us to add new keywords, modify existing keywords and modify the internal
functionality of the library. Also new libraries can be built on top of the
SeleniumLibrary. Please see `extending documentation`_ for more details about the
available methods and for examples how the library can be extended.

Community
---------

If the provided documentation is not enough, there are various community channels
available:

- `robotframework-users`_ mailing list
- ``#seleniumlibrary`` and ``#seleniumlibrary-dev`` channels in
  Robot Framework `Slack community`_
- `Robot Framework forum`_ has channel for SeleniumLibrary.
- SeleniumLibrary `issue tracker`_ for bug reports and concrete enhancement
  requests
- `Other community channels`_ including paid support

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

Going forward, all new development will happen in the new SeleniumLibrary
project.

.. _Robot Framework: https://robotframework.org
.. _Selenium: https://www.seleniumhq.org/
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium2Library: https://github.com/robotframework/Selenium2Library
.. _Old SeleniumLibrary: https://github.com/robotframework/OldSeleniumLibrary
.. _pip: http://pip-installer.org
.. _PyPI: https://pypi.python.org/pypi/robotframework-seleniumlibrary
.. _GitHub: https://github.com/robotframework/SeleniumLibrary
.. _Keyword Documentation: https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
.. _Python: https://python.org
.. _PyPy: https://pypy.org
.. _Jython: https://jython.org/
.. _IronPython: https://ironpython.net/
.. _demo project: https://github.com/robotframework/WebDemo
.. _Robot Framework User Guide: https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
.. _Robot Framework installation instructions: https://github.com/robotframework/robotframework/blob/master/INSTALL.rst
.. _robotframework-users: https://groups.google.com/group/robotframework-users
.. _extending documentation: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst
.. _Slack community: https://robotframework-slack-invite.herokuapp.com
.. _Robot Framework forum: https://forum.robotframework.org/
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues
.. _Other community channels: https://robotframework.org/#community
