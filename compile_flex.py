#!/usr/bin/env python

"""Usage: python compile_flex.py [file name]
e.g. python compile_flex.py test/resources/html/flex/LoginApp.mxml

Troubleshooting:
- Set FLEX_HOME environment variable.
- On Linux, convert the windows line breaks in file: mxmlc, to linux line breaks.
  e.g. fromdos $FLEX_HOME/bin/mxmlc
  Also on linux, remember to: chmod +x mxmlc
- Checkout Flex pilot sources to .. directory (git clone https://github.com/mde/flex-pilot.git).
"""
import getopt
import os
import subprocess
import sys


def compile_flex(file_names):
    for file_name in file_names:
        subprocess.call([os.path.join(os.environ['FLEX_HOME'], 'bin', 'mxmlc'),
                         '-source-path=../flex-pilot/src/',
                         '-source-path+=test/resources/html/flex/',
                         file_name])

def exit_with(msg):
    print msg
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv)  == 1:
        exit_with(__doc__)
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        exit_with(msg + "\nfor help use --help")
    for o, _ in opts:
        if o in ("-h", "--help"):
            exit_with(__doc__)
    if not 'FLEX_HOME' in os.environ:
        exit_with('Please set FLEX_HOME environment variable.')
    compile_flex(sys.argv[1:])
