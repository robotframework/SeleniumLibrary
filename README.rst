SeleniumLibrary
===============

.. contents::
   :local:

Introduction
------------

SeleniumLibrary_ is a web testing library for `Robot Framework`_
that utilizes the Selenium_ tool internally. See `keyword documentation`_
for available keywords and more information about the library in general.

SeleniumLibrary requires Selenium 2.53.6 or newer. It works with Python 2.7
as well as with Python 3.3 or newer.

SeleniumLibrary is based on the `old SeleniumLibrary`_ that was forked to
Selenium2Library_ and then later renamed back to SeleniumLibrary.
See the `History`_ section below for more information about different
versions.

The new SeleniumLibrary is currently in pre-release phase. The final
SeleniumLibrary 3.0 release is planned for early September.

.. image:: https://img.shields.io/pypi/v/robotframework-seleniumlibrary.svg?label=version
   :target: https://pypi.python.org/pypi/robotframework-seleniumlibrary

.. image:: https://img.shields.io/pypi/l/robotframework-seleniumlibrary.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0

.. image:: https://api.travis-ci.org/robotframework/SeleniumLibrary.png
   :target: http://travis-ci.org/robotframework/SeleniumLibrary

Installation
------------

The recommended installation method is using pip_::

    pip install --pre --upgrade robotframework-seleniumlibrary

Notice that the ``--pre`` option is needed to get the current SeleniumLibrary,
not the `old SeleniumLibrary`_, until the final SeleniumLibrary 3.0 is
released. The ``--upgrade`` option can be omitted when installing the
library for the first time.

Those migrating from Selenium2Library_ can install SeleniumLibrary so that
it is exposed also as Selenium2Library::

    pip install --pre --upgrade robotframework-selenium2library

The above command installs the normal SeleniumLibrary as well as a new
Selenium2Library version that is just a thin wrapper to SeleniumLibrary.
That allows importing Selenium2Library in tests while migrating to
SeleniumLibrary.

To install the last legacy Selenium2Library_ version, use this command instead::

    pip install robotframework-selenium2library==1.8.0

See `INSTALL.rst`_ for more details about installation.

Usage
-----

To use SeleniumLibrary in Robot Framework tests, the library needs to
first be imported using the ``Library`` setting as any other library.
The library accepts some import time arguments, which are documented
in the `keyword documentation`_ along with all the keywords provided
by the library.

When using Robot Framework, it is generally recommended to write as
easy-to-understand tests as possible. The keywords provided by
SeleniumLibrary are pretty low level, though, and often require
implementation specific arguments like element locators to be passed
as arguments. It is thus typically a good idea to write tests using
Robot Framework's higher level keywords that utilize SeleniumLibrary
keywords internally. This is illustrated by the following example
where SeleniumLibrary keywords like ``Input Text`` are primarily
used by higher level keywords like ``Input Username``.

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
general see `Robot Framework User Guide`_.

Support
-------

If the provided documentation is not enough, there are various support forums
available:

- `robotframework-users`_ mailing list
- ``#seleniumlibrary`` and ``#seleniumlibrary-dev`` channels in
  Robot Framework `Slack community`_
- SeleniumLibrary `issue tracker`_ for bug reports and concrete enhancement
  requests
- `Other support forums`_ including paid support

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
- Rename Selenium2Library project and the library itself to SeleniumLibrary.
- Add new Selenium2Library_ project to ease transitioning from Selenium2Library
  to SeleniumLibrary.

Going forward, all new development will happen in the new SeleniumLibrary
project.

.. _Robot Framework: http://robotframework.org
.. _Selenium: http://seleniumhq.org
.. _SeleniumLibrary: https://github.com/robotframework/SeleniumLibrary
.. _Selenium2Library: https://github.com/robotframework/Selenium2Library
.. _Old SeleniumLibrary: https://github.com/robotframework/OldSeleniumLibrary
.. _pip: http://pip-installer.org
.. _Keyword Documentation: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
.. _INSTALL.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/INSTALL.rst
.. _BUILD.rst: https://github.com/robotframework/SeleniumLibrary/blob/master/BUILD.rst
.. _demo project: https://bitbucket.org/robotframework/webdemo
.. _Robot Framework User Guide: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
.. _robotframework-users: http://groups.google.com/group/robotframework-users
.. _Slack community: https://robotframework-slack-invite.herokuapp.com
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues
.. _Other support forums: http://robotframework.org/#support
