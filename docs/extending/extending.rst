Extending SeleniumLibrary
=========================

.. contents::

Introduction
============
SeleniumLibrary offers three main ways to creating new functionality for SeleniumLibrary: Plugin
API, `EventFiringWebDriver`_ and building new libraries on top the SeleniumLibrary (later
referred as extending SeleniumLibrary.) Plugin API and extending SeleniumLibrary allows
similar access to the SeleniumLibrary public API and offers their own pros and cons for
building custom functionality on top the SeleniumLibrary. The EventFiringWebDriver offers
listener-like interface to the Selenium API. The plugin API and EventFiringWebDriver
are new in SeleniumLibrary 4.0.

Plugin API
----------
SeleniumLibrary offers plugins as a way to modify, add library keywords and modify some of the internal
functionality without creating new library or hacking the source code. Plugins can be only loaded in the
library import, with the `plugins`_ argument and SeleniumLibrary does not offer way to unload the
plugins from the SeleniumLibrary. Creating new plugins is more strict than creating new libraries, but
plugins allows more access to the methods that are used to implement the keywords.

EventFiringWebDriver
--------------------
The EventFiringWebDriver is an listener type of API offered by the Selenium. The EventFiringWebDriver
allows to listen Selenium API calls and allows users to fire events before and after Selenium API methods.
Refer the to the Selenium `EventFiringWebDriver`_ documentation what Selenium API methods are
supported and how to EventFiringWebDriver works.

Extending SeleniumLibrary
-------------------------
As with any Robot Framework Python library, new libraries can be build on top of the SeleniumLibrary
by inheriting the SeleniumLibrary, getting active library instance from Robot Framework or by other
means which are available from Python or from Robot Framework. Building new libraries allows
library creator freedom to choose which keywords new library offers and more flexibility how
new libraries are created than what the plugin API offers.

Contributing to SeleniumLibrary project
---------------------------------------
Before making your own plugin or library on top of the SeleniumLibrary, private or public,
please consider if the plugin or extension be generally useful in the SeleniumLibrary. If the
plugin or extension would be useful for others, then please create an issue and perhaps a pull
request. More details on how the SeleniumLibrary project handles the enhancement requests can
be found in the CONTRIBUTING.rst `Enhancement requests`_ chapter.

Public API
==========
The plugin API and extending SeleniumLibrary have same access to the SeleniumLibrary public API.
All the methods, which are exposed as keywords, are available in the SeleniumLibrary public API.
Generally keywords are converted to lower case and spaces are converted to underscores. For
example, the `Open Browser`_ keyword is available as ``open_browser`` method. The method name can
be overwritten with the ``@keyword`` decorator, but the SeleniumLibrary 4.0.0 release does not
contain keywords where the keyword name would differ from the method name (other than the keyword
case.) Please note that keywords created by the plugins may not follow these rules and it is good
to verify the method name from the plugin API source.

Methods and attributes which are not keywords but are available in the public API
---------------------------------------------------------------------------------
The SeleniumLibrary also contains methods and attributes which are not keywords, but are
useful when creating plugin or extending the SeleniumLibrary. The available methods are:

================  ================================================================================
     Method                         Description
================  ================================================================================
find_element      Finds first element matching ``locator``.
find_elements     Find all elements matching ``locator``.
get_keyword_tags  Responsible for returning keywords tags for Robot Framework dynamic library API.
register_driver   Add's a Selenium ``driver`` to the library WebDriverCache.
run_keyword       Responsible for executing keywords by Robot Framework dynamic library API.
failure_occurred  Method that is executed when a SeleniumLibrary keyword fails.
================  ================================================================================

Also there are the following public attributes available:

=========================  ================================================================
   Attribute                         Description
=========================  ================================================================
driver                     Current active driver.
event_firing_webdriver     Reference to a class implementing event firing selenium support.
timeout                    Default value for ``timeouts`` used with ``Wait ...`` keywords.
implicit_wait              Default value for ``implicit wait`` used when locating elements.
run_on_failure_keyword     Default action for the `run-on-failure functionality`.
screenshot_root_directory  Location where possible screenshots are created
=========================  ================================================================

For more details about the methods, please read the individual method documentation and many
of the attributes are explained in the library `keyword documentation`_. please note that
plugins may alter the functionality of the method or attributes and documentation applies
only for the core SeleniumLibrary.

Initialisation order
====================
When instance is created from the SeleniumLibrary, example when library is imported in the
test data, there is an order in the initialisation. At first all classes defining SeleniumLibrary
keywords are discovered. As a second event, discovery for the EventFiringWebDriver is done.
At third event, plugins are discovered. As a last event, keywords are found from SeleniumLibrary
classes and plugins. Because plugins are discovered last, they may example alter the
EventFiringWebDriver. Consult the plugin's documentation for more details.

Plugins
=======
SeleniumLibrary offers plugins as a way to modify, add library keywords and modify some of the internal
functionality without creating new library or hacking the source code. See `plugin example`_ how plugins
can be implemented.

Importing plugins
-----------------
Importing plugins is similar when importing Robot Framework `libraries`_. It is possible import plugin
with using `physical path`_ or with `plugin name`_ exactly in same way as importing libraries in
Robot Framework. SeleniumLibrary plugins are searched from the same `module search path`_ as
Robot Framework searches libraries. It is only possible to import plugins written in Python, other
programming languages or Robot Framework test data is not supported. Like with Robot Framework
library imports, plugin names are case sensitive and spaces are not supported in the plugin name.
It is possible to import multiple plugins at the same time by separating plugins with comma. It
is possible to have space before and after the comma. Plugins are imported in the order they defined
in the `plugins`_ argument. If two or more plugins declare the same keyword or modify the same
method/attribute in the SeleniumLibrary, the last plugin to perform the changes will overwrite
the changes made by other plugins. Example of plugin imports::

    | Library | SeleniumLibrary | plugins=${CURDIR}/MyPlugin.py                   | # Imports plugin with physical path |
    | Library | SeleniumLibrary | plugins=plugins.MyPlugin, plugins.MyOtherPlugin | # Import two plugins with name      |


Plugin arguments
----------------
When SeleniumLibrary creates instances from the plugin classes, it will by default initiate the class
with a single argument, called ``ctx`` (context). ``ctx`` is the instance of the SeleniummLibrary and
it provides access to the SeleniumLibrary `Public API`_.

It is also possible to provide optional arguments to the plugins. Arguments must be separated with a
semicolon from the plugin. SeleniumLibrary will not convert arguments to any specific type and everything
is by default unicode. Plugin is responsible for converting the argument to proper types. Example of
importing plugin with arguments::

    | Library | SeleniumLibrary | plugins=plugins.Plugin;ArgOne;ArgTwo | # Import two plugins with two arguments: ArgOne and ArgTwo |

It is also possible to provide variable number of arguments and keywords arguments. Named arguments
must be defined first, variable number of arguments as second and keywords arguments as last.
All arguments must be separated with semicolon. Example if plugin __init__ is defined like this::

    class Plugin(LibraryComponent):

        def __init__(self, ctx, arg, *varargs, **kwargs):
            # Code to implement the plugin.

Then, for example, it is possible to plugin with these arguments::

    | Library | SeleniumLibrary | plugins=plugins.Plugin;argument1;varg1;varg2;kw1=kwarg1;kw2=kwarg2 |

Then the ``argument1`` is given the ``arg`` in the ``__init__``. The ``varg1`` and ``varg2`` variable
number arguments are given to the ``*varargs`` argument in the  ``__init__``. Finally, the ``kw1=kwarg1``
and ``kw2=kwarg2`` keyword arguments are given to the ``**kwargs`` in the  ``__init__``. As in Python,
there can be zero or more variable number and keyword arguments.

Plugin API
----------
Generally speaking, plugins are not any different from the classes that are used to implement keyword
in the SeleniumLibrary. Example like with `BrowserManagementKeywords`_ class inherits the `LibraryComponent`_
and uses ``@keyword`` decorator to mark which methods are exposed as keywords.

Plugins must be implemented as Python classes and plugins must inherit the SeleniumLibrary `LibraryComponent`_
class. Plugin __init__ must support at least one argument: ``ctx``. Also optional arguments are supported, see
`Plugin arguments`_ for more details how to provide optional arguments to plugins.

SeleniumLibrary uses Robot Framework `dynamic library API`_. The main difference, when compared to libraries
using dynamic library API, is that plugins are not responsible for implementing the dynamic library API.
SeleniumLibrary is handling the dynamic library API requirements towards Robot Framework. For plugins
this means that methods that implements keywords, must be decorated with ``@keyword`` decorator. The ``@keyword``
decorator can be imported from Robot Framework and used in the following way::

    from robot.api.deco import keyword

    class Plugin(LibraryComponent):

        @keyword
        def keyword(self):
            self.driver....  # More code here to implement the keyword

Handling plugins failures
-------------------------
SeleniumLibrary does not suppress exception raised during plugin import or during keywords discovery from the
plugins. In this case the whole SeleniumLibrary import will fail and SeleniumLibrary keywords can not be used
from that import.

By default when exceptions raised by SeleniumLibrary keywords will trigger the `run on failure`_ functionality,
this also applies keywords created or modified by the plugins. But it must be noted that plugins can alter the
SeleniumLibrary run on failure functionality and refer to the plugin documentation for further details.

LibraryComponent
----------------
Although ``ctx`` provides access to the SeleniumLibrary `Public API`_, the `LibraryComponent`_ provides more
methods and attributes and also an IDE friendly access to the plugin API, Example currently active
browser can be found from ``self.ctx.driver``, the ``LibraryComponent`` exposes the browser as:
``self.driver`` and most IDE can discover the completion automatically. Plugin classes must inherit
the ``LibraryComponent``.

The following methods are available from the ``LibraryComponent`` class:

========================  =================================================================================================================================================
          Method                         Description
========================  =================================================================================================================================================
find_element               Finds first element matching ``locator``.
find_elements              Find all elements matching ``locator``.
is_text_present            Returns True if text is present in the page.
is_element_enabled         Returns True if element is enabled.
is_visible                 Returns True if element is visible.
log_source                 Calls method defining the `Log Source` keyword.
assert_page_contains       Raises AssertionError if element is not found from the page.
assert_page_not_contains   Raises AssertionError if element is found from the page.
get_timeout                By default returns SeleniumLibrary ``timeout`` argument value. With argument converts string with Robot Framework ``timestr_to_secs`` to seconds.
info                       Wrapper to ``robot.api.logger.info`` method.
debug                      Wrapper to ``robot.api.logger.debug`` method.
warn                       Wrapper to ``robot.api.logger.warn`` method.
log                        Wrapper to ``robot.api.logger.write`` method.
========================  =================================================================================================================================================

Also following attributes are available from the ``LibraryComponent`` class:

======================  ==============================================================================
      Attribute                                          Description
======================  ==============================================================================
driver                  Currently active browser/WebDriver instance in the SeleniumLibrary.
drivers                 `Cache`_ for the opened browsers/WebDriver instances.
element_finder          Read/write attribute for the `ElementFinder`_ instance.
ctx                     Instance of the SeleniumLibrary.
log_dir                 Folder where output files are written.
event_firing_webdriver  Read/write attribute for the SeleniumLibrary `EventFiringWebDriver`_ instance.
======================  ==============================================================================

See the `SeleniumLibrary init`_, the `LibraryComponent`_ and the `ContextAware`_ classes for further
implementation details.

Generating keyword documentation
--------------------------------
To separate keywords which are added or modified by plugins, SeleniumLibrary will add ``plugin`` `keyword tag`_
to all keywords added or modified from plugins. When SeleniumLibrary keyword documentation, with plugins,
is generated by `libdoc`_ it is easy to separate keywords which are added or modified by plugins. Keyword
documentation can be example generated by following command::

    python -m robot.libdoc SeleniumLibrary::plugins=/path/to/Plugin.py ./SeleniumLibraryWithPlugin.html


EventFiringWebDriver support
============================
The `EventFiringWebDriver`_ is an listener type of API offered by the Selenium. In practice ``EventFiringWebDriver``
offers way to intercept Selenium API call, made by SeleniumLibrary or by other library keywords and fire
separate Selenium events. Events can be fired before and after Selenium API call.

SeleniumLibrary offers support for Selenium ``EventFiringWebDriver`` listener class by providing possibility
to import the listener class by `event_firing_webdriver`_ argument. Importing ``EventFiringWebDriver``
is similar when importing Robot Framework `libraries`_. It is possible import ``EventFiringWebDriver``
with using `physical path`_ or with `name`_ exactly in same way as importing libraries in
Robot Framework. ``EventFiringWebDriver`` class is searched from the same `module search path`_ as
Robot Framework searches libraries. It is only possible to import ``EventFiringWebDriver`` class
written in Python, other programming languages or Robot Framework test data is not supported. Like with
Robot Framework library imports, ``EventFiringWebDriver`` class name is case sensitive and spaces
are not supported in the class name. It is possible to import only one ``EventFiringWebDriver`` class.
Example of ``EventFiringWebDriver`` imports::

    | Library | SeleniumLibrary | event_firing_webdriver=${CURDIR}/MyListener.py | # Imports EventFiringWebDriver with physical path |

Refer the to the Selenium `EventFiringWebDriver`_ documentation what Selenium API methods are
supported and how to EventFiringWebDriver works. Also there is simple
`EventFiringWebDriver example`_ for more details.

Extending SeleniumLibrary
=========================
Starting from SeleniumLibrary 3.0, the library has moved to use Robot Framework
`dynamic library API`_. To ease the usage of the dynamic library API, the SeleniumLibrary uses
a `PythonLibCore`_ project to handle the most the dynamic library API requirements, except running
the keyword and providing keywords tags. For more details please about the dynamic library API,
read the Robot Framework `dynamic library API`_ documentation.


General principles for extending SeleniumLibrary
------------------------------------------------
The principles described in the Robot Framework User Guide, `Extending existing test libraries`_
chapter also apply when extending SeleniumLibrary. There are two different ways to
extend the SeleniumLibrary.

1) Create a library which also contains the existing SeleniumLibrary keywords, example by using `inheritance`_.
2) Create library which contains only new keywords.

When creating a library, which also includes the existing SeleniumLibrary keywords, there are
extra steps which needs to be taken account, because SeleniumLibrary uses `PythonLibCore`_
and the `dynamic library API`_. All methods which should be published as keywords must be
decorated with the ``@keyword`` decorator. The ``@keyword`` decorator can be imported in
the following way::

    from robot.api.deco import keyword

Keywords should be inside of a ``class`` and the ``add_library_components`` method
must be called to add keywords. The ``add_library_components`` method is inherited from the
`PythonLibCore`_ project and the method must contain list of classes which contain the
new keywords.

Creating a new library by using inheritance
-------------------------------------------
Perhaps the easiest way to extend the SeleniumLibrary is to inherit the SeleniumLibrary and add
new keywords methods to a new library. The `inheritance example`_ shows how to declare a new
keyword ``Get Browser Desired Capabilities`` and how to overwrite the existing ``Open Browser``
keyword.

Because the ``InheritSeleniumLibrary`` class does not overwrite the SeleniumLibrary ``init``
method, the ``add_library_components`` is called automatically. Then the ``InheritSeleniumLibrary``
class methods which are  decorated with ``@keyword`` decorator are added to the
``InheritSeleniumLibrary`` library keywords. Also existing keywords from SeleniumLibrary are added as library keywords.

Because the methods are no longer  directly available in the SeleniumLibrary class, it's not
possible to call the original method example like this::

    super(ClassName, self).open_browser(url, browser, alias, remote_url,
                                        desired_capabilities, ff_profile_dir)

Instead user must call the method from the class instance which implements the keyword, example::

    browser_management = BrowserManagementKeywords(self)
    browser_management.open_browser(url, 'chrome')

Creating a new library from multiple classes
--------------------------------------------
Decomposition is a good way to split library into smaller namespaces and it usually eases the
testing of the library. The `decomposition example`_ shows how the ``Get Browser Desired Capabilities``
and ``Open Browser`` keywords can be divided into their own classes.

The example also shows the usage of the ``ctx`` (context) object and the `LibraryComponent`_ class.
The ``ctx`` object is an instance of the SeleniumLibrary which provides access to the
SeleniumLibrary `Public API`_ for the ``BrowserKeywords``  and ``DesiredCapabilitiesKeywords`` classes.

The ``LibraryComponent`` is a wrapper class, which provides easier shortcuts to the ``ctx`` object
methods and the example provides general logging methods. Example the Selenium WebDriver instance
in the context: ``self.ctx.driver``, but the ``LibraryComponent`` provides a shortcut and it can be
accessed with: ``self.driver``


Creating a new library by getting active library instance
---------------------------------------------------------
Getting the active library instance provides a way to create a new library that does not
automatically contain keywords from the SeleniumLibrary. This eases the name space
handling and if only new keywords are created, the user does not have to prefix the keywords
with the library name. This way also allows users to freely choose the Robot Framework `library API`_.
The `instance example`_ shows a way to get the active SeleniumLibrary from the Robot Framework.
The example shows how to declare ``Get Browser Desired Capabilities`` and ``Open Browser`` keywords
in the new library and the `instance example`_ uses the `static keyword API`_ to declare new
keywords.

.. _EventFiringWebDriver: https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver
.. _plugins: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Importing
.. _Enhancement requests: https://github.com/robotframework/SeleniumLibrary/blob/master/CONTRIBUTING.rst#enhancement-requests
.. _dynamic library API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api
.. _PythonLibCore: https://github.com/robotframework/PythonLibCore
.. _Open Browser: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Open%20Browser
.. _keyword documentation: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
.. _libraries: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#importing-libraries
.. _plugin example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/plugin_api/readme.rst
.. _physical path: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-physical-path-to-library
.. _plugin name: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-library-name
.. _module search path: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path
.. _BrowserManagementKeywords: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/keywords/browsermanagement.py
.. _run on failure: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Run-on-failure%20functionality
.. _Cache: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/keywords/webdrivertools.py
.. _ElementFinder: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/locators/elementfinder.py
.. _SeleniumLibrary init: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/__init__.py
.. _ContextAware: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/context.py
.. _keyword tag: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#keyword-tags
.. _libdoc: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#library-documentation-tool-libdoc
.. _event_firing_webdriver: http://robotframework.org/SeleniumLibrary/SeleniumLibrary.html#Importing
.. _EventFiringWebDriver example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/event_firing_webdriver/readme.rst
.. _Extending existing test libraries: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#extending-existing-test-libraries
.. _name: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-library-name
.. _inheritance: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending/inheritance/InheritSeleniumLibrary.py
.. _inheritance example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending/inheritance/InheritSeleniumLibrary.py
.. _decomposition example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending/decomposition/Decomposition.py
.. _instance example: https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending/get_instance/GetSeleniumLibraryInstance.py
.. _LibraryComponent: https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py
.. _library API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#different-test-library-apis
.. _static keyword API: http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#creating-static-keywords
