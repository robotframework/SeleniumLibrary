Selenium test library for Robot Framework
=========================================

Introduction
------------

SeleniumLibrary is a test library for Robot Framework that enables testing
of web applications. As the name suggests, it uses Selenium_ via Selenium-RC_
internally. Currently, not all features of Selenium are implemented in 
SeleniumLibrary, but most of them are quite trivial to implement when someone 
needs them.


Usage
-----

To run tests with Robot Framework and SeleniumLibrary following things 
must be done

- SeleniumLibrary must be taken into use in Robot test data.
  See `Robot Framework user guide`__ for more information.
- Selenium server must be started with command 
  ``java -jar [path_to_server]/selenium_server.jar``, 
  where [path_to_server] depends on platform. On Windows it will be 
  '[PythonDir]\\Lib\\site-packages\\SeleniumLibrary\\lib' and on Linux it is 
  '/usr/lib/python[version]/site-packages/SeleniumLibrary/lib' 


__ http://code.google.com/p/robotframework/wiki/UserGuide


Installation
------------

See INSTALLATION.txt for installation and uninstallation instructions.


Directory Layout
-----------------

demo/
    A simple demonstration, with an application running on localhost.

doc/
    Keyword documentation.

src/
    Python source code.

test/
    Acceptance tests for keywords using Robot Framework.


.. _Selenium: http://selenium.openqa.org
.. _Selenium-RC: http://selenium-rc.openqa.org

