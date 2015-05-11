*** Setting ***
Suite Setup       Go To Page "cookies.html"
Suite Teardown    Delete All Cookies
Test Setup        Add Cookies
Resource          ../resource.robot

*** Test Cases ***
Get Cookies
    ${cookies}=    Get Cookies
    Should Match Regexp    ${cookies}    ^(test=seleniumlibrary; another=value)|(another=value; test=seleniumlibrary)$

Get Cookie Value Set By Selenium
    ${value}=    Get Cookie Value    another
    Should Be Equal    ${value}    value

Get Cookie Value Set By App
    Click Link    Add cookie
    ${cookie}=    Get Cookie Value    spam
    Should Be Equal    ${cookie}    eggs

App Sees Cookie Set By Selenium
    Add Cookie    setbyselenium    true
    Click Link    Check cookie
    Element Text Should Be    output    Cookie found with value 'true'!

Delete Cookie
    Delete Cookie    test
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    another=value

Non-existent Cookie
    Run Keyword And Expect Error    ValueError: Cookie with name missing not found.    Get Cookie Value    missing

Get Cookies When There Are None
    Delete All Cookies
    ${cookies}=    Get Cookies
    Should Be Equal    ${cookies}    ${EMPTY}

*** Keyword ***
Add Cookies
    Delete All Cookies
    Add Cookie    test    seleniumlibrary
    Add Cookie    another    value
