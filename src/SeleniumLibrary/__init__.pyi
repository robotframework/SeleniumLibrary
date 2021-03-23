from datetime import timedelta
from typing import Any, Optional, Union

import selenium
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class SeleniumLibrary:
    def __init__(
        self,
        timeout=timedelta(seconds=5.0),
        implicit_wait=timedelta(seconds=0.0),
        run_on_failure="Capture Page Screenshot",
        screenshot_root_directory: Optional[str] = None,
        plugins: Optional[str] = None,
        event_firing_webdriver: Optional[str] = None,
    ): ...
    def add_cookie(
        self,
        name: str,
        value: str,
        path: Optional[str] = None,
        domain: Optional[str] = None,
        secure: Optional[bool] = None,
        expiry: Optional[str] = None,
    ): ...
    def add_location_strategy(
        self, strategy_name: str, strategy_keyword: str, persist: bool = False
    ): ...
    def alert_should_be_present(
        self,
        text: str = "",
        action: str = "ACCEPT",
        timeout: Optional[timedelta] = None,
    ): ...
    def alert_should_not_be_present(
        self, action: str = "ACCEPT", timeout: Optional[timedelta] = None
    ): ...
    def assign_id_to_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        id: str,
    ): ...
    def capture_element_screenshot(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        filename: str = "selenium-element-screenshot-{index}.png",
    ): ...
    def capture_page_screenshot(
        self, filename: str = "selenium-screenshot-{index}.png"
    ): ...
    def checkbox_should_be_selected(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def checkbox_should_not_be_selected(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def choose_file(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        file_path: str,
    ): ...
    def clear_element_text(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def click_button(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        modifier: Union[bool, str] = False,
    ): ...
    def click_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        modifier: Union[bool, str] = False,
        action_chain: bool = False,
    ): ...
    def click_element_at_coordinates(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        xoffset: int,
        yoffset: int,
    ): ...
    def click_image(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        modifier: Union[bool, str] = False,
    ): ...
    def click_link(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        modifier: Union[bool, str] = False,
    ): ...
    def close_all_browsers(self): ...
    def close_browser(self): ...
    def close_window(self): ...
    def cover_element(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def create_webdriver(
        self, driver_name: str, alias: Optional[str] = None, kwargs={}, **init_kwargs
    ): ...
    def current_frame_should_contain(self, text: str, loglevel: str = "TRACE"): ...
    def current_frame_should_not_contain(self, text: str, loglevel: str = "TRACE"): ...
    def delete_all_cookies(self): ...
    def delete_cookie(self, name): ...
    def double_click_element(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def drag_and_drop(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        target: Union[selenium.webdriver.remote.webelement.WebElement, str],
    ): ...
    def drag_and_drop_by_offset(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        xoffset: int,
        yoffset: int,
    ): ...
    def element_attribute_value_should_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        attribute: str,
        expected: Union[None, str],
        message: Optional[str] = None,
    ): ...
    def element_should_be_disabled(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def element_should_be_enabled(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def element_should_be_focused(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def element_should_be_visible(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
    ): ...
    def element_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: Union[None, str],
        message: Optional[str] = None,
        ignore_case: bool = False,
    ): ...
    def element_should_not_be_visible(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
    ): ...
    def element_should_not_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: Union[None, str],
        message: Optional[str] = None,
        ignore_case: bool = False,
    ): ...
    def element_text_should_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: Union[None, str],
        message: Optional[str] = None,
        ignore_case: bool = False,
    ): ...
    def element_text_should_not_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        not_expected: Union[None, str],
        message: Optional[str] = None,
        ignore_case: bool = False,
    ): ...
    def execute_async_javascript(
        self, *code: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def execute_javascript(
        self, *code: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def frame_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        text: str,
        loglevel: str = "TRACE",
    ): ...
    def get_all_links(self): ...
    def get_browser_aliases(self): ...
    def get_browser_ids(self): ...
    def get_cookie(self, name: str): ...
    def get_cookies(self, as_dict: bool = False): ...
    def get_element_attribute(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        attribute: str,
    ): ...
    def get_element_count(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_element_size(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_horizontal_position(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_list_items(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        values: bool = False,
    ): ...
    def get_location(self): ...
    def get_locations(self, browser: str = "CURRENT"): ...
    def get_selected_list_label(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_selected_list_labels(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_selected_list_value(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_selected_list_values(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_selenium_implicit_wait(self): ...
    def get_selenium_speed(self): ...
    def get_selenium_timeout(self): ...
    def get_session_id(self): ...
    def get_source(self): ...
    def get_table_cell(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        row: int,
        column: int,
        loglevel: str = "TRACE",
    ): ...
    def get_text(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_title(self): ...
    def get_value(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_vertical_position(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_webelement(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_webelements(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def get_window_handles(self, browser: str = "CURRENT"): ...
    def get_window_identifiers(self, browser: str = "CURRENT"): ...
    def get_window_names(self, browser: str = "CURRENT"): ...
    def get_window_position(self): ...
    def get_window_size(self, inner: bool = False): ...
    def get_window_titles(self, browser: str = "CURRENT"): ...
    def go_back(self): ...
    def go_to(self, url): ...
    def handle_alert(
        self, action: str = "ACCEPT", timeout: Optional[timedelta] = None
    ): ...
    def input_password(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        password: str,
        clear: bool = True,
    ): ...
    def input_text(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        text: str,
        clear: bool = True,
    ): ...
    def input_text_into_alert(
        self, text: str, action: str = "ACCEPT", timeout: Optional[timedelta] = None
    ): ...
    def list_selection_should_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *expected: str,
    ): ...
    def list_should_have_no_selections(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def location_should_be(self, url: str, message: Optional[str] = None): ...
    def location_should_contain(self, expected: str, message: Optional[str] = None): ...
    def log_location(self): ...
    def log_source(self, loglevel: str = "INFO"): ...
    def log_title(self): ...
    def maximize_browser_window(self): ...
    def mouse_down(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def mouse_down_on_image(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def mouse_down_on_link(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def mouse_out(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def mouse_over(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def mouse_up(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: str = "firefox",
        alias: Optional[str] = None,
        remote_url: Union[bool, str] = False,
        desired_capabilities: Optional[Union[dict, None, str]] = None,
        ff_profile_dir: Optional[
            Union[selenium.webdriver.firefox.firefox_profile.FirefoxProfile, str, None]
        ] = None,
        options: Optional[Any] = None,
        service_log_path: Optional[str] = None,
        executable_path: Optional[str] = None,
    ): ...
    def open_context_menu(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def page_should_contain(self, text: str, loglevel: str = "TRACE"): ...
    def page_should_contain_button(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_checkbox(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
        limit: Optional[int] = None,
    ): ...
    def page_should_contain_image(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_link(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_list(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_radio_button(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_contain_textfield(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain(self, text: str, loglevel: str = "TRACE"): ...
    def page_should_not_contain_button(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_checkbox(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_image(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_link(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_list(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_radio_button(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def page_should_not_contain_textfield(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        message: Optional[str] = None,
        loglevel: str = "TRACE",
    ): ...
    def press_key(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        key: str,
    ): ...
    def press_keys(
        self,
        locator: Optional[
            Union[selenium.webdriver.remote.webelement.WebElement, None, str]
        ] = None,
        *keys: str,
    ): ...
    def radio_button_should_be_set_to(self, group_name: str, value: str): ...
    def radio_button_should_not_be_selected(self, group_name: str): ...
    def register_keyword_to_run_on_failure(self, keyword: Union[str, None]): ...
    def reload_page(self): ...
    def remove_location_strategy(self, strategy_name: str): ...
    def scroll_element_into_view(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def select_all_from_list(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def select_checkbox(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def select_frame(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def select_from_list_by_index(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *indexes: str,
    ): ...
    def select_from_list_by_label(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *labels: str,
    ): ...
    def select_from_list_by_value(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *values: str,
    ): ...
    def select_radio_button(self, group_name: str, value: str): ...
    def set_browser_implicit_wait(self, value: timedelta): ...
    def set_focus_to_element(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def set_screenshot_directory(self, path: Union[None, str]): ...
    def set_selenium_implicit_wait(self, value: timedelta): ...
    def set_selenium_speed(self, value: timedelta): ...
    def set_selenium_timeout(self, value: timedelta): ...
    def set_window_position(self, x: int, y: int): ...
    def set_window_size(self, width: int, height: int, inner: bool = False): ...
    def simulate_event(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        event: str,
    ): ...
    def submit_form(
        self,
        locator: Optional[
            Union[selenium.webdriver.remote.webelement.WebElement, None, str]
        ] = None,
    ): ...
    def switch_browser(self, index_or_alias: str): ...
    def switch_window(
        self,
        locator: Union[list, str] = "MAIN",
        timeout: Optional[str] = None,
        browser: str = "CURRENT",
    ): ...
    def table_cell_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        row: int,
        column: int,
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def table_column_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        column: int,
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def table_footer_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def table_header_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def table_row_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        row: int,
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def table_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        expected: str,
        loglevel: str = "TRACE",
    ): ...
    def textarea_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ): ...
    def textarea_value_should_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ): ...
    def textfield_should_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ): ...
    def textfield_value_should_be(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        expected: str,
        message: Optional[str] = None,
    ): ...
    def title_should_be(self, title: str, message: Optional[str] = None): ...
    def unselect_all_from_list(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def unselect_checkbox(
        self, locator: Union[selenium.webdriver.remote.webelement.WebElement, str]
    ): ...
    def unselect_frame(self): ...
    def unselect_from_list_by_index(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *indexes: str,
    ): ...
    def unselect_from_list_by_label(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *labels: str,
    ): ...
    def unselect_from_list_by_value(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, str],
        *values: str,
    ): ...
    def wait_for_condition(
        self,
        condition: str,
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_element_contains(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        text: str,
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_element_does_not_contain(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        text: str,
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_element_is_enabled(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_element_is_not_visible(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_element_is_visible(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_location_contains(
        self,
        expected: str,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ): ...
    def wait_until_location_does_not_contain(
        self,
        location: str,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ): ...
    def wait_until_location_is(
        self,
        expected: str,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ): ...
    def wait_until_location_is_not(
        self,
        location: str,
        timeout: Optional[timedelta] = None,
        message: Optional[str] = None,
    ): ...
    def wait_until_page_contains(
        self,
        text: str,
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_page_contains_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
        limit: Optional[int] = None,
    ): ...
    def wait_until_page_does_not_contain(
        self,
        text: str,
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
    ): ...
    def wait_until_page_does_not_contain_element(
        self,
        locator: Union[selenium.webdriver.remote.webelement.WebElement, None, str],
        timeout: Optional[timedelta] = None,
        error: Optional[str] = None,
        limit: Optional[int] = None,
    ): ...
    # methods from library.
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
    def find_elements(self, locator: str, parent: WebElement = None): ...
    def _parse_plugins(self, plugins: Any): ...
    def _parse_plugin_doc(self): ...
    def _get_intro_documentation(self): ...
    def _parse_listener(self, event_firing_webdriver: Any): ...
    def _string_to_modules(self, modules: Any): ...
    def _store_plugin_keywords(self, plugin): ...
    def _resolve_screenshot_root_directory(self): ...
