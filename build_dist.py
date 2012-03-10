#!/usr/bin/env python

import os, sys, shutil
import subprocess

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(THIS_DIR, "dist")
sys.path.append(os.path.join(THIS_DIR, "src", "Selenium2Library"))
sys.path.append(os.path.join(THIS_DIR, "doc"))
sys.path.append(os.path.join(THIS_DIR, "demo"))

def main():
    clear_dist_folder()
    run_doc_gen()
    run_sdist()
    run_win_bdist()
    run_demo_packaging()

def clear_dist_folder():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.mkdir(DIST_DIR)

def run_doc_gen():
    import generate
    generate.main()

def run_sdist():
    subprocess.call(["python", os.path.join(THIS_DIR, "setup.py"), "sdist", "--formats=gztar,zip"])

def run_win_bdist():
    if os.name == 'nt':
        subprocess.call(["python", os.path.join(THIS_DIR, "setup.py"), "bdist", "--formats=wininst", "--plat-name=win32"])
        subprocess.call(["python", os.path.join(THIS_DIR, "setup.py"), "bdist", "--formats=wininst", "--plat-name=win-amd64"])

def run_demo_packaging():
    import package
    package.main()


if __name__ == '__main__':
    main()
