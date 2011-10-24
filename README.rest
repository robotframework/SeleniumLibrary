Selenium 2 (WebDriver) library for Robot Framework
==================================================


Introduction
------------

Selenium2Library is a web testing library for Robot Framework
that leverage the `Selenium 2 (WebDriver)`_ libraries from the
Selenium_ project.

It is modeled after (and forked from) the SeleniumLibrary_ library, 
but re-implemented to use Selenium 2 and WebDriver technologies.


Usage
-----

To write tests with Robot Framework and Selenium2Library, 
Selenium2Library must be imported into your Robot test suite.
See `Robot Framework User Guide`_ for more information.


Installation
------------

See INSTALL.txt for installation and uninstallation instructions.


Directory Layout
-----------------

demo/
    A simple demonstration, with an application running on localhost.

doc/
    Keyword documentation.

src/
    Python source code.

test/
    Unit tests and acceptance tests for Selenium2Library source code.

	
.. _Selenium: http://selenium.openqa.org
.. _Selenium 2 (WebDriver): http://seleniumhq.org/docs/03_webdriver.html
.. _SeleniumLibrary: http://code.google.com/p/robotframework-seleniumlibrary/
.. _Robot Framework User Guide: http://code.google.com/p/robotframework/wiki/UserGuide