Selenium 2 (WebDriver) library for Robot Framework
==================================================

.. image:: https://api.travis-ci.org/rtomac/robotframework-selenium2library.png
    :target: http://travis-ci.org/rtomac/robotframework-selenium2library

.. image:: https://img.shields.io/pypi/v/robotframework-selenium2library.svg
    :target: https://pypi.python.org/pypi/robotframework-selenium2library

.. image:: https://img.shields.io/pypi/dm/robotframework-selenium2library.svg
    :target: https://pypi.python.org/pypi/robotframework-selenium2library

.. image:: https://img.shields.io/pypi/l/robotframework-selenium2library.svg
    :target: http://www.apache.org/licenses/LICENSE-2.0

.. image:: https://robotframework-slack.herokuapp.com/badge.svg
	:target: https://robotframework-slack.herokuapp.com
	:alt: Slack channel


Introduction
------------

Selenium2Library is a web testing library for `Robot Framework`_
that leverages the `Selenium 2 (WebDriver)`_ libraries from the
Selenium_ project.

It is modeled after (and forked from) the SeleniumLibrary_ library,
but re-implemented to use Selenium 2 and WebDriver technologies.

- More information about this library can be found on the Wiki_ and in the `Keyword Documentation`_.
- Installation information is found in the `INSTALL.rst`_ file.
- Developer information is found in `BUILD.rst`_ file.


Installation
------------

Using ``pip``
'''''''''''''

The recommended installation method is using
`pip <http://pip-installer.org>`__::

    pip install robotframework-selenium2library

The main benefit of using ``pip`` is that it automatically installs all
dependencies needed by the library. Other nice features are easy upgrading
and support for un-installation::

    pip install --upgrade robotframework-selenium2library
    pip uninstall robotframework-selenium2library

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the Selenium tool used by the library::

    pip install robotframework-selenium2library==1.4.1
    pip install --upgrade selenium
    pip install selenium==2.34

Proxy configuration
'''''''''''''''''''

If you are behind a proxy, you can use ``--proxy`` command line option
or set ``http_proxy`` and/or ``https_proxy`` environment variables to
configure ``pip`` to use it. If you are behind an authenticating NTLM proxy,
you may want to consider installing `CNTML <http://cntlm.sourceforge.net>`__
to handle communicating with it.

For more information about ``--proxy`` option and using pip with proxies
in general see:

- http://pip-installer.org/en/latest/usage.html
- http://stackoverflow.com/questions/9698557/how-to-use-pip-on-windows-behind-an-authenticating-proxy
- http://stackoverflow.com/questions/14149422/using-pip-behind-a-proxy

Manual installation
'''''''''''''''''''

If you do not have network connection or cannot make proxy to work, you need
to resort to manual installation. This requires installing both the library
and its dependencies yourself.

1) Make sure you have `Robot Framework installed
   <http://code.google.com/p/robotframework/wiki/Installation>`__.

2) Download source distributions (``*.tar.gz``) for the library and its
   dependencies:

   - https://pypi.python.org/pypi/robotframework-selenium2library
   - https://pypi.python.org/pypi/selenium
   - https://pypi.python.org/pypi/decorator

3) Extract each source distribution to a temporary location.

4) Go each created directory from the command line and install each project
   using::

       python setup.py install

If you are on Windows, and there are Windows installers available for
certain projects, you can use them instead of source distributions.
Just download 32bit or 64bit installer depending on your system,
double-click it, and follow the instructions.

Directory Layout
----------------

demo/
    A simple demonstration, with an application running on localhost

doc/
    Keyword documentation

src/
    Python source code


Usage
-----

To write tests with Robot Framework and Selenium2Library,
Selenium2Library must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.


Running the Demo
----------------

The demo directory contains an easily executable demo for Robot Framework
using Selenium2Library. To run the demo, run::

    python demo/rundemo.py

E.g.::

	python demo/rundemo.py demo/login_tests

Getting Help
------------
The `user group for Robot Framework`_ is the best place to get help. Consider including in the post:

- Full description of what you are trying to do and expected outcome
- Version number of Selenium2Library, Robot Framework, and Selenium
- Traceback or other debug output containing error information

.. _Robot Framework: http://robotframework.org
.. _Selenium: http://selenium.openqa.org
.. _Selenium 2 (WebDriver): http://seleniumhq.org/docs/03_webdriver.html
.. _SeleniumLibrary: http://code.google.com/p/robotframework-seleniumlibrary/
.. _Wiki: https://github.com/rtomac/robotframework-selenium2library/wiki
.. _Keyword Documentation: http://rtomac.github.com/robotframework-selenium2library/doc/Selenium2Library.html
.. _INSTALL.rst: https://github.com/rtomac/robotframework-selenium2library/blob/master/INSTALL.rst
.. _BUILD.rst: https://github.com/rtomac/robotframework-selenium2library/blob/master/BUILD.rst
.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuide
.. _user group for Robot Framework: http://groups.google.com/group/robotframework-users
