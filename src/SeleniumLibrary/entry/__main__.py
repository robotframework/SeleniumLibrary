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
import click

from print_version import print_version

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


@click.group(
    invoke_without_command=True, context_settings=CONTEXT_SETTINGS, no_args_is_help=True
)
@click.option(
    "--version",
    is_flag=True,
    help="Prints versions and exits",
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
def cli():
    """Robot Framework SeleniumLibrary command line tool.

    Possible commands are:
    translation


    translation will generate detaul tranlsation json file from library keywords.

    See each command argument help for more details what (optional) arguments that command supports.
    """
    pass


if __name__ == "__main__":
    cli()
