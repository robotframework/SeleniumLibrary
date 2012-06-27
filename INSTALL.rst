Selenium2Library Installation
=============================


Preconditions
-------------

Selenium2Library supports all Python and Jython interpreters supported by the
Robot Framework and the `Selenium Python Bindings`_. The Selenium Python Bindings
are the most restrictive, and as of now require Python 2.6 or Python 2.7.

Selenium2Library depends on a few other Python libraries, including
of course Robot Framework and Selenium. All dependencies are declared
in setup.py. If you use pip or easy_install to install this library, the
dependencies will be installed for you (this is recommended).


Installing from PyPI (recommended)
----------------------------------

Selenium2Library is available in the Python Package Index (PyPI_). To install,
you need to have `pip`_ installed. Then run::

	pip install robotframework-selenium2library

Or alternately, if you only have `easy_install`_,::

	easy_install robotframework-selenium2library


Installing from source
----------------------

The source code can be retrieved either as a source distribution or as a clone
of the main source repository. The installer requires Python version 2.4 or
newer. Install by running::

    python setup.py install

Or, if you'd like to automatically install dependencies, run::

    python setup.py develop

Note: In most linux systems, you need to have root privileges for installation.

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
.. _pip: http://www.pip-installer.org
.. _easy_install: http://pypi.python.org/pypi/setuptools