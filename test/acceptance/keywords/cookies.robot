*** Setting ***
Suite Setup       Run Keywords    Add Cookies    Go To Page "index.html"
Suite Teardown    Delete All Cookies
Force Tags        cookies
Resource          ../resource.robot

*** Test Cases ***
Get Cookies
    ${cookies} =    Get Cookies
    #Should Be Equal    ${cookies}    test=seleniumlibrary; another=value    # in IE order is reversed
    Should Contain    ${cookies}    test=seleniumlibrary
    Should Contain    ${cookies}    another=value

Get Cookie Value
    ${value} =    Get Cookie Value    another
    Should Be Equal    ${value}    value

Delete Cookie
    Delete Cookie    test
    ${cookies} =    Get Cookies
    #Should Be Equal    ${cookies}    another=value    #Chrome created cookies twice
    Should Not Contain    ${cookies}    test=seleniumlibrary

*** Keyword ***
Add Cookies
    Delete All Cookies
    Add Cookie    test    seleniumlibrary
    Add Cookie    another    value
