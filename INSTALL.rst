Selenium2Library Installation
=============================


This document is currently out of date. If you need to install the latest
stable version, then run::

    pip install robotframework-selenium2library

If you need the alpha release, which supports Python 2 and 3, then run::

    pip install -U --pre robotframework-seleniumlibrary

The documentation will be fixed when the robotframework-seleniumlibrary
is released.

Preconditions
-------------

Selenium2Library supports almost all Python interpreters supported by the
Robot Framework and the `Selenium Python Bindings`_. The Selenium2Library
requires Python 2.7 or Python 3.3+. String from release 3.0.0, the Python
2.6 is not anymore supported.

Selenium2Library depends on Robot Framework and Selenium. All dependencies are
declared in `requirements.txt`_ with their minimum required versions. With the
Selenium it might be possible that the Selenium2Library supports older versions,
but older Selenium version are not tested by the development team.

Selenium needs a browser specific driver to downloaded and placed in the
operating system PATH variable. For more details about supported drivers and
their downloads can be found from the selenium documentation:
https://seleniumhq.github.io/selenium/docs/api/py/index.html#drivers

Installing using pip
--------------------

Selenium2Library is available in the Python Package Index (PyPI_). It is
recommended that you use `pip`_ to install. Using pip will ensure that
both Selenium2Library **and** it's dependiences are installed.
To install using pip, run::

    pip install robotframework-selenium2library

The main benefit of using `pip` is that it automatically installs all
dependencies needed by the library. Other nice features are easy upgrading
and support for un-installation::

    pip install --upgrade robotframework-selenium2library
    pip uninstall robotframework-selenium2library

Notice that using ``--upgrade`` above updates both the library and all
its dependencies to the latest version. If you want, you can also install
a specific version or upgrade only the Selenium tool used by the library::

    pip install robotframework-selenium2library==1.8.0
    pip install --upgrade selenium
    pip install selenium==3.4.2

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

- https://pip.pypa.io/en/stable/
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

With resent versions of `pip` it is possible to perform the installation
directly from the Selenium2Library GitHub repository. For more details about
the `pip` vcs support, please refer to the pip documentation:
https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support

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

      pip install robotframework

Similarly if you receive "No module named ..." error message then you have another missing dependency.  To correct, use pip to install the missing package.


.. _Selenium Python Bindings: https://github.com/SeleniumHQ/selenium/wiki/Python-Bindings
.. _PyPI: https://pypi.python.org/pypi
.. _pip: http://www.pip-installer.org
.. _easy_install: http://pypi.python.org/pypi/setuptools
.. _requirements.txt: https://github.com/robotframework/Selenium2Library/blob/master/requirements.txt
