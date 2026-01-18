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

import hashlib
import inspect
import json
from pathlib import Path
from typing import List, Optional

KEYWORD_NAME = "Keyword name"
DOC_CHANGED = "Documentation update needed"
NO_LIB_KEYWORD = "Keyword not found from library"
MISSING_TRANSLATION = "Keyword is missing translation"
MISSING_CHECKSUM = "Keyword translation is missing checksum"
MAX_REASON_LEN = max(
    len(DOC_CHANGED),
    len(NO_LIB_KEYWORD),
    len(MISSING_TRANSLATION),
    len(MISSING_CHECKSUM),
)


def get_library_translation(plugins: Optional[str] = None) -> dict:
    from SeleniumLibrary import SeleniumLibrary

    selib = SeleniumLibrary(plugins=plugins)
    translation = {}
    for function in selib.attributes.values():
        translation[function.__name__] = {
            "name": function.__name__,
            "doc": function.__doc__,
            "sha256": hashlib.sha256(function.__doc__.encode("utf-16")).hexdigest(),
        }
    translation["__init__"] = {
        "name": "__init__",
        "doc": inspect.getdoc(selib),
        "sha256": hashlib.sha256(inspect.getdoc(selib).encode("utf-16")).hexdigest(),  # type: ignore
    }
    translation["__intro__"] = {
        "name": "__intro__",
        "doc": selib.__doc__,
        "sha256": hashlib.sha256(selib.__doc__.encode("utf-16")).hexdigest(),  # type: ignore
    }
    return translation


def _max_kw_name_length(project_translation: dict) -> int:
    max_lenght = 0
    for keyword_data in project_translation.values():
        if (current_kw_length := len(keyword_data["name"])) > max_lenght:
            max_lenght = current_kw_length
    return max_lenght


def _get_heading(max_kw_length: int) -> List[str]:
    heading = f"| {KEYWORD_NAME} "
    next_line = f"| {'-' * len(KEYWORD_NAME)}"
    if (padding := max_kw_length - len(KEYWORD_NAME)) > 0:
        heading = f"{heading}{' ' * padding}"
        next_line = f"{next_line}{'-' * padding}"
    reason = "Reason"
    reason_padding = MAX_REASON_LEN - len(reason)
    heading = f"{heading}| {reason}{' ' * reason_padding} |"
    next_line = f"{next_line} | {'-' * MAX_REASON_LEN} |"
    return [heading, next_line]


def _table_doc_updated(lib_kw: str, max_name_lenght: int, reason: str) -> str:
    line = f"| {lib_kw} "
    if (padding := max_name_lenght - len(lib_kw) - 0) > 0:
        line = f"{line}{' ' * padding}| {reason} "
    else:
        line = f"{line}| {reason} "
    if reason_padding := MAX_REASON_LEN - len(reason):
        line = f"{line}{' ' * reason_padding}"
    return f"{line}|"


def compare_translation(filename: Path, library_translation: dict):
    with filename.open("r") as file:
        project_translation = json.load(file)
    max_kw_length = _max_kw_name_length(library_translation)
    table_body = []
    for lib_kw, lib_kw_data in library_translation.items():
        project_kw_data = project_translation.get(lib_kw)
        if not project_kw_data:
            table_body.append(
                _table_doc_updated(lib_kw, max_kw_length, MISSING_TRANSLATION)
            )
            continue
        sha256_value = project_kw_data.get("sha256")
        if not sha256_value:
            table_body.append(
                _table_doc_updated(lib_kw, max_kw_length, MISSING_CHECKSUM)
            )
            continue
        if project_kw_data["sha256"] != lib_kw_data["sha256"]:
            table_body.append(_table_doc_updated(lib_kw, max_kw_length, DOC_CHANGED))
    for project_kw in project_translation:
        if project_kw not in library_translation:
            table_body.append(
                _table_doc_updated(project_kw, max_kw_length, NO_LIB_KEYWORD)
            )
    if not table_body:
        return []

    table = _get_heading(max_kw_length)
    table.extend(table_body)
    return table
