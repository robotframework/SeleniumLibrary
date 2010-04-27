#!/usr/bin/env python

import os
from time import localtime
from zipfile import ZipFile


FILES = {'': ['rundemo.py', 'README.txt'],
         'login_tests': ['valid_login.txt', 'invalid_login.txt',
                         'resource.txt'],
         'demoapp': ['server.py', 'index.html', 'welcome.html', 'error.html',
                     'login.js', 'demo.css']}

name = 'robotframework-seleniumlibrary-demo'
root = os.path.dirname(__file__)
zippath = os.path.join(root, '%s-%s.zip' % (name,
                                            '%d%02d%02d' % localtime()[:3]))
if os.path.exists(zippath):
    os.remove(zippath)
zipfile = ZipFile(zippath, 'w')
for dirname in FILES:
    for filename in FILES[dirname]:
        path = os.path.join(root, dirname, filename)
        print 'Adding:  ', os.path.normpath(path)
        zipfile.write(path, os.path.join(name, path))
zipfile.close()
print 'Created: ', os.path.normpath(zippath)
