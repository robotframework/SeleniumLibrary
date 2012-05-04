#!/usr/bin/env python

import os, sys
from time import localtime
from zipfile import ZipFile, ZIP_DEFLATED

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, '..', 'src', 'Selenium2Library', 'version.py'))

FILES = {
    '': ['rundemo.py'],
    'login_tests': ['valid_login.txt', 'invalid_login.txt', 'resource.txt'],
    'demoapp': ['server.py'],
    'demoapp/html': ['index.html', 'welcome.html', 'error.html', 'demo.css']
}

def main():
    cwd = os.getcwd()
    try:
        os.chdir(THIS_DIR)
        name = 'robotframework-selenium2library-%s-demo' % VERSION
        zipname = '%s.zip' % name
        if os.path.exists(zipname):
            os.remove(zipname)
        zipfile = ZipFile(zipname, 'w', ZIP_DEFLATED)
        for dirname in FILES:
            for filename in FILES[dirname]:
                path = os.path.join('.', dirname.replace('/', os.sep), filename)
                print 'Adding:  ', os.path.normpath(path)
                zipfile.write(path, os.path.join(name, path))
        zipfile.close()
        target_path = os.path.join('..', 'dist', zipname)
        if os.path.exists(target_path):
            os.remove(target_path)
        os.rename(zipname, target_path)
        print 'Created: ', os.path.abspath(target_path)
    finally:
        os.chdir(cwd)


if __name__ == '__main__':
    main()
