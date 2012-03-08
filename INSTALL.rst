Selenium2Library Installation
=============================


Preconditions
-------------

Selenium2Library supports all Python and Jython interpreters supported by the
Robot Framework and the `Selenium Python Bindings`_. The Selenium Python Bindings
are the most restrictive, and as of now require Python 2.6 or Python 2.7.

Selenium2Library depends on a few other Python libraries, but all of those
will be installed automatically when Selenium2Library is installed.


Installing from PyPI
--------------------

Selenium2Library is available in the Python Package Index (PyPI_). To install,
you need to have `easy_install`_ installed. Then run::

	easy_install robotframework-selenium2library


Installing from source
----------------------

The source code can be retrieved either as a source distribution or as a clone
of the main source repository. The installer requires Python version 2.4 or
newer. Selenium Library is installed from source by typing following command::

    python setup.py install

In most linux systems, you need to have root privileges for installation.

Uninstallation is achieved by deleting the installation directory and its
contents from the file system. The default installation directory is
`[PythonLibraries]/site-packages/Selenium2Library`.


Using Windows installer
-----------------------

Currently, Windows installer is the only available binary installer. Just
double-click the installer and follow the instructions.

Selenium2Library can be uninstalled using the Programs and Features utility from
Control Panel (Add/Remove Programs on older versions of Windows).


.. _Selenium Python Bindings: http://code.google.com/p/selenium/wiki/PythonBindings
.. _PyPI: http://code.google.com/p/selenium/wiki/PythonBindings
.. _easy_install: http://pypi.python.org/pypi/setuptools