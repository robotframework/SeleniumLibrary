import os
import unittest

from SeleniumLibrary import SeleniumLibrary
from .my_lib import my_lib
from .my_lib_args import my_lib_args


class PluginKeywordTags(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cls.plugin = os.path.join(root_dir, "my_lib.py")
        cls.plugin_varargs = os.path.join(root_dir, "my_lib_args.py")

    def test_no_plugin(self):
        sl = SeleniumLibrary()
        tags = sl.get_keyword_tags("open_browser")
        self.assertFalse(tags)

    def test_store_plugin_keywords(self):
        sl = SeleniumLibrary()
        sl._store_plugin_keywords(my_lib("0"))
        self.assertEqual(sl._plugin_keywords, ["bar", "foo"])

    def test_store_plugin_keywords_with_args(self):
        sl = SeleniumLibrary()
        sl._store_plugin_keywords(my_lib_args("000", "111", "222"))
        self.assertEqual(sl._plugin_keywords, ["add_cookie", "bar_2", "foo_1"])

    def test_tags_in_plugin(self):
        sl = SeleniumLibrary(plugins=self.plugin)
        tags = sl.get_keyword_tags("foo")
        self.assertEqual(tags, ["plugin"])

        tags = sl.get_keyword_tags("open_browser")
        self.assertFalse(tags)

    def test_tags_in_plugin_args(self):
        sl = SeleniumLibrary(plugins=f"{self.plugin_varargs};foo;bar")
        tags = sl.get_keyword_tags("foo_1")
        self.assertEqual(tags, ["MyTag", "plugin"])

        tags = sl.get_keyword_tags("open_browser")
        self.assertFalse(tags)

        tags = sl.get_keyword_tags("add_cookie")
        self.assertEqual(tags, ["plugin"])
