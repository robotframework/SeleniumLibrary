import unittest

from SeleniumLibrary.keywords import ExpectedConditionKeywords

# Test cases

# Parsing expected condition
# expect to match ..
#    element_to_be_clickable
#    Element To Be Clickable
#    eLEment TO be ClIcKable
# expect to not match ..
#    element__to_be_clickable
#    elementtobeclickable
#    element_to_be_clickble
#    Ice Cream Cone Has Three Scopes

# what about ..?
#    ${ec_var}
#    Element\ To\ Be\ Clickable
#    Element${SPACE}To${SPACE}Be${SPACE}Clickable

class ExpectedConditionKeywords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ec_keywords = ExpectedConditionKeywords(None)

    def WorkInProgresstest_parse_condition(self):
        results = []
        results.append(self.ec_keywords._parse_condition("Element To Be Clickable"))
        results.append(self.ec_keywords._parse_condition("eLEment TO be ClIcKable"))
