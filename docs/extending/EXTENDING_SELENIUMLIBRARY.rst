Extending SeleniumLibrary
=========================

.. contents::

Introduction
------------
Starting from SeleniumLibrary 3.0, the library has moved to use Robot Framework
`dynamic library API`_. To ease the usage of the dynamic library API, the SeleniumLibrary uses
a `PythonLibCore`_ project to handle the keyword keyword discovery, running the keywords and
other things to related to the dynamic library API. For more details please read the Robot
Framework `dynamic library API`_ documentation.

Public API methods
------------------
All the methods, which are exposed as keywords, are available in the library public API. Generally
keywords are converted to lover case and spaces are converted to underscores. Example `Open Browser`_
is available as ``open_browser``. Please note that method name can be overwritten with the ``@keyword``
decorator, but in the SeleniumLibrary 3.0.0 release does not contain keywords where the keyword
name would differ from the method name (other than the keywords name case).

Methods and attributes which are not keywords in the public API methods
-----------------------------------------------------------------------
The SeleniumLibrary instance also contains methods and attributes which are not keywords but are
useful when extending the SeleniumLibrary. The available methods are:

================  =============================================================
     Method                         Description
================  =============================================================
find_element      Finds first element matching ``locator``.
find_elements     Find all elements matching ``locator``.
register_driver   Add's a ``driver`` to the library WebDriverCache.
run_keyword       Responsible for executing keywords.
failure_occurred  Method that is executed when a SeleniumLibrary keyword fails.
================  =============================================================

Also there are the following public attributes available:

=========================  ================================================================
   Attribute                         Description
=========================  ================================================================
driver                     Current active driver.
timeout                    Default value for ``timeouts`` used with ``Wait ...`` keywords.
implicit_wait              Default value for ``implicit wait`` used when locating elements.
run_on_failure_keyword     Default action for the `run-on-failure functionality`.
screenshot_root_directory  Location where possible screenshots are created
=========================  ================================================================

For more details about the methods, please read the individual method documentation and many
of the attributes are explained in the library `keyword documentation`_.

Extending SeleniumLibrary by pull requests
------------------------------------------
Before making your own extension, private or public, please consider would the extension be
generally useful in the SeleniumLibrary. If the extension would be useful for others, then please
create an issue and a pull request. For more details how SeleniumLibrary project handles the
enhancement requests can be read from the `CONTRIBUTING.rst Enhancement requests`_ chapter.

General prinsibles for extending SeleniumLibrary
------------------------------------------------
The prinsibles described in the Robot Framework User Guide, `Extending existing test libraries`_
chapter also apply when extending the SeleniumLibrary. But because the SeleniumLibrary uses the
`PythonLibCore`_ and the `dynamic library API`_, there are some extra steps which needs to be taken
in account when SeleniumLibrary is extended by using with `inheritace`_ or `dynamically`_.

All methods which should be published as keywords must be decorated with ``@keyword`` decorator.
The ``@keyword`` decorator can be imported in following ways::

    from from SeleniumLibrary.base import keyword

Creating a new library by using inheritance
-------------------------------------------
Perhaps the easiest way to extend the SeleniumLibrary is to inherit the SeleniumLibrary and add
new keywords methods to a new library. The `inheritance example`_ shows how to declare new keyword
`Get Browser Desired Capabilities` and how to overwrite existing `Open Browser` keyword.

The

Creating a new library by getting active library instance
---------------------------------------------------------
* Creating a new library by getting active library instance from Robot Framework.

Extending the SeleniumLibrary dynamically
-----------------------------------------
TO BE DEIFNED


.. _dynamic library API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Open Browser: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Open%20Browser
.. _keyword documentation: https://github.com/robotframework/SeleniumLibrary#keyword-documentation
.. _CONTRIBUTING.rst Enhancement requests: https://github.com/robotframework/SeleniumLibrary/blob/master/CONTRIBUTING.rst#enhancement-requests
.. _Extending existing test libraries: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-existing-test-libraries
.. _inheritace: https://github.com/robotframework/SeleniumLibrary#TO_BE_DEDFINE
.. _dynamically: https://github.com/robotframework/SeleniumLibrary#TO_BE_DEDFINE_2
.. _inheritance example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/examples/inheritance/InheritSeleniumLibrary.py