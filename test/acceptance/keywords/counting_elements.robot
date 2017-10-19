*** Settings ***
Test Setup        Go To Front Page
Default Tags      element count
Resource          ../resource.robot
Library           String

*** Test Cases ***
Get Matching XPath Count
    [Documentation]    Deprecated
    [Setup]    Go To Page "links.html"
    ${count}=    Get Matching XPath Count    //a
    Should Be Equal    ${count}    19
    ${count}=    Get Matching XPath Count    //a    ${True}
    Should Be Equal    ${count}    19
    Should Be String    ${count}
    ${count}=    Get Matching XPath Count    //a    ${False}
    Should Be Equal    ${count}    ${19}
    Should Not Be String    ${count}
    ${count}=    Get Matching XPath Count    //div[@id="first_div"]/a
    Should Be Equal    ${count}    2

Xpath Should Match X Times
    [Documentation]    Deprecated
    [Setup]    Go To Page "forms/login.html"
    Xpath Should Match X Times      //input[@type="text"]    1
    Xpath Should Match X Times      //input[@type="text"]    ${1}
    Run Keyword And Expect Error
    ...    Locator 'xpath://input[@type="text"]' should have matched 2 times but matched 1 time.
    ...    Xpath Should Match X Times    //input[@type="text"]    2

Locator Should Match X Times
    [Documentation]    Deprecated
    [Setup]    Go To Page "links.html"
    Locator Should Match X Times    link=Link    2
    Locator Should Match X Times    link=Missing Link    0
    Locator Should Match X Times    name:div_name    2
    Locator Should Match X Times    xpath://*[@name="div_name"]    2

Locator Should Match X Times Error
    [Documentation]    Deprecated
    [Setup]    Go To Page "links.html"
    Run Keyword And Expect Error
    ...    Locator 'name: div_name' should have matched 3 times but matched 2 times.
    ...    Locator Should Match X Times    name: div_name    3
    Run Keyword And Expect Error
    ...    Custom error
    ...    Locator Should Match X Times    name:div_name    3    Custom error

Get Element Count With Xpath Locator
    [Setup]    Go To Page "links.html"
    ${count} =     Get Element Count    xpath://*[@name="div_name"]
    Should Be Equal    ${count}    ${2}
    ${count} =     Get Element Count    //*[@name="div_name"]
    Should Be Equal    ${count}    ${2}

Get Element Count With Default Locator
    [Setup]    Go To Page "links.html"
    ${count} =     Get Element Count    div_name
    Should Be Equal    ${count}    ${2}

Get Element Count With Name Locator
    [Setup]    Go To Page "links.html"
    ${count} =     Get Element Count    name:div_name
    Should Be Equal    ${count}    ${2}

Get Element Count Should Not Fail When Zero Elements Is Found
    [Setup]    Go To Page "links.html"
    ${count} =     Get Element Count    name:not_exist
    Should Be Equal    ${count}    ${0}
