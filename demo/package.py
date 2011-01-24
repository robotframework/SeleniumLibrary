#!/usr/bin/env python

import os
from time import localtime
from zipfile import ZipFile, ZIP_DEFLATED


FILES = {'': ['rundemo.py', 'README.txt'],
         'login_tests': ['valid_login.txt', 'invalid_login.txt',
                         'html_resource.txt', 'flex_resource.txt'],
         'demoapp': ['server.py'],
         'demoapp/html': ['index.html', 'welcome.html', 'error.html',
                          'demo.css'],
         'demoapp/flex': ['index.html', 'LoginApp.mxml', 'LoginApp.swf',
                          'FlexPilot.swf']}

name = 'robotframework-seleniumlibrary-demo'
root = os.path.dirname(__file__)
timestamp = '%d%02d%02d' % localtime()[:3]
zippath = os.path.join(root, '%s-%s.zip' % (name, timestamp))
if os.path.exists(zippath):
    os.remove(zippath)
zipfile = ZipFile(zippath, 'w', ZIP_DEFLATED)
for dirname in FILES:
    for filename in FILES[dirname]:
        path = os.path.join(root, dirname.replace('/', os.sep), filename)
        print 'Adding:  ', os.path.normpath(path)
        zipfile.write(path, os.path.join(name, path))
zipfile.close()
print 'Created: ', os.path.normpath(zippath)
