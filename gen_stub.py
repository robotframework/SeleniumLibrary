# Copyright 2020-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# Copied from: https://github.com/MarketSquare/robotframework-browser/blob/master/Browser/gen_stub.py
import sys
from pathlib import Path
from typing import Any

from robotlibcore import KeywordBuilder  # type: ignore

SRC_DIR = Path("./src").absolute()
sys.path.append(str(SRC_DIR))
import SeleniumLibrary  # noqa


def is_named_method(keyword_name: str) -> bool:
    keyword_attribute = SL.attributes[keyword_name]
    return (
        keyword_attribute.robot_name is not None
        and keyword_attribute.robot_name == keyword_name
    )


def get_method_name_for_keyword(keyword_name: str) -> str:
    if is_named_method(keyword_name):
        for key in SL.attributes.keys():
            if key != keyword_name and keyword_name == SL.attributes[key].robot_name:
                return key
    return keyword_name


def get_type_string_from_type(argument_type: type) -> str:
    if hasattr(argument_type, "__name__"):
        return argument_type.__name__
    else:
        arg_type_str = str(argument_type.__repr__()).lstrip("typing.")
        return arg_type_str.replace("NoneType", "None")


def get_type_sting_from_argument(argument_string: str, argument_types: dict) -> str:
    agrument_name = argument_string.lstrip("*")
    if agrument_name in argument_types:
        return get_type_string_from_type(argument_types[agrument_name])
    return ""


def get_function_list_from_keywords(keywords):
    functions = list()
    for keyword in keywords:
        method_name = get_method_name_for_keyword(keyword)
        keyword_arguments = SL.get_keyword_arguments(keyword)
        keyword_types = SL.get_keyword_types(keyword)
        functions.append(keyword_line(keyword_arguments, keyword_types, method_name))
    functions.sort()
    last_function = functions.pop()
    functions.append(last_function.rstrip())
    return functions


def keyword_line(keyword_arguments, keyword_types, method_name):
    arguments_list = list()
    for argument in keyword_arguments:
        if isinstance(argument, tuple):
            arg_str = argument[0]
            default_value = argument[1]
            arg_type_str = get_type_sting_from_argument(arg_str, keyword_types)
            if arg_type_str:
                if default_value is None:
                    arg_type_str = f"Optional[{arg_type_str}]"
                if arg_type_str == "str":
                    default_value = f"'{default_value}'"
                arg_str = arg_str + f": {arg_type_str}"
            elif isinstance(default_value, str):
                default_value = f"'{default_value}'"
            arg_str = arg_str + f" = {default_value}"
        else:
            arg_str = argument
            arg_type_str = get_type_sting_from_argument(arg_str, keyword_types)
            if arg_type_str:
                arg_str = arg_str + f": {arg_type_str}"
        arguments_list.append(arg_str)
    arguments_string = (
        f", {', '.join(arguments_list)}" if len(arguments_list) > 0 else ""
    )
    return f"    def {method_name}(self{arguments_string}): ...\n"


SL: Any = SeleniumLibrary.SeleniumLibrary()
FUNCTION_LIST = get_function_list_from_keywords(SL.get_keyword_names())


pyi_boilerplate = """
class SeleniumLibrary:
"""
pyi_boilerplate_append = """
    def add_library_components(self, library_components): ...
    def get_keyword_names(self): ...
    def run_keyword(self, name, args, kwargs=None): ...
    def get_keyword_arguments(self, name): ...
    def get_keyword_tags(self, name): ...
    def get_keyword_documentation(self, name): ...
    def get_keyword_types(self, name): ...
    def get_keyword_source(self, keyword_name): ...

"""

INIT_METHOD = KeywordBuilder.build(SL.__init__)
with open("src/SeleniumLibrary/__init__.pyi", "w") as stub_file:
    stub_file.write(pyi_boilerplate)
    stub_file.write(
        keyword_line(
            INIT_METHOD.argument_specification, INIT_METHOD.argument_types, "__init__"
        )
    )
    stub_file.writelines(FUNCTION_LIST)
    stub_file.write("\n    # methods from PythonLibCore")
    stub_file.writelines(pyi_boilerplate_append.splitlines(keepends=True))
