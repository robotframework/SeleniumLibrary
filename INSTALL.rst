Selenium2Library Installation
=============================

Preconditions
-------------

Selenium2Library supports all Python and Jython interpreters supported by the
Robot Framework and the `Selenium Python Bindings`_. The Robot Framework Python
Bindings are the most restrictive and as of now require Python 2.7 or
Python 3.3+

Selenium2Library depends on Robot Framework and Selenium. All dependencies are
declared in requirements.txt with their minimum required versions.

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

Once installation is completed, you should verify proper installation of
Selenium2Library and it's dependencies. See `Verifying Installation` section
below.

Proxy configuration
-------------------

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


Installing from source
----------------------

The source code can be retrieved either as a source distribution or as a clone
of the main source repository. The installer requires Python version 2.7 or
Python 3.3+. Install by running::

    python setup.py install

Or, if you'd like to automatically install dependencies, run::

    python setup.py develop

Note: In most linux systems, you need to have root privileges for installation.

Uninstallation is achieved by deleting the installation directory and its
contents from the file system. The default installation directory is
`[PythonLibraries]/site-packages/Selenium2Library`.

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

      pip_install robotframework

Similarly if you receive "No module named ..." error message then you have another missing dependency.  To correct, use pip to install the missing package.


.. _Selenium Python Bindings: https://github.com/SeleniumHQ/selenium/wiki/Python-Bindings
.. _PyPI: https://pypi.python.org/pypi
.. _pip: http://www.pip-installer.org
.. _easy_install: http://pypi.python.org/pypi/setuptools