*** Setting ***
<<<<<<< HEAD
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
=======
Suite Setup       Go To Page "cookies.html"
Suite Teardown    Delete All Cookies
Test Setup        Add Cookies
Resource          ../resource.txt

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
>>>>>>> ac83046a85a8b5d4163e6b6fc15c61eaebb34282

*** Keyword ***
Add Cookies
    Delete All Cookies
    Add Cookie    test    seleniumlibrary
    Add Cookie    another    value
