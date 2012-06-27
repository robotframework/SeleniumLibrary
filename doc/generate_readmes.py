#!/usr/bin/env python

import os, shutil
from buildhtml import Builder

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")
LIB_DIR = os.path.join(SRC_DIR, "Selenium2Library")

README_FILES = [
    "README.rst",
    "INSTALL.rst",
    "BUILD.rst",
    "CHANGES.rst"
]

def main():
    try:
        import docutils
    except:
        print "Readme files will not be built into HTML, docutils not installed"
        return
    for readme_relative_path in README_FILES:
        (readme_dir, readme_name) = _parse_readme_path(readme_relative_path)
        readme_txt_name = _make_txt_file(readme_dir, readme_name)
        Builder().process_txt(readme_dir, readme_txt_name)
        _cleanup_txt_file(readme_dir, readme_txt_name)

        readme_html_name = os.path.splitext(readme_name)[0] + '.html'
        readme_html_path = os.path.join(readme_dir, readme_html_name)
        target_readme_html_name =  os.path.splitext(readme_relative_path.replace('/', '-'))[0] + '.html'
        target_readme_html_path = os.path.join(THIS_DIR, target_readme_html_name)

        if os.path.exists(target_readme_html_path):
            os.remove(target_readme_html_path)
        os.rename(readme_html_path, target_readme_html_path)

        print "    ::: Saved: %s" % target_readme_html_name

def _parse_readme_path(readme_relative_path):
    readme_abs_path = os.path.join(ROOT_DIR, readme_relative_path.replace('/', os.sep))
    readme_path_parts = os.path.split(readme_abs_path)
    readme_dir = readme_path_parts[0]
    readme_name = readme_path_parts[1]
    return (readme_dir, readme_name)

def _make_txt_file(readme_dir, readme_name):
    readme_txt_name  = os.path.splitext(readme_name)[0] + '.txt'
    _cleanup_txt_file(readme_dir, readme_txt_name)
    shutil.copyfile(
        os.path.join(readme_dir, readme_name), 
        os.path.join(readme_dir, readme_txt_name))
    return readme_txt_name

def _cleanup_txt_file(readme_dir, readme_txt_name):
    readme_txt_abs_path = os.path.join(readme_dir, readme_txt_name)
    if os.path.exists(readme_txt_abs_path):
        os.remove(readme_txt_abs_path)


if __name__ == '__main__':
    main()
