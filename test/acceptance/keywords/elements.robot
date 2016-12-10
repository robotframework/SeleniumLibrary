*** Settings ***
Documentation     Tests elements
Test Setup        Go To Page "links.html"
Resource          ../resource.robot

*** Test Cases ***
Get Elements
    [Documentation]    Get Elements
    @{links}=    Get WebElements    //div[@id="div_id"]/a
    Length Should Be    ${links}    11

Get Web Element
    [Documentation]    Get Web Element
    @{links}=    Get WebElements    //div[@id="div_id"]/a
    ${link}=    Get WebElement    //div[@id="div_id"]/a
    Should Be Equal    @{links}[0]    ${link}
    Run Keyword and Expect Error
    ...    ValueError: Element locator 'id=non_existing_elem' did not match any elements.
    ...    Get WebElement    id=non_existing_elem

More Get Elements
    [Documentation]    More Get Elements
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    @{checkboxes}=    Get WebElements    //input[@type="checkbox"]
    Length Should Be    ${checkboxes}    2
    : FOR    ${checkbox}    IN    @{checkboxes}
    \    Unselect Checkbox    ${checkbox}
    : FOR    ${checkbox}    IN    @{checkboxes}
    \    Checkbox Should Not Be Selected    ${checkbox}
    : FOR    ${checkbox}    IN    @{checkboxes}
    \    Select Checkbox    ${checkbox}
    : FOR    ${checkbox}    IN    @{checkboxes}
    \    Checkbox Should Be Selected    ${checkbox}

Assign Id To Element
    [Documentation]    Tests also Reload Page keyword.
    Page Should Not Contain Element    my id
    Assign ID to Element    xpath=//div[@id="first_div"]    my id
    Page Should Contain Element    my id
    Reload Page
    Page Should Not Contain Element    my id

Get Element Attribute
    [Documentation]    Get Element Attribute
    ${id}=    Get Element Attribute    link=Link with id@id
    Should Be Equal    ${id}    some_id
    ${id}=    Get Element Attribute    dom=document.getElementsByTagName('a')[3]@id
    Should Be Equal    ${id}    some_id
    ${class}=    Get Element Attribute    second_div@class
    Should Be Equal    ${class}    Second Class

Get Matching XPath Count
    [Documentation]    Get Matching XPath Count
    ${count}=    Get Matching XPath Count    //a
    Should Be Equal    ${count}    19
    ${count}=    Get Matching XPath Count    //div[@id="first_div"]/a
    Should Be Equal    ${count}    2

Get Horizontal Position
    [Documentation]    Get Horizontal Position
    ${pos}=    Get Horizontal Position    link=Link
    Should Be True    ${pos} > ${0}
    Run Keyword And Expect Error    Could not determine position for 'non-existent'
    ...    Get Horizontal Position    non-existent

Get Vertical Position
    [Documentation]    Get Vertical Position
    ${pos}=    Get Vertical Position    link=Link
    Should Be True    ${pos} > ${0}
    Run Keyword And Expect Error    Could not determine position for 'non-existent'
    ...    Get Horizontal Position    non-existent


Get Element Size
    ${width}  ${height}=  Get Element Size  link=Link
    Should be True  ${height} > ${0}
    Should be True  ${width} > ${0}
    Run Keyword And Expect Error  ValueError: Element locator 'non-existent' did not match any elements.  Get Element Size  non-existent

Get Empty Element Size
    [Tags]  Known Issue Internet Explorer
    ${width}  ${height}=  Get Element Size  id=emptyDiv
    Should be True  ${height} == 0
