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


def _format_path(file_path, index):
    return _format_path_with_index(file_path, index)[0]


def _format_path_with_index(file_path, index):
    formatter = _SafeFormatter(index=index)
    formatted = file_path.format_map(formatter)
    return formatted, formatter.index_used


class _SafeFormatter(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index_used = False

    def __getitem__(self, key):
        if key == "index":
            self.index_used = True
        return super().__getitem__(key)

    def __missing__(self, key):
        return f"{{{key}}}"
