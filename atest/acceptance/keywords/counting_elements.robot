*** Settings ***
Test Setup        Go To Front Page
Default Tags      element count
Resource          ../resource.robot
Library           String

*** Test Cases ***
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

Page Should Contain Element When Limit Is None
    [Setup]    Go To Page "links.html"
    Page Should Contain Element    name: div_name
    Page Should Contain Element    name: div_name    limit=None
    Page Should Contain Element    name: div_name    limit=${None}

Page Should Contain Element When Limit Is Number
    [Tags]    NoGrid
    [Documentation]    LOG 2:4    INFO Current page contains 2 element(s).
    [Setup]    Go To Page "links.html"
    Page Should Contain Element    name: div_name    limit=2

Page Should Contain Element Log Level Does Not Affect When Keyword Passes
    [Tags]    NoGrid
    [Documentation]    LOG 2:4    INFO Current page contains 2 element(s).
    [Setup]    Go To Page "links.html"
    Page Should Contain Element    name: div_name    loglevel=debug    limit=2

Page Should Contain Element When Limit Is Number And Error
    [Setup]    Go To Page "links.html"
    Run Keyword And Expect Error
    ...    Page should have contained "99" element(s), but it did contain "2" element(s).
    ...    Page Should Contain Element    name: div_name    limit=99
    Run Keyword And Expect Error
    ...    Custom error message.
    ...    Page Should Contain Element    name: div_name    message=Custom error message.    limit=${99}

Page Should Contain Element When Limit Is Not Number
    [Setup]    Go To Page "links.html"
    Run Keyword And Expect Error
    ...    ValueError: *Argument 'limit' got value 'AA'*
    ...    Page Should Contain Element    name: div_name    limit=AA

Page Should Contain Element When Error With Limit And Different Loglevels
    [Tags]    NoGrid
    [Documentation]    Only at DEBUG loglevel is the html placed in the log.
    ...    FAIL Page should have contained "99" element(s), but it did contain "2" element(s).
    ...    LOG 2.1:7    FAIL Page should have contained "99" element(s), but it did contain "2" element(s).
    ...    LOG 3:7    DEBUG REGEXP: .*links\\.html.*
    ...    LOG 3:8    FAIL Page should have contained "99" element(s), but it did contain "2" element(s).
    [Setup]    Go To Page "links.html"
    Run Keyword And Ignore Error
    ...    Page Should Contain Element    name: div_name    limit=99
    Page Should Contain Element    name: div_name    loglevel=debug    limit=99
