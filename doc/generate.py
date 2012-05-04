#!/usr/bin/env python
from os.path import join, dirname
try:
    from robot.libdoc import libdoc
except:
    print """Robot Framework 2.7 or later required for generating documentation"""
else:
    libdoc(join(dirname(__file__),'..','src','Selenium2Library'), join(dirname(__file__),'Selenium2Library.html'))
