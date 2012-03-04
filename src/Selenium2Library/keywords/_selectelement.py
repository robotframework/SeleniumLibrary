from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from keywordgroup import KeywordGroup

class _SelectElementKeywords(KeywordGroup):

    # Public

    def get_list_items(self, locator):
        """Returns the values in the select list identified by `locator`.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select, options = self._get_select_list_options(locator)
        return self._get_labels_for_options(options)

    def get_selected_list_label(self, locator):
        """Returns the visible label of the selected element from the select list identified by `locator`.

        Fails if there are zero or more than one selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        labels = self.get_selected_list_labels(locator)
        if len(labels) != 1:
            raise ValueError("Select list with locator '%s' does not have a single selected value")
        return labels[0]

    def get_selected_list_labels(self, locator):
        """Returns the visible labels of selected elements (as a list) from the select list identified by `locator`.

        Fails if there is no selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select, options = self._get_select_list_options_selected(locator)
        if len(options) == 0:
            raise ValueError("Select list with locator '%s' does not have any selected values")
        return self._get_labels_for_options(options)

    def get_selected_list_value(self, locator):
        """Returns the value of the selected element from the select list identified by `locator`.

        Return value is read from `value` attribute of the selected element.
        Fails if there are zero or more than one selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        values = self.get_selected_list_values(locator)
        if len(values) != 1:
            raise ValueError("Select list with locator '%s' does not have a single selected value")
        return values[0]

    def get_selected_list_values(self, locator):
        """Returns the values of selected elements (as a list) from the select list identified by `locator`.

        Fails if there is no selection.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select, options = self._get_select_list_options_selected(locator)
        if len(options) == 0:
            raise ValueError("Select list with locator '%s' does not have any selected values")
        return self._get_values_for_options(options)

    def list_selection_should_be(self, locator, *items):
        """Verifies the selection of select list identified by `locator` is exactly `*items`.

        If you want to test that no option is selected, simply give no `items`.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) [ %s ]" % " | ".join(items) or "no options"
        self._info("Verifying list '%s' has %s selected." % (locator, items_str))
        items = list(items)
        self.page_should_contain_list(locator)
        select, options = self._get_select_list_options_selected(locator)
        if not items and len(options) == 0:
            return
        selected_values = self._get_values_for_options(options)
        selected_labels = self._get_labels_for_options(options)
        err = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
            % (locator, ' | '.join(items), ' | '.join(selected_labels))
        for item in items:
            if item not in selected_values + selected_labels:
                raise AssertionError(err)
        for selected_value, selected_label in zip(selected_values, selected_labels):
            if selected_value not in items and selected_label not in items:
                raise AssertionError(err)

    def list_should_have_no_selections(self, locator):
        """Verifies select list identified by `locator` has no selections.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Verifying list '%s' has no selection." % locator)
        select, options = self._get_select_list_options_selected(locator)
        if options:
            selected_labels = self._get_labels_for_options(options)
            items_str = " | ".join(selected_labels)
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, items_str))

    def page_should_contain_list(self, locator, message='', loglevel='INFO'):
        """Verifies select list identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_contain_element(locator, 'list', message, loglevel)

    def page_should_not_contain_list(self, locator, message='', loglevel='INFO'):
        """Verifies select list identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'list', message, loglevel)

    def select_all_from_list(self, locator):
        """Selects all values from multi-select list identified by `id`.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._info("Selecting all options from list '%s'." % locator)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Select all from list' works only for multiselect lists.")

        select, options = self._get_select_list_options(select)
        for i in range(len(options)):
            self._select_option_from_multi_select_list(select, options, i)

    def select_from_list(self, locator, *items):
        """Selects `*items` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*items` is an empty list, all values of the list will be selected.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Selecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select, options = self._get_select_list_options(locator)
        is_multi_select = self._is_multiselect_list(select)
        select_func = self._select_option_from_multi_select_list if is_multi_select else self._select_option_from_single_select_list

        if not items:
            for i in range(len(options)):
                select_func(select, options, i)
            return

        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            select_func(select, options, option_index)

    def unselect_from_list(self, locator, *items):
        """Unselects given values from select list identified by locator.

        As a special case, giving empty list as `*items` will remove all
        selections.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Unselecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        if not items:
            self._unselect_all_options_from_multi_select_list(select)
            return

        select, options = self._get_select_list_options(select)
        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            self._unselect_option_from_multi_select_list(select, options, option_index)

    # Private
    
    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels

    def _get_select_list(self, locator):
        return self._element_find(locator, True, True, 'select')

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, WebElement):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.find_elements_by_tag_name('option')

    def _get_select_list_options_selected(self, select_list_or_locator):
        select, options = self._get_select_list_options(select_list_or_locator)
        selected = []
        for option in options:
            if option.is_selected():
                selected.append(option)
        return select, selected
    
    def _get_values_for_options(self, options):
        values = []
        for option in options:
             values.append(option.get_attribute('value'))
        return values

    def _is_multiselect_list(self, select):
        multiple_value = select.get_attribute('multiple')
        if multiple_value is not None and (multiple_value == 'true' or multiple_value == 'multiple'):
            return True
        return False

    def _select_option_from_multi_select_list(self, select, options, index):
        if not options[index].is_selected():
            options[index].click()

    def _select_option_from_single_select_list(self, select, options, index):
        sel = Select(select)
        sel.select_by_index(index)


    def _unselect_all_options_from_multi_select_list(self, select):
        self._current_browser().execute_script("arguments[0].selectedIndex = -1;", select)

    def _unselect_option_from_multi_select_list(self, select, options, index):
        if options[index].is_selected():
            options[index].click()
