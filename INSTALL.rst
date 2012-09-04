Selenium2Library Installation
=============================


Preconditions
-------------

Selenium2Library supports all Python and Jython interpreters supported by the
Robot Framework and the `Selenium Python Bindings`_. The Selenium Python Bindings
are the most restrictive, and as of now require Python 2.6 or Python 2.7.

Selenium2Library depends on a few other Python libraries, including
of course Robot Framework and Selenium. All dependencies are declared
in setup.py.

Installing on Windows
---------------------
or (because easy_install under Windows doesn't install dependencies)
Installing using pip (recommended)
--------------------
but not (because pip does not necessarily install from pypi)
Installing from PyPI (recommended)
----------------------------------

Selenium2Library is available in the Python Package Index (PyPI_). To install,
you need to have `pip`_ installed. Then run::

	pip install robotframework-selenium2library

Or alternately, if you only have `easy_install`_,::

	easy_install robotframework-selenium2library

Installing on Linux
-------------------
Installing on Mac OSX
---------------------
if we use `Installing on Windows`_ then we need sections for other OSes

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

Verifying Installation
----------------------

Once you have installed Selenium2Library it is a good idea to verify the installation. To verify installation start python::

     C:\> python

and then at the Python prompt type::

	>> import Selenium2Library
	>>

If the python command line interpretor returns with another prompt ('>>' as shown above) then your installation was successful.

Troubleshooting Installation
----------------------------

The most common issue with installing Selenium2Library is missing dependencies. An error like::

    ImportError: No module named robot.variables

indicates that you are missing the Robot Framework package.  To correct this problem try typing at the prompt::

	  easy_install robotframework

Similarly if you receive "No module named ..." error message then you have another missing dependency.  To correct, use easy_install to install the missing package.

Different Flavors of Python
---------------------------
CPython, PyPy, Iron Python, ActivePython, 32 bit, 64 bit. Not all flavors of Python are the same. Explain the differences and some expected roadblocks with various versions.

Python Packaging Tools
----------------------
The in's and out's of easy_setup, pip, etc. Explain how to upgrade a package using pip.



.. _Selenium Python Bindings: http://code.google.com/p/selenium/wiki/PythonBindings
.. _PyPI: http://code.google.com/p/selenium/wiki/PythonBindings
.. _pip: http://www.pip-installer.org
.. _easy_install: http://pypi.python.org/pypi/setuptools