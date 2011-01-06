#!/usr/bin/env python

from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'src', 'SeleniumLibrary', 'version.py'))

setup(name         = 'robotframework-seleniumlibrary',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      author       = 'Robot Framework Developers',
      author_email = 'robotframework-users@googlegroups.com',
      url          = 'http://code.google.com/p/robotframework-seleniumlibrary',
      package_dir  = {'' : 'src'},
      packages     = ['SeleniumLibrary'],
      package_data = {'SeleniumLibrary': ['lib/*.jar', 'firefoxprofile/*.*']},
      )
