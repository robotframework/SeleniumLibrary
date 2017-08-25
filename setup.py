#!/usr/bin/env python

import re
from os.path import abspath, dirname, join
from setuptools import setup


CURDIR = dirname(abspath(__file__))

with open(join(CURDIR, 'src', 'SeleniumLibrary', '__init__.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'\n", f.read()).group(1)

DESCRIPTION = """
SeleniumLibrary is a web testing library for Robot Framework
that utilizes the Selenium tool internally.
"""[1:-1]

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(name         = 'robotframework-seleniumlibrary',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Tatu Aalto',
      author_email = 'aalto.tatu@gmail.com',
      url          = 'https://github.com/robotframework/SeleniumLibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium webdriver web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Programming Language :: Python :: 2",
                        "Programming Language :: Python :: 3",
                        "Topic :: Software Development :: Testing",
                        "Framework :: Robot Framework"
                     ],
      install_requires = REQUIREMENTS,
      package_dir  = {'' : 'src'},
      packages     = ['SeleniumLibrary', 'SeleniumLibrary.keywords',
                      'SeleniumLibrary.locators', 'SeleniumLibrary.utils'],
      include_package_data = True,
      )
