# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
import re
import subprocess
import sys

from selenium import __version__

INSTALL_DIR = Path(__file__).parent.parent


def get_rf_version() -> str:
    process = subprocess.run(
        [sys.executable, "-m", "robot", "--version"], capture_output=True, check=False
    )
    return process.stdout.decode("utf-8").split(" ")[2]


def get_library_version() -> str:
    init_file = INSTALL_DIR / "__init__.py"
    with init_file.open("r") as file:
        data = file.read()
    return re.search('\n__version__ = "(.*)"', data).group(1)


def get_version():
    """Display Python, Robot Framework, SeleniumLibrary and selenium versions"""
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    return (
        f"\nUsed Python is: {sys.executable}\n\tVersion: {python_version}\n"
        f'Robot Framework version: "{get_rf_version()}"\n'
        f"Installed SeleniumLibrary version is: {get_library_version()}\n"
        f"Installed selenium version is: {__version__}\n"
    )
