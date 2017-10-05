*** Setting ***
Documentation     Tests cookies
Suite Setup       Go To Page "cookies.html"
Suite Teardown    Delete All Cookies
Test Setup        Add Cookies
Resource          ../resource.robot


*** Test Cases ***
Get Cookies
    ${cookies}=    Get Cookies
    Should Match Regexp    ${cookies}
    ...    ^(test=seleniumlibrary; another=value)|(another=value; test=seleniumlibrary)$

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
    [Tags]    Known Issue Safari
    Delete Cookie    test
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    another=value

Non-existent Cookie
    Run Keyword And Expect Error    ValueError: Cookie with name missing not found.
    ...    Get Cookie Value    missing

Get Cookies When There Are None
    [Tags]    Known Issue Safari
    Delete All Cookies
    ${cookies}=    Get Cookies
    Should Be Equal    ${cookies}    ${EMPTY}

Get Cookie Expiry Set By Selenium
    [Tags]  Known Issue Firefox
    ${cookie} =    Get Cookie    another
    ${date} =  Convert Date  2027-09-28 16:21:35  epoch
    Should Be Equal As Integers   ${cookie.expiry}  ${date}
    [Teardown]    Delete All Cookies

Test Get Cookie Object Expiry
    ${cookie} =    Get Cookie    another
    ${date} =    Convert Date  2027-09-28 16:21:35  epoch
    Should Be Equal As Integers    ${cookie.expiry}       ${date}

Test Get Cookie Object Domain
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.domain}       localhost

Test Get Cookie Object HttpOnly
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.httpOnly}     ${False}

Test Get Cookie Object Name
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.name}         another

Test Get Cookie Object Path
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.path}         /

Test Get Cookie Object Secure
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.secure}       ${False}

Test Get Cookie Object Value
    ${cookie} =    Get Cookie    another
    Should Be Equal    ${cookie.value}        value

Test Get Cookie Object Full_info
    ${cookie} =    Get Cookie    another
    ${date} =    Convert Date  2027-09-28 16:21:35  epoch
    ${date} =    Convert To Integer    ${date}
    Should Contain     ${cookie.full_info}    domain=localhost
    Should Contain     ${cookie.full_info}    secure=False
    Should Contain     ${cookie.full_info}    value=value
    Should Contain     ${cookie.full_info}    expiry=${date}
    Should Contain     ${cookie.full_info}    path=/
    Should Contain     ${cookie.full_info}    httpOnly=False
    Should Contain     ${cookie.full_info}    name=another

*** Keyword ***
Add Cookies
    Delete All Cookies
    Add Cookie    test    seleniumlibrary
    Add Cookie    another    value   expiry=2027-09-28 16:21:35
