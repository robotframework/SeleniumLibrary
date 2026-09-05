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
from datetime import timedelta
from pathlib import Path
from typing import Any, Union, get_args, get_origin

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


def _format_type_name(tp: Any) -> str:
    """Return a short, pyi-compatible name for a plain (non-generic) type."""
    name = getattr(tp, "__name__", None)
    if name is not None:
        return name
    # Fallback for typing constructs that lack __name__ (e.g. typing.List[int]).
    origin = get_origin(tp)
    if origin is not None and getattr(origin, "__name__", None):
        return origin.__name__
    return repr(tp)


def _is_union_origin(origin: Any) -> bool:
    """True for typing.Union / typing.Optional / PEP 604 types.UnionType."""
    if origin is Union:
        return True
    # PEP 604 unions (X | Y) have origin types.UnionType (Py>=3.10).
    union_type = getattr(sys.modules.get("types"), "UnionType", None)
    return union_type is not None and origin is union_type


def get_type_string_from_type(argument_type: Any) -> str:
    """Render a Robot keyword argument type as a valid PEP 484 annotation.

    The previous implementation returned the bare string ``"Union"`` for any
    typing.Union / typing.Optional / PEP 604 union (because each of those
    exposes ``__name__ == "Union"``), which produced invalid annotations like
    ``locator: Union`` and ``Optional[Optional]`` in the generated ``.pyi``.
    """
    origin = get_origin(argument_type)
    if _is_union_origin(origin):
        args = [a for a in get_args(argument_type) if a is not type(None)]
        if not args:
            return "Any"
        if len(args) == 1:
            return get_type_string_from_type(args[0])
        return "Union[" + ", ".join(get_type_string_from_type(a) for a in args) + "]"
    if argument_type is type(None):
        return "None"
    return _format_type_name(argument_type)


def get_type_sting_from_argument(argument_string: str, argument_types: dict) -> str:
    agrument_name = argument_string.lstrip("*")
    if agrument_name in argument_types:
        return get_type_string_from_type(argument_types[agrument_name])
    return ""


def get_function_list_from_keywords(keywords):
    functions = list()
    for keyword in keywords:
        if keyword == "switch_window":
            print(keyword)
        method_name = get_method_name_for_keyword(keyword)
        keyword_arguments = SL.get_keyword_arguments(keyword)
        keyword_types = SL.get_keyword_types(keyword)
        functions.append(keyword_line(keyword_arguments, keyword_types, method_name))
    functions.sort()
    last_function = functions.pop()
    functions.append(last_function.rstrip())
    return functions


def _type_already_includes_none(type_str: str) -> bool:
    """True when a rendered annotation already accepts ``None``."""
    if type_str in ("None", "Any"):
        return True
    # PEP 604 form, e.g. "str | None" / "list[int] | None".
    if " | None" in type_str or type_str.endswith(" | None"):
        return True
    # typing.Union / typing.Optional form.
    if type_str.startswith("Optional["):
        return True
    if type_str.startswith("Union[") and "None" in type_str:
        return True
    return False


def keyword_line(keyword_arguments, keyword_types, method_name):
    arguments_list = list()
    for argument in keyword_arguments:
        if isinstance(argument, tuple):
            arg_str = argument[0]
            default_value = argument[1]
            arg_type_str = get_type_sting_from_argument(arg_str, keyword_types)
            if arg_type_str:
                is_optional = (
                    default_value is None
                    and not _type_already_includes_none(arg_type_str)
                )
                if is_optional:
                    arg_type_str = f"Optional[{arg_type_str}]"
                if arg_type_str == "str" or arg_type_str == "Union[list, str]":
                    default_value = f"'{default_value}'"
                arg_str = arg_str + f": {arg_type_str}"
            elif isinstance(default_value, str):
                default_value = f"'{default_value}'"
            elif isinstance(default_value, timedelta):
                default_value = f"timedelta(seconds={default_value.total_seconds()})"
            arg_str = f"{arg_str} = {default_value}"
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


pyi_boilerplate = """\
from datetime import timedelta
from typing import Any, Optional, Union

import selenium
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.utils.types import Secret

class SeleniumLibrary:
"""
pyi_boilerplate_append = """
    def add_library_components(self, library_components): ...
    def get_keyword_names(self): ...
    def run_keyword(self, name: str, args: tuple, kwargs: Optional[dict] = None): ...
    def get_keyword_arguments(self, name: str): ...
    def get_keyword_tags(self, name: str): ...
    def get_keyword_documentation(self, name: str): ...
    def get_keyword_types(self, name: str): ...
    def get_keyword_source(self, keyword_name: str): ...
    def failure_occurred(self): ...
    def register_driver(self, driver: WebDriver, alias: str): ...
    @property
    def driver(self) -> WebDriver: ...
    def find_element(self, locator: str, parent: Optional[WebElement] = None): ...
    def find_elements(self, locator: str, parent: Optional[WebElement] = None): ...
    def _parse_plugins(self, plugins: Any): ...
    def _parse_plugin_doc(self): ...
    def _get_intro_documentation(self): ...
    def _parse_listener(self, event_firing_webdriver: Any): ...
    def _string_to_modules(self, modules: Any): ...
    def _store_plugin_keywords(self, plugin): ...
    def _resolve_screenshot_root_directory(self): ...
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
    stub_file.write("\n    # methods from library.")
    stub_file.writelines(pyi_boilerplate_append.splitlines(keepends=True))
