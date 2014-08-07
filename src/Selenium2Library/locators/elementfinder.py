from Selenium2Library import utils
from robot.api import logger

class ElementFinder(object):

    def __init__(self):
        self._strategies = {
            'identifier': self._find_by_identifier,
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'dom': self._find_by_dom,
            'link': self._find_by_link_text,
            'css': self._find_by_css_selector,
            'jquery': self._find_by_sizzle_selector,
            'sizzle': self._find_by_sizzle_selector,
            'tag': self._find_by_tag_name,
            'binding': self._find_by_binding,
            'model': self._find_by_model,
            'repeater': self._find_by_ng_repeater,
            None: self._find_by_default
        }

    def find(self, browser, locator, tag=None):
        assert browser is not None
        assert locator is not None and len(locator) > 0

        (prefix, criteria) = self._parse_locator(locator)
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        (tag, constraints) = self._get_tag_and_constraints(tag)
        return strategy(browser, criteria, tag, constraints)

    # Strategy routines, private

    def _find_by_identifier(self, browser, criteria, tag, constraints):
        elements = self._normalize_result(browser.find_elements_by_id(criteria))
        elements.extend(self._normalize_result(browser.find_elements_by_name(criteria)))
        return self._filter_elements(elements, tag, constraints)

    def _find_by_id(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_id(criteria),
            tag, constraints)

    def _find_by_name(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_name(criteria),
            tag, constraints)

    def _find_by_xpath(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_xpath(criteria),
            tag, constraints)

    def _find_by_dom(self, browser, criteria, tag, constraints):
        result = browser.execute_script("return %s;" % criteria)
        if result is None:
            return []
        if not isinstance(result, list):
            result = [result]
        return self._filter_elements(result, tag, constraints)

    def _find_by_sizzle_selector(self, browser, criteria, tag, constraints):
        js = "return jQuery('%s').get();" % criteria.replace("'", "\\'")
        return self._filter_elements(
            browser.execute_script(js),
            tag, constraints)

    def _find_by_link_text(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_link_text(criteria),
            tag, constraints)

    def _find_by_css_selector(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_css_selector(criteria),
            tag, constraints)

    def _find_by_tag_name(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.find_elements_by_tag_name(criteria),
            tag, constraints)

    def _find_by_binding(self, browser, criteria, tag, constraints):
        return self._filter_elements(
            browser.execute_script("var binding = '%s'; var bindings = document.getElementsByClassName('ng-binding'); var matches = []; for (var i = 0; i < bindings.length; ++i) { var dataBinding = angular.element(bindings[i]).data('$binding'); if(dataBinding) { var bindingName = dataBinding.exp || dataBinding[0].exp || dataBinding; if (bindingName.indexOf(binding) != -1) { matches.push(bindings[i]); } } } return matches;" % criteria),
            tag, constraints)

    def _find_by_model(self, browser, criteria, tag, constraints):
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\:']
        for prefix in prefixes:
            selector = '[%smodel="%s"]' % (prefix, criteria)
            elements = browser.execute_script("""return document.querySelectorAll('%s');""" % selector);
            if len(elements):
                return self._filter_elements(elements, tag, constraints)

    def _find_by_ng_repeater(self, browser, criteria, tag, constraints):
        matches=[]
        repeater_row_col = self._parse_ng_repeat_locator(criteria)

        import collections
        def get_iterable(x):
            if isinstance(x, collections.Iterable):
                return x
            else:
                return [x]
        
        rows = []
        prefixes = ['ng-', 'ng_', 'data-ng-', 'x-ng-', 'ng\\\\:']
        for prefix in prefixes:
            #import pdb,sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            repeatElems=[]
            attr = prefix + 'repeat'
            try:
                repeatElems = browser.execute_script("""return document.querySelectorAll('[%s]');""" % attr)
            except:
                print attr
            attr = attr.replace('\\','')
            repeatElems = get_iterable(repeatElems)
            for elem in repeatElems:
                val = elem.get_attribute(attr)
                print val
                if val and repeater_row_col['repeater'] in elem.get_attribute(attr):
                    rows.append(elem)
        multiRows = []
        for prefix in prefixes:
            attr = prefix + 'repeat-start'
            repeatElems = browser.execute_script("""return document.querySelectorAll('[%s]');""" % attr)
            attr = attr.replace('\\','')
            for elem in repeatElems:
                if repeater_row_col['repeater'] in elem.get_attribute(attr):
                    item = elem
                    is_end = item.get_attribute('ng-repeat-end')
                    row = []
                    while is_end!='':
                        row.append(item)
                        try:
                            is_end = item.get_attribute('ng-repeat-end')
                            item = item.find_element_by_xpath('./following-sibling::*')
                        except:
                            item = None
                            is_end = ''
                    multiRows.append(row)

        # if ...@row[index]...
        if repeater_row_col['row_index'] is not None:
            #import pdb,sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            if rows:
                rows = get_iterable(rows[repeater_row_col['row_index']])
            if multiRows:
                multiRows = get_iterable(multiRows[repeater_row_col['row_index']])

        # if ...@col=binding... 
        if repeater_row_col['col_binding'] is not None:
            #import pdb,sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
            from selenium.common.exceptions import NoSuchElementException
            bindings=[]
            for row in rows:
                if 'ng-binding' in row.get_attribute("class"):
                    bindings.append(row)
                try:
                    childBindings = row.find_elements_by_class_name('ng-binding')
                    bindings.extend(childBindings)
                except NoSuchElementException:
                    pass
            
            for row in multiRows:
                for elem in row:
                    if 'ng-binding' in elem.get_attribute("class"):
                        bindings.append(elem)
                    try:
                        childBindings = elem.find_elements_by_class_name('ng-binding')
                        bindings.extend(childBindings)
                    except NoSuchElementException:
                        pass
            
            for bind in bindings:
                bindingName = browser.execute_script("dataBinding=angular.element(arguments[0]).data('$binding');if(dataBinding){bindingName=dataBinding.exp||dataBinding[0].exp||dataBinding;}return bindingName;",bind)
                if repeater_row_col['col_binding'] in bindingName:
                    matches.append(bind)
            return matches
        
        #import pdb,sys; pdb.Pdb(stdout=sys.__stdout__).set_trace()
        matches = rows
        matches.extend(multiRows)
        return matches

    def _find_by_default(self, browser, criteria, tag, constraints):
        if criteria.startswith('//'):
            return self._find_by_xpath(browser, criteria, tag, constraints)
        elif criteria.startswith('{{'):
            return self._find_by_binding(browser, criteria, tag, constraints)
        return self._find_by_key_attrs(browser, criteria, tag, constraints)

    def _find_by_key_attrs(self, browser, criteria, tag, constraints):
        key_attrs = self._key_attrs.get(None)
        if tag is not None:
            key_attrs = self._key_attrs.get(tag, key_attrs)

        xpath_criteria = utils.escape_xpath_value(criteria)
        xpath_tag = tag if tag is not None else '*'
        xpath_constraints = ["@%s='%s'" % (name, constraints[name]) for name in constraints]
        xpath_searchers = ["%s=%s" % (attr, xpath_criteria) for attr in key_attrs]
        xpath_searchers.extend(
            self._get_attrs_with_url(key_attrs, criteria, browser))
        xpath = "//%s[%s(%s)]" % (
            xpath_tag,
            ' and '.join(xpath_constraints) + ' and ' if len(xpath_constraints) > 0 else '',
            ' or '.join(xpath_searchers))

        return self._normalize_result(browser.find_elements_by_xpath(xpath))

    # Private

    _key_attrs = {
        None: ['@id', '@name'],
        'a': ['@id', '@name', '@href', 'normalize-space(descendant-or-self::text())'],
        'img': ['@id', '@name', '@src', '@alt'],
        'input': ['@id', '@name', '@value', '@src'],
        'button': ['@id', '@name', '@value', 'normalize-space(descendant-or-self::text())']
    }

    def _get_tag_and_constraints(self, tag):
        if tag is None: return None, {}

        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = 'text'
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        elif tag == 'text area':
            tag = 'textarea'
        return tag, constraints

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if not element.get_attribute(name) == constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None: return elements
        return filter(
            lambda element: self._element_matches(element, tag, constraints),
            elements)

    def _get_attrs_with_url(self, key_attrs, criteria, browser):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url(browser) + "/" + criteria
                    xpath_url = utils.escape_xpath_value(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self, browser):
        url = browser.get_current_url()
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//') and not locator.startswith('{{'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return (prefix, criteria)

    def _parse_ng_repeat_locator(self, criteria):
        def _startswith(str,sep):
            parts = str.lower().partition(sep)
            if parts[1]==sep and parts[0]=='':
                return parts[2]
            else:
                return None
        
        
        def _parse_arrayRE(str):
            import re
            match = re.search(r"(?<=^\[).+([0-9]*).+(?=\]$)",str)
            if match:
                return match.group()
            else:
                return None
        
        def _parse_array(str):
            if str[0]=='[' and str[-1]==']':
                return int(str[1:-1])
            else:
                return None

        rrc = criteria.rsplit('@')
        extractElem = {'repeater': None, 'row_index': None, 'col_binding': None}
        if len(rrc)==1:
            #is only repeater
            extractElem['repeater']=rrc[0]
            return extractElem
        else:
            # for index in reversed(rrc):
            while 1 < len(rrc):
                index = rrc.pop()
                row = _startswith(index,'row')
                column = _startswith(index,'column')
                if row:
                    array = _parse_array(row)
                    rlocator = _startswith(row,'=')
                    if array is not None:
                        extractElem['row_index'] = array
                        print array
                    elif rlocator:
                        # row should be an list index and not binding locator
                        print rlocator
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                elif column:
                    array = _parse_array(column)
                    clocator = _startswith(column,'=')
                    if array is not None:
                        # col should be an binding locator and not list index
                        print array
                    elif clocator:
                        extractElem['col_binding'] = clocator
                        print clocator
                    else:
                        # stray @ not releated to row/column seperator
                        rrc[-1] = rrc[-1] + '@' + index
                else:
                    # stray @ not releated to row/column seperator
                    rrc[-1] = rrc[-1] + '@' + index
        extractElem['repeater']=rrc[0]
        return extractElem

    def _normalize_result(self, elements):
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements
