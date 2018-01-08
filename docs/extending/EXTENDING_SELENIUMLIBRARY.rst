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
chapter also apply when extending the SeleniumLibrary. There are two different ways to
extend the SeleniumLibrary.
1) Create a library which also the existing SeleniumLibrary keywords, example by using `inheritace`_.
2) Create library which contains only new keywords.

When creating a library, which also includes the existing SeleniumLibrary keywords, there are
extra steps which needs to be taken account because SeleniunLibrary uses `PythonLibCore`_
and the `dynamic library API`_. All methods which should be published as keywords must be
decorated with ``@keyword`` decorator. The ``@keyword`` decorator can be imported in following way::

    from from SeleniumLibrary.base import keyword

Keywords should be inside of a ``class`` and the ``add_library_components`` method
must be called to add keywords. The ``add_library_components`` method is inherited from the
`PythonLibCore`_ project and the project provides easy way to write libraries with
dynamic or hybrid library API.

Creating a new library by using inheritance
-------------------------------------------
Perhaps the easiest way to extend the SeleniumLibrary is to inherit the SeleniumLibrary and add
new or replace existing keywords methods to a new library. The `inheritance example`_ shows how
to declare new keyword ``Get Browser Desired Capabilities`` and how to overwrite existing
``Open Browser`` keyword.

Because the ``InheritSeleniumLibrary`` class foes not overwrite the SeleniumLibrary init method, the
``add_library_components`` is called automatically. Then the ``InheritSeleniumLibrary`` class methods
which are  decorated with ``@keyword`` decorator are added to the ``InheritSeleniumLibrary``
library keywords. Also existing keywords from SeleniumLibrary are added as library keywords.

Creating a new library from multiple classes
--------------------------------------------
Decomposition is a good way to split library to smaller name spaces and it usually eases the
library testing. The `decomposition example`_ shows how the ``Get Browser Desired Capabilities``
and ``Open Browser`` keywords can divided to own classes.

The example also shows the usage of the ``context`` object and the `LibraryComponent`_ class.
The ``context`` object is a instance of the SeleniunLibrary which provides access the the
SeleniumLibrary methods, example to the Selenium WebDriver instance. Without the ``context`` object,
the ``BrowserKeywords``  and ``DesiredCapabilitiesKeywords`` classes would not have access to the
SeleniunLibrary methods and objects.

The ``LibraryComponent`` wrapper class, which provides easier shortcuts the ``context`` object methods
and example provides general logging methods. Example the Selenium WebDriver instance in the context in:
``self.ctx.driver``, but the ``LibraryComponent`` provides a shortcut and it can be accessed with
``self.driver``


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
.. _decomposition example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/examples/decomposition/Decomposition.py
.. _LibraryComponent: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py