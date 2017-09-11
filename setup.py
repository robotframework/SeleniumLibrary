#!/usr/bin/env python

import re
from os.path import abspath, dirname, join
from setuptools import setup, find_packages


CURDIR = dirname(abspath(__file__))

CLASSIFIERS = '''
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Topic :: Software Development :: Testing
Framework :: Robot Framework
Framework :: Robot Framework :: Library
'''.strip().splitlines()
with open(join(CURDIR, 'src', 'SeleniumLibrary', '__init__.py')) as f:
    VERSION = re.search("\n__version__ = '(.*)'", f.read()).group(1)
with open(join(CURDIR, 'README.rst')) as f:
    DESCRIPTION = f.read()
with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name             = 'robotframework-seleniumlibrary',
    version          = VERSION,
    description      = 'Web testing library for Robot Framework',
    long_description = DESCRIPTION,
    author           = 'Tatu Aalto',
    author_email     = 'aalto.tatu@gmail.com',
    url              = 'https://github.com/robotframework/SeleniumLibrary',
    license          = 'Apache License 2.0',
    keywords         = 'robotframework testing testautomation selenium webdriver web',
    platforms        = 'any',
    classifiers      = CLASSIFIERS,
    install_requires = REQUIREMENTS,
    package_dir      = {'': 'src'},
    packages         = find_packages('src')
)
