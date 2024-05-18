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
import json
from pathlib import Path
from typing import Optional
import click

from .get_versions import get_version
from .translation import compare_translatoin, get_library_translaton


CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
VERSION = get_version()


@click.group()
@click.version_option(VERSION)
def cli():
    """Robot Framework SeleniumLibrary command line tool.

    Possible commands are:
    translation


    translation will generate detaul tranlsation json file from library keywords.

    See each command argument help for more details what (optional) arguments that command supports.
    """
    pass


@cli.command()
@click.argument(
    "filename",
    type=click.Path(exists=False, dir_okay=False, path_type=Path),
    required=True,
)
@click.option(
    "--plugings",
    help="Same as plugins argument in the library import.",
    default=None,
    type=str,
)
@click.option(
    "--compare",
    help="Compares the translation file sha256 sum to library documentation.",
    default=False,
    is_flag=True,
    show_default=True,
)
def translation(
    filename: Path,
    plugings: Optional[str] = None,
    compare: bool = False,
):
    """Default translation file from library keywords.

    This will help users to create their own translation as Python plugins. Command
    will populate json file with english language. To create proper translation
    file, users needs to translate the keyword name and doc arguments values in
    json file.

    The filename argument will tell where the default json file is saved.

    The --pluging argument is same as plugins argument in the library import.
    If you use plugins, it is also get default translation json file also witht
    the plugin keyword included in the library.

    If the --compare flag is set, then command does not generate template
    translation file. Then it compares sha256 sums from the filenane
    to ones read from the library documenentation. It will print out a list
    of keywords which documentation sha256 does not match. This will ease
    translation projects to identify keywords which documentation needs updating.
    """
    translation = get_library_translaton(plugings)
    if compare:
        if table := compare_translatoin(filename, translation):
            print(
                "Found differences between translation and library, see below for details."
            )
            for line in table:
                print(line)
        else:
            print("Translation is valid, no updated needed.")
    else:
        with filename.open("w") as file:
            json.dump(translation, file, indent=4)
        print(f"Translation file created in {filename.absolute()}")


if __name__ == "__main__":
    cli()
