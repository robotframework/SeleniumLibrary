#!/usr/bin/env python

from os.path import abspath, dirname, join

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

curdir = dirname(abspath(__file__))
execfile(join(curdir, 'src', 'Selenium2Library', 'version.py'))
with open(join(curdir, 'README.rst')) as f:
    DESCRIPTION = f.read()

setup(
    name             = 'robotframework-selenium2library',
    version          = VERSION,
    description      = 'Web testing library for Robot Framework',
    long_description = DESCRIPTION,
    author           = 'Ryan Tomac , Ed Manlove , Jeremy Johnson',
    author_email     = '<ryan@tomacfamily.com> ,  <devPyPlTw@verizon.net> ,  <jeremy@softworks.com.my>',
    url              = 'https://github.com/rtomac/robotframework-selenium2library',
    license          = 'Apache License 2.0',
    keywords         = 'robotframework testing testautomation selenium selenium2 webdriver web',
    platforms        = 'any',
    classifiers      = ['Development Status :: 5 - Production/Stable',
                        'License :: OSI Approved :: Apache Software License',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python',
                        'Topic :: Software Development :: Testing'],
    install_requires = ['decorator >= 3.3.2',
                        'selenium >= 2.32.0',
                        'robotframework >= 2.6.0',
                        'docutils >= 0.8.1'],
    py_modules       = ['ez_setup'],
    package_dir      = {'' : 'src'},
    packages         = ['Selenium2Library',
                        'Selenium2Library.keywords',
                        'Selenium2Library.locators',
                        'Selenium2Library.utils'],
    include_package_data = True,
)
