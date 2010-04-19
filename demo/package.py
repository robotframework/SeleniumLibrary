#!/usr/bin/env python

import os
import time
import shutil
from zipfile import ZipFile


def package():
    demodir = os.path.normpath(os.path.dirname(__file__))
    zipname = 'robotframework-seleniumlibrary-demo-%d%d%d.zip' % time.localtime()[:3]
    zippath = os.path.join(demodir, zipname)
    if os.path.exists(zippath):
        os.remove(zippath)
    demozip = ZipFile(zippath, 'w')
    add_files(demodir, demozip)
    demozip.close()
    return zipname

def add_files(dirname, zipfile):
    for path in os.listdir(dirname):
        path = os.path.normpath(os.path.join(dirname, path))
        if path == 'results' or path == os.path.normpath(__file__)\
            or os.path.splitext(path)[1] == '.zip': 
            continue
        if os.path.isfile(path):
            print 'Adding', path
            zipfile.write(path, os.path.join('robotframework-seleniumlibrary-demo', path))
        elif '.svn' not in path:
            add_files(path, zipfile)


if __name__ == '__main__':
    print package()
