*** Setting ***
Documentation     Tests cookies
Suite Setup       Go To Page "cookies.html"
Suite Teardown    Delete All Cookies
Test Setup        Add Cookies
Resource          ../resource.robot
Library           Collections

*** Test Cases ***
Get Cookies
    [Documentation]    Get Cookies
    ${cookies}=    Get Cookies
    Should Match Regexp    ${cookies}
    ...    ^(test=seleniumlibrary; another=value)|(another=value; test=seleniumlibrary)$

Get Cookie Value Set By Selenium
    [Documentation]    Get Cookie Value Set By Selenium
    ${value}=    Get Cookie Value    another
    Should Be Equal    ${value}    value

Get Cookie Value Set By App
    [Documentation]    Get Cookie Value Set By App
    Click Link    Add cookie
    ${cookie}=    Get Cookie Value    spam
    Should Be Equal    ${cookie}    eggs

App Sees Cookie Set By Selenium
    [Documentation]    App Sees Cookie Set By Selenium
    Add Cookie    setbyselenium    true
    Click Link    Check cookie
    Element Text Should Be    output    Cookie found with value 'true'!

Delete Cookie
    [Documentation]    Delete Cookie
    [Tags]    Known Issue Safari
    Delete Cookie    test
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    another=value

Non-existent Cookie
    [Documentation]    Non-existent Cookie
    Run Keyword And Expect Error    ValueError: Cookie with name missing not found.
    ...    Get Cookie Value    missing

Get Cookies When There Are None
    [Documentation]    Get Cookies When There Are None
    [Tags]    Known Issue Safari
    Delete All Cookies
    ${cookies}=    Get Cookies
    Should Be Equal    ${cookies}    ${EMPTY}

Get Cookie Expiry Set By Selenium
    [Documentation]    Get Cookie Value Set By Selenium
    [Tags]  Known Issue Firefox
    ${cookie_dict}=    Get Cookie    another
    ${expiry} =  Convert To Integer  1822148495
    Dictionary Should Contain Value   ${cookie_dict}  ${expiry}

*** Keyword ***
Add Cookies
    [Documentation]    Add Cookies
    Delete All Cookies
    Add Cookie    test    seleniumlibrary
    Add Cookie    another    value   expiry=2027-09-28 16:21:35
