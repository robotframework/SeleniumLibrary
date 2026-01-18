*** Settings ***
Documentation     Tests elements
Test Setup        Go To Page "links.html"
Resource          ../resource.robot
Library           String

*** Test Cases ***
Get Many Elements
    @{links}=    Get WebElements    //div[@id="div_id"]/a
    Length Should Be    ${links}    12

Get Zero Elements
    ${no_elements} =     Get WebElements    id:non_existing_elem
    Should Be Empty    ${no_elements}

Get Web Element
    @{links}=    Get WebElements    //div[@id="div_id"]/a
    ${link}=    Get WebElement    //div[@id="div_id"]/a
    Should Be Equal    ${links}[0]    ${link}

Get Web Element Should Fail If Element Is Not Found
    Run Keyword and Expect Error
    ...    Element with locator 'id=non_existing_elem' not found.
    ...    Get WebElement    id=non_existing_elem

More Get Elements
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    @{checkboxes}=    Get WebElements    //input[@type="checkbox"]
    Length Should Be    ${checkboxes}    2
    FOR    ${checkbox}    IN    @{checkboxes}
        Unselect Checkbox    ${checkbox}
    END
    FOR    ${checkbox}    IN    @{checkboxes}
        Checkbox Should Not Be Selected    ${checkbox}
    END
    FOR    ${checkbox}    IN    @{checkboxes}
        Select Checkbox    ${checkbox}
    END
    FOR    ${checkbox}    IN    @{checkboxes}
        Checkbox Should Be Selected    ${checkbox}
    END

Assign Id To Element
    Page Should Not Contain Element    my id
    Assign ID to Element    xpath=//div[@id="first_div"]    my id
    Page Should Contain Element    my id
    Reload Page
    Page Should Not Contain Element    my id

Get Element Attribute
    ${id}=    Get Element Attribute    link:Link with id    id
    Should Be Equal    ${id}    some_id
    ${id}=    Get Element Attribute    dom:document.getElementsByTagName('a')[3]    id
    Should Be Equal    ${id}    some_id
    ${class}=    Get Element Attribute    second_div    class
    Should Be Equal    ${class}    Second Class
    ${id}=    Get Element Attribute    link=Link with id    id
    Should Be Equal    ${id}    some_id
    ${second_div}=    Get Webelement    second_div
    ${class}=    Get Element Attribute    ${second_div}    class
    Should Be Equal    ${class}    Second Class

# About DOM Attributes and Properties
# -----------------------------------
# When implementing the new `Get DOM Attirbute` and `Get Property` keywords (#1822), several
# questions were raised. Fundamentally what is the difference between a DOM attribute and
# a Property. As [1] explains "Attributes are defined by HTML. Properties are defined by the
# DOM (Document Object Model)."
#
# Below are some references which talk to some descriptions and oddities of DOM attributes
# and properties.
#
# References:
#    [1] HTML attributes and DOM properties:
#      https://angular.io/guide/binding-syntax#html-attribute-vs-dom-property
#    [2] W3C HTML Specification - Section 13.1.2.3 Attributes:
#      https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
#    [3] JavaScript.Info - Attributes and properties:
#      https://javascript.info/dom-attributes-and-properties
#    [4] "Which CSS properties are inherited?" - StackOverflow
#      https://stackoverflow.com/questions/5612302/which-css-properties-are-inherited
#    [5] MDN Web Docs: Attribute
#      https://developer.mozilla.org/en-US/docs/Glossary/Attribute
#    [6] MDN Web Docs: HTML attribute reference
#      https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes

Get DOM Attribute
    # Test get DOM attribute
    ${id}=    Get DOM Attribute    link:Link with id    id
    Should Be Equal    ${id}    some_id
    # Test custom attribute
    ${existing_custom_attr}=   Get DOM Attribute    id:emptyDiv  data-id
    Should Be Equal    ${existing_custom_attr}    my_id
    ${doesnotexist_custom_attr}=   Get DOM Attribute    id:emptyDiv  data-doesnotexist
    Should Be Equal    ${doesnotexist_custom_attr}    ${None}
    # Get non existing DOM Attribute
    ${class}=    Get DOM Attribute    link:Link with id    class
    Should Be Equal    ${class}    ${NONE}

More DOM Attributes
    [Setup]    Go To Page "forms/enabled_disabled_fields_form.html"
    # Test get empty boolean attribute
    ${disabled}=    Get DOM Attribute    css:input[name="disabled_input"]    disabled
    Should Be Equal    ${disabled}    true
    # Test boolean attribute whose value is a string
    ${disabled}=    Get DOM Attribute    css:input[name="disabled_password"]    disabled
    Should Be Equal    ${disabled}    true
    # Test empty string as the value for the attribute
    ${empty_value}=    Get DOM Attribute    css:input[name="disabled_password"]    value
    Should Be Equal    ${empty_value}    ${EMPTY}
    # Test non-existing attribute
    ${disabled}=    Get DOM Attribute    css:input[name="enabled_password"]    disabled
    Should Be Equal    ${disabled}    ${NONE}

Get Property
    [Setup]    Go To Page "forms/enabled_disabled_fields_form.html"
    ${tagName_prop}=   Get Property  css:input[name="readonly_empty"]    tagName
    Should Be Equal    ${tagName_prop}    INPUT
    # Get a boolean property
    ${isConnected}=   Get Property  css:input[name="readonly_empty"]     isConnected
    Should Be Equal    ${isConnected}    ${True}
    # Test property which returns webelement
    ${children_prop}=    Get Property    id:table1    children
    Length Should Be    ${children_prop}    ${1}
    ${isWebElement}=  Evaluate  isinstance($children_prop[0], selenium.webdriver.remote.webelement.WebElement)  modules=selenium
    Should Be Equal    ${isWebElement}    ${True}
    # ToDo: need to test own versus inherited property
    # ToDo: Test enumerated property

Get "Attribute" That Is Both An DOM Attribute and Property
    [Setup]    Go To Page "forms/enabled_disabled_fields_form.html"
    ${value_property}=    Get Property  css:input[name="readonly_empty"]   value
    ${value_attribute}=    Get DOM Attribute  css:input[name="readonly_empty"]   value
    Should Be Equal    ${value_property}    ${value_attribute}

Modify "Attribute" That Is Both An DOM Attribute and Property
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    ${initial_value_property}=    Get Property  css:input[name="email"]   value
    ${initial_value_attribute}=    Get DOM Attribute  css:input[name="email"]   value
    Should Be Equal    ${initial_value_property}    ${initial_value_attribute}
    Should Be Equal    ${initial_value_attribute}    Prefilled Email
    Input Text    css:input[name="email"]    robot@robotframework.org
    ${changed_value_property}=    Get Property  css:input[name="email"]   value
    ${changed_value_attribute}=    Get DOM Attribute  css:input[name="email"]   value
    Should Not Be Equal    ${changed_value_property}    ${changed_value_attribute}
    Should Be Equal    ${changed_value_attribute}    Prefilled Email
    Should Be Equal    ${changed_value_property}    robot@robotframework.org

Get Element Attribute Value Should Be Should Be Succesfull
    Element Attribute Value Should Be  link=Absolute external link  href  http://www.google.com/
    Element Attribute Value Should Be  link=Absolute external link  nothere  ${None}


Get Element Attribute And Element Attribute Value Should Be Should have same results
    ${attribute_value}=  Get Element Attribute  css=#second_div  class
    Element Attribute Value Should Be  css=#second_div  class  ${attribute_value}

Get Element Attribute Value Should Be Should Be Succesfull with non-ascii characters
    Element Attribute Value Should Be  link=Link with Unicode äöüÄÖÜß  href  ${FRONT_PAGE}index.html

Get Element Attribute Value Should Be Should Be Succesfull error and error messages
    Run Keyword And Expect Error
    ...    Test Fail Custom Message
    ...    Element Attribute Value Should Be  id=image_id  href  http://non_existing.com  message=Test Fail Custom Message
    Run Keyword And Expect Error
    ...    Element 'id=image_id' attribute should have value 'http://non_existing.com' (str) but its value was 'None' (nonetype).
    ...    Element Attribute Value Should Be  id=image_id  href  http://non_existing.com
    Run Keyword And Expect Error
    ...    Element with locator 'id=non_existing' not found.
    ...    Element Attribute Value Should Be  id=non_existing  href  http://non_existing.com
    Run Keyword And Expect Error
    ...    Element 'link=Target opens in new window' attribute should have value '${FRONT_PAGE}indéx.html' (str) but its value was '${FRONT_PAGE}index.html' (str).
    ...    Element Attribute Value Should Be  link=Target opens in new window  href  ${FRONT_PAGE}indéx.html

Get Horizontal Position
    ${pos}=    Get Horizontal Position    link=Link
    Should Be True    ${pos} > 0
    Run Keyword And Expect Error
    ...    Element with locator 'non-existent' not found.
    ...    Get Horizontal Position    non-existent

Get Vertical Position
    ${pos}=    Get Vertical Position    link=Link
    Should Be True    ${pos} > 0
    Run Keyword And Expect Error
    ...    Element with locator 'non-existent' not found.
    ...    Get Horizontal Position    non-existent

Get Element Size
    ${width}  ${height}=  Get Element Size  link=Link
    Should be True  ${height} > 0
    Should be True  ${width} > 0
    Run Keyword And Expect Error
    ...    Element with locator 'non-existent' not found.
    ...    Get Element Size  non-existent

Get Empty Element Size
    [Tags]  Known Issue Internet Explorer
    ${width}  ${height}=  Get Element Size  id=emptyDiv
    Should be Equal    ${height}    ${0}

Cover Element
    Cover Element  //img[@src="image.jpg"]
    Element Should Not be Visible  //img[@src="image.jpg"]
    Element Should be Visible  //div[@name="covered"]

Cover Element should cover all matching elements
    Cover Element  //img[@src="image.jpg"]
    Element Should Not be Visible  //img[@src="image.jpg"]
    ${count}  Get Element Count  //div[@name="covered"]
    Should Be equal As Integers  ${count}  2

Cover Element can cover just one element
    Cover Element  (//img[@src="image.jpg"])[1]
    Element Should be Visible  //img[@src="image.jpg"]
    ${count}  Get Element Count  //div[@name="covered"]
    Should Be equal As Integers  ${count}  1

Cover Elements should throw exception when locator is invalid
    Run Keyword And Expect Error  No element with locator '//img?@src="inexistent"?' found.
    ...  Cover Element  //img[@src="inexistent"]