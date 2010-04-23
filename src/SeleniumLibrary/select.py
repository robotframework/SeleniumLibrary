#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

class Select(object):
        
    def list_selection_should_be(self, locator, *values):
        """Verifies the selection of list identified by `locator` is exactly `*values`.
        
        If you want to test that no option is selected, simply give no `values`.
        Key attributes for list are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        opts = values and 'options [ %s ]' % ' | '.join(values) or 'no options'
        self._info("Verifying list '%s' has %s selected." % (locator, opts))
        self.page_should_contain_list(locator)
        xpath = self._parse_locator(locator, 'select')
        try:
            selected_values = self._selenium.get_selected_values(xpath)
            selected_labels = self._selenium.get_selected_labels(xpath)
        except Exception, err:
            if not values and 'No option selected' in self._get_error_message(err):
                return
            raise # Means that something unexpecet happened in Selenium.
        else:
            msg = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
                   % (locator, ' | '.join(values), ' | '.join(selected_labels))
            for expvalue in values:
                if expvalue not in selected_labels + selected_values:
                    raise AssertionError(msg)          
            for label, value in zip(selected_labels, selected_values):
                if label not in values and value not in values:
                    raise AssertionError(msg)
   
    def select_from_list(self, locator, *values):
        """Selects `*values` from list identified by `locator`
        
        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*values` is an empty list, all values of the list will be selected.
        
        Key attributes for list are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        selection = values and "values '%s'" % ', '.join(values) or 'all values'
        self._info("Selecting %s from list '%s'." % (selection, locator))
        locator = self._parse_locator(locator, 'select')
        values = list(values)
        if len(values) == 0:
            values = self._selenium.get_select_options(locator)
        if self._is_multiselect_list(locator):
            self._select_from_multiselect_list(locator, values)
        else:
            self._select_from_singleselect_list(locator, values)

    def _select_from_multiselect_list(self, locator, selection):
        self._call_method_for_list_elements('add_selection', locator, selection)

    def _select_from_singleselect_list(self, locator, selection):
        self._call_method_for_list_elements('select', locator, selection)

    def _is_multiselect_list(self, locator):
        try:
            self._selenium.get_attribute(locator+'@multiple')
            return True
        except Exception, err:
            if 'attribute: %s@multiple' % locator in self._get_error_message(err):
                return False
            else:
                raise

    def _call_method_for_list_elements(self, method_name, locator, elements):
        method = getattr(self._selenium, method_name)
        for elem in elements:
            try:
                method(locator, elem)
            except:
                method(locator, 'value=%s'%elem)
            
    def unselect_from_list(self, locator, *values):
        """Unselects given values from list identified by locator.
        
        As a special case, giving empty list as `*selection` will remove all 
        selections.
        
        Key attributes for list are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        selection = values and "values '%s'" % ', '.join(values) or 'all values'
        self._info("Unselecting %s from list '%s'." % (selection, locator))
        locator = self._parse_locator(locator, 'select')
        if not self._is_multiselect_list(locator):
            raise RuntimeError("Keyword 'Unselect from list' works only for "
                               "multiselect lists")
        if len(values) == 0:
            self._selenium.remove_all_selections(locator)
        else:
            self._call_method_for_list_elements('remove_selection', locator,
                                                list(values))
            
    def select_all_from_list(self, locator, wait=''):
        """Selects all values from multi-select list identified by `id`.
        
        Key attributes for list are `id` and `name`. See `introduction` for
        details about locating elements and about `wait` argument.
        """
        self._info("Selecting all values from list '%s'." % locator)
        locator = self._parse_locator(locator, 'select')
        selected_items = [] 
        if self._selenium.is_something_selected(locator):
            selected_items = self._selenium.get_selected_labels(locator)
        for item in self._selenium.get_select_options(locator):
            if not item in selected_items:
                self._add_to_selection(locator, item)
                if wait:
                    self._wait_for_page_to_load()
                    
    def _add_to_selection(self, locator, item):
        try:
            self._selenium.add_selection(locator, item)
        except Exception, err:
            if "Not a multi-select" in self._get_error_message(err):
                raise RuntimeError("Keyword 'Select all from list' works only "
                                   "for multiselect lists.")
            raise
            
    def list_should_have_no_selections(self, locator):
        """Verifies list identified by `locator` has no selections.
        
        Key attributes for list are `id` and `name`. See `introduction` for
        more details on key attributes and locating elements.
        """
        self._info("Verifying list '%s' has no selection." % locator)
        _locator = self._parse_locator(locator, 'select')
        if self._selenium.is_something_selected(_locator):
            selection = ' | '.join(self._selenium.get_selected_labels(_locator))
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, selection))

