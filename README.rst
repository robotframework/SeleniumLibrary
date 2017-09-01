SeleniumLibrary
===============

.. contents::
   :local:

Introduction
------------

SeleniumLibrary_ is a web testing library for `Robot Framework`_ that
utilizes the Selenium_ tool internally. The project is hosted on GitHub_
and downloads can be found from PyPI_. See `keyword documentation`_
for available keywords and more information about the library in general.

SeleniumLibrary works with Selenium 2.53.6 or newer, including Selenium 3.
It supports Python 2.7 as well as Python 3.3 or newer.

SeleniumLibrary is based on the `old SeleniumLibrary`_ that was forked to
Selenium2Library_ and then later renamed back to SeleniumLibrary.
See the Versions_ and History_ sections below for more information about
different versions and the overall project history.

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

Running this command installs also the latest Selenium and Robot Framework
versions, but you still need to install `browser drivers`_ separately.
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

An alternative to using ``pip`` is getting the project source code either
from a source distribution at PyPI_ or by cloning the GitHub_ repository,
and installing the code using ``python setup.py install``. This approach
does not install Selenium or other dependencies, so they need to be installed
separately.

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

__ https://seleniumhq.github.io/selenium/docs/api/py/index.html#drivers
__ https://en.wikipedia.org/wiki/PATH_(variable)

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

Versions
--------

SeleniumLibrary has over the years lived under SeleniumLibrary and
Selenium2Library names and different library versions have supported
different Selenium and Python versions. This is summarized in the table
below and the History_ section afterwards explains the project history
a bit more.

==================================  ================  ===================  ===============
             Project                Selenium Version    Python Version         Comment
==================================  ================  ===================  ===============
SeleniumLibrary 2.9.2 and earlier   Selenium 1 and 2  Python 2.5-2.7       The original SeleniumLibrary using Selenium RC API.
Selenium2Library 1.8.0 and earlier  Selenium 2 and 3  Python 2.6-2.7       Fork of SeleniumLibrary using Selenium WebDriver API.
SeleniumLibrary 3.0 and newer       Selenium 2 and 3  Python 2.7 and 3.3+  Selenium2Library renamed and with Python 3 support and new architecture.
Selenium2Library 3.0 and newer      Selenium 2 and 3  Python 2.7 and 3.3+  Thin wrapper for SeleniumLibrary 3.0 to ease transition.
==================================  ================  ===================  ===============

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
.. _PyPI: https://pypi.python.org
.. _GitHub: https://github.com/robotframework/SeleniumLibrary
.. _Keyword Documentation: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
.. _demo project: https://bitbucket.org/robotframework/webdemo
.. _Robot Framework User Guide: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html
.. _Robot Framework installation instructions: https://github.com/robotframework/robotframework/blob/master/INSTALL.rst
.. _robotframework-users: http://groups.google.com/group/robotframework-users
.. _Slack community: https://robotframework-slack-invite.herokuapp.com
.. _issue tracker: https://github.com/robotframework/SeleniumLibrary/issues
.. _Other support forums: http://robotframework.org/#support
