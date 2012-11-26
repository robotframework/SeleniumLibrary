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


Installing using pip (recommended) or easy_install
--------------------------------------------------

Selenium2Library is available in the Python Package Index (PyPI_). It is
recommended that you use `pip`_ to install. Using pip will ensure that
both Selenium2Library **and** it's dependiences are installed.
To install using pip, run::

	pip install robotframework-selenium2library

Or alternately, if you only have `easy_install`_,::

	easy_install robotframework-selenium2library

If you install Selenium2Library under Windows **and** you use easy_install, 
you will need to install Selenium2Library's dependencies seperately.
To install the dependencies, run::

	easy_install robotframework
        easy_install selenium
        easy_install decorator
        easy_install docutils

Once installation is completed, you should verify proper installation of
Selenium2Library and it's dependencies. See `Verifying Installation` section
below.

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
double-click the installer and follow the instructions. The installer is missing 
decorator module. It must be installed either via pip or easy install, or from
http://pypi.python.org/pypi/decorator/

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


.. _Selenium Python Bindings: http://code.google.com/p/selenium/wiki/PythonBindings
.. _PyPI: http://code.google.com/p/selenium/wiki/PythonBindings
.. _pip: http://www.pip-installer.org
.. _easy_install: http://pypi.python.org/pypi/setuptools