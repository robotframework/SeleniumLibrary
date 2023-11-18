import os
import unittest
from collections import namedtuple

from robot.errors import DataError
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.errors import PluginError


class ExtendingSeleniumLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sl = SeleniumLibrary()
        cls.root_dir = os.path.dirname(os.path.abspath(__file__))
        Plugin = namedtuple("Plugin", "plugin, args, kw_args")
        lib = Plugin(
            plugin=os.path.join(cls.root_dir, "my_lib.py"), args=[], kw_args={}
        )
        cls.plugin = lib

    def test_no_libraries(self):
        for item in [None, "None", ""]:
            sl = SeleniumLibrary(plugins=item)
            assert len(sl.get_keyword_names()) == 177

    def test_parse_library(self):
        plugin = "path.to.MyLibrary"
        plugins = self.sl._string_to_modules(plugin)
        assert len(plugins) == 1
        assert plugins[0].module == plugin
        assert plugins[0].args == []
        assert plugins[0].kw_args == {}

    def test_parse_libraries(self):
        plugin = "path.to.MyLibrary,path.to.OtherLibrary"
        plugins = self.sl._string_to_modules(plugin)
        assert len(plugins) == 2
        assert plugins[0].module == plugin.split(",")[0]
        assert plugins[0].args == []
        assert plugins[1].module == plugin.split(",")[1]
        assert plugins[1].args == []

    def test_comma_and_space(self):
        plugin = "path.to.MyLibrary , path.to.OtherLibrary"
        plugins = self.sl._string_to_modules(plugin)
        assert len(plugins) == 2
        assert plugins[0].module == "path.to.MyLibrary"
        assert plugins[0].args == []
        assert plugins[1].module == "path.to.OtherLibrary"
        assert plugins[1].args == []

    def test_comma_and_space_with_arg(self):
        plugin = "path.to.MyLibrary;foo;bar , path.to.OtherLibrary"
        plugins = self.sl._string_to_modules(plugin)
        assert len(plugins) == 2
        assert plugins[0].module == "path.to.MyLibrary"
        assert plugins[0].args == ["foo", "bar"]
        assert plugins[1].module == "path.to.OtherLibrary"
        assert plugins[1].args == []

    def test_parse_library_with_args(self):
        plugin = "path.to.MyLibrary"
        plugin_args = "arg1;arg2"
        parsed_plugins = self.sl._string_to_modules(f"{plugin};{plugin_args}")
        parsed_plugin = parsed_plugins[0]
        assert len(parsed_plugins) == 1
        assert parsed_plugin.module == plugin
        assert parsed_plugin.args == list(plugin_args.split(";"))
        assert parsed_plugin.kw_args == {}

    def test_parse_plugin_with_kw_args(self):
        plugin = "PluginWithKwArgs.py"
        plugin_args = "kw1=Text1;kw2=Text2"
        parsed_plugins = self.sl._string_to_modules(f"{plugin};{plugin_args}")
        parsed_plugin = parsed_plugins[0]
        assert len(parsed_plugins) == 1
        assert parsed_plugin.module == plugin
        assert parsed_plugin.args == []
        assert parsed_plugin.kw_args == {"kw1": "Text1", "kw2": "Text2"}

    def test_plugin_does_not_exist(self):
        not_here = os.path.join(self.root_dir, "not_here.py")
        with self.assertRaises(DataError):
            SeleniumLibrary(plugins=not_here)

        with self.assertRaises(DataError):
            SeleniumLibrary(plugins="SeleniumLibrary.NotHere")

    def test_plugin_wrong_import_with_path(self):
        my_lib = os.path.join(self.root_dir, "my_lib.py")
        wrong_name = os.path.join(self.root_dir, "my_lib_wrong_name.py")
        with self.assertRaises(DataError):
            SeleniumLibrary(plugins=f"{my_lib}, {wrong_name}")

    def test_sl_with_kw_args_plugin(self):
        kw_args_lib = os.path.join(
            self.root_dir,
            "..",
            "..",
            "..",
            "atest",
            "acceptance",
            "1-plugin",
            "PluginWithKwArgs.py;kw1=Text1;kw2=Text2",
        )
        SeleniumLibrary(plugins=kw_args_lib)

    def test_no_library_component_inherit(self):
        no_inherit = os.path.join(self.root_dir, "my_lib_not_inherit.py")
        with self.assertRaises(PluginError):
            SeleniumLibrary(plugins=no_inherit)

    def test_plugin_as_last_in_init(self):
        plugin_file = os.path.join(self.root_dir, "plugin_tester.py")
        event_firing_wd = os.path.join(self.root_dir, "MyListener.py")
        sl = SeleniumLibrary(
            plugins=plugin_file, event_firing_webdriver=event_firing_wd
        )
        assert sl.event_firing_webdriver == "should be last"

    def test_easier_event_firing_webdriver_from_plugin(self):
        plugin_file = os.path.join(
            self.root_dir, "plugin_with_event_firing_webdriver.py"
        )
        sl = SeleniumLibrary(plugins=plugin_file)
        assert sl._plugin_keywords == ["tidii"]
        assert sl.event_firing_webdriver == "event_firing_webdriver"
