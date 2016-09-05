#!/usr/bin/env python

import os, sys, shutil, subprocess, argparse

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(THIS_DIR, "dist")
sys.path.append(os.path.join(THIS_DIR, "src", "Selenium2Library"))
sys.path.append(os.path.join(THIS_DIR, "doc"))
sys.path.append(os.path.join(THIS_DIR, "demo"))

def main():
    parser = argparse.ArgumentParser(description="Builds a Se2Lib distribution")
    parser.add_argument('py_26_path', action='store', help='Python 2.6 executbale file path')
    parser.add_argument('py_27_path', action='store', help='Python 2.7 executbale file path')
    parser.add_argument('--release', action='store_true')
    parser.add_argument('--winonly', action='store_true')
    args = parser.parse_args()
    
    if args.winonly:
        run_builds(args)
        return
    
    clear_dist_folder()
    run_register(args)
    run_builds(args)
    run_demo_packaging()
    run_doc_gen()

def clear_dist_folder():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.mkdir(DIST_DIR)

def run_doc_gen():
    import generate
    print
    generate.main()

def run_register(args):
    if args.release:
        _run_setup(args.py_27_path, "register", [], False)

def run_builds(args):
    print
    if not args.winonly:
        _run_setup(args.py_27_path, "sdist", [ "--formats=gztar,zip" ], args.release)
        _run_setup(args.py_26_path, "bdist_egg", [], args.release)
        _run_setup(args.py_27_path, "bdist_egg", [], args.release)
    if os.name == 'nt':
        _run_setup(args.py_27_path, "bdist_wininst", [ "--plat-name=win32" ], args.release)
        _run_setup(args.py_27_path, "bdist_wininst", [ "--plat-name=win-amd64" ], args.release)
    else:
        print    
        print("Windows binary installers cannot be built on this platform!")    

def run_demo_packaging():
    import package
    print
    package.main()

def _run_setup(py_path, type, params, upload):
    setup_args = [py_path, os.path.join(THIS_DIR, "setup.py")]
    #setup_args.append("--quiet")
    setup_args.append(type)
    setup_args.extend(params)
    if upload:
        setup_args.append("upload")
        
    print
    print("Running: %s" % ' '.join(setup_args))
    returncode = subprocess.call(setup_args)
    if returncode != 0:
        print("Error running setup.py")
        sys.exit(1)

if __name__ == '__main__':
    main()
