import os
from fnmatch import fnmatch
from browsercache import BrowserCache

__all__ = [
    "get_child_packages_in",
    "get_module_names_under",
    "import_modules_under",
    "escape_xpath_value",
    "BrowserCache"
]

# Public

def get_child_packages_in(root_dir, include_root_package_name=True, exclusions=None):
    packages = []
    root_package_str = os.path.basename(root_dir) + '.' if include_root_package_name else ""
    _discover_child_package_dirs(
        root_dir,
        _clean_exclusions(exclusions),
        lambda abs_path, relative_path, name: 
            packages.append(root_package_str + relative_path.replace(os.sep, '.')))
    return packages

def get_module_names_under(root_dir, include_root_package_name=True, exclusions=None, pattern=None):
    module_names = []
    root_package_str = os.path.basename(root_dir) + '.' if include_root_package_name else ""
    _discover_module_files_in(
        root_dir,
        _clean_exclusions(exclusions),
        pattern if pattern is not None else "*.*",
        lambda abs_path, relative_path, name: 
            module_names.append(root_package_str + os.path.splitext(relative_path)[0].replace(os.sep, '.')))
    return module_names

def import_modules_under(root_dir, include_root_package_name=True, exclusions=None, pattern=None):
    module_names = get_module_names_under(root_dir, include_root_package_name, exclusions, pattern)
    modules = [ __import__(module_name, globals(), locals(), ['*'], -1)
        for module_name in module_names ]
    return (module_names, modules)

def escape_xpath_value(value):
    value = unicode(value)
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value

# Private

def _clean_exclusions(exclusions):
    if exclusions is None: exclusions = []
    if not isinstance(exclusions, list): exclusions = [ exclusions ]
    exclusions = [ os.sep + exclusion.lower().strip(os.sep) + os.sep
        for exclusion in exclusions ]
    return exclusions

def _discover_child_package_dirs(root_dir, exclusions, callback, relative_dir=None):
    relative_dir = relative_dir if relative_dir is not None else ''
    abs_dir = os.path.join(root_dir, relative_dir)
    for item in os.listdir(abs_dir):
        item_relative_path = os.path.join(relative_dir, item)
        item_abs_path = os.path.join(root_dir, item_relative_path)
        if os.path.isdir(item_abs_path):
            if os.path.exists(os.path.join(item_abs_path, "__init__.py")):
                exclusion_matches = [ exclusion for exclusion in exclusions 
                    if os.sep + item_relative_path.lower() + os.sep == exclusion ]
                if not exclusion_matches:
                    callback(item_abs_path, item_relative_path, item)
                    _discover_child_package_dirs(root_dir, exclusions, callback, item_relative_path)

def _discover_module_files_in(root_dir, exclusions, pattern, callback):
    def find_matching_files(relative_dir):
        abs_dir = os.path.join(root_dir, relative_dir)
        for item in os.listdir(abs_dir):
            item_relative_path = os.path.join(relative_dir, item)
            item_abs_path = os.path.join(root_dir, item_relative_path)
            if os.path.isfile(item_abs_path) and fnmatch(item, pattern):
                callback(item_abs_path, item_relative_path, item)

    find_matching_files('')

    _discover_child_package_dirs(
        root_dir,
        _clean_exclusions(exclusions),
        lambda abs_path, relative_path, name: find_matching_files(relative_path))
