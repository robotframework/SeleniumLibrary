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

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.text

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

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute('value')

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
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Select all from list' works only for multiselect lists.")

        for i in range(len(select.options)):
            select.select_by_index(i)

    def select_from_list(self, locator, *items):
        """Selects `*items` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*items` is an empty list, all values of the list will be selected.

        *items try to select by value then by label.

        It's faster to use 'by index/value/label' functions.

        An exception is raised for a single-selection list if the last
        value does not exist in the list and a warning for all other non-
        existing items. For a multi-selection list, an exception is raised
        for any and all non-existing values.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        non_existing_items = []

        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)

        if not items:
            for i in range(len(select.options)):
                select.select_by_index(i)
            return

        for item in items:
            try:
                select.select_by_value(item)
            except:
                try:
                    select.select_by_visible_text(item)
                except:
                    non_existing_items = non_existing_items + [item]
                    continue

        if any(non_existing_items):
            if select.is_multiple:
                raise ValueError("Options '%s' not in list '%s'." % (", ".join(non_existing_items), locator))
            else:
                if any (non_existing_items[:-1]):
                    items_str = non_existing_items[:-1] and "Option(s) '%s'" % ", ".join(non_existing_items[:-1])
                    self._warn("%s not found within list '%s'." % (items_str, locator))
                if items and items[-1] in non_existing_items:
                    raise ValueError("Option '%s' not in list '%s'." % (items[-1], locator))

    def select_from_list_by_index(self, locator, *indexes):
        """Selects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not indexes:
            raise ValueError("No index given.")
        items_str = "index(es) '%s'" % ", ".join(indexes)
        self._info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    def select_from_list_by_value(self, locator, *values):
        """Selects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not values:
            raise ValueError("No value given.")
        items_str = "value(s) '%s'" % ", ".join(values)
        self._info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    def select_from_list_by_label(self, locator, *labels):
        """Selects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not labels:
            raise ValueError("No value given.")
        items_str = "label(s) '%s'" % ", ".join(labels)
        self._info("Selecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    def unselect_from_list(self, locator, *items):
        """Unselects given values from select list identified by locator.

        As a special case, giving empty list as `*items` will remove all
        selections.

        *items try to unselect by value AND by label.

        It's faster to use 'by index/value/label' functions.

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        if not items:
            select.deselect_all()
            return

        select, options = self._get_select_list_options(select)
        for item in items:
            select.deselect_by_value(item)
            select.deselect_by_visible_text(item)

    def unselect_from_list_by_index(self, locator, *indexes):
        """Unselects `*indexes` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not indexes:
            raise ValueError("No index given.")

        items_str = "index(es) '%s'" % ", ".join(indexes)
        self._info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for index in indexes:
            select.deselect_by_index(int(index))

    def unselect_from_list_by_value(self, locator, *values):
        """Unselects `*values` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not values:
            raise ValueError("No value given.")
        items_str = "value(s) '%s'" % ", ".join(values)
        self._info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for value in values:
            select.deselect_by_value(value)

    def unselect_from_list_by_label(self, locator, *labels):
        """Unselects `*labels` from list identified by `locator`

        Select list keywords work on both lists and combo boxes. Key attributes for
        select lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        if not labels:
            raise ValueError("No value given.")
        items_str = "label(s) '%s'" % ", ".join(labels)
        self._info("Unselecting %s from list '%s'." % (items_str, locator))

        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        for label in labels:
            select.deselect_by_visible_text(label)

    # Private

    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels

    def _get_select_list(self, locator):
        el = self._element_find(locator, True, True, 'select')
        return Select(el)

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, Select):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.options

    def _get_select_list_options_selected(self, locator):
        select = self._get_select_list(locator)
        # TODO: Handle possible exception thrown by all_selected_options
        return select, select.all_selected_options

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

    def _unselect_all_options_from_multi_select_list(self, select):
        self._current_browser().execute_script("arguments[0].selectedIndex = -1;", select)

    def _unselect_option_from_multi_select_list(self, select, options, index):
        if options[index].is_selected():
            options[index].click()
