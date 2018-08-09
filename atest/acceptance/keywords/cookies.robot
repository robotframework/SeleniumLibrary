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
    ${value} =    Get Cookie Value    another
    Should Be Equal    ${value}       value

Get Cookie Value Set By App
    Click Link    Add cookie
    ${cookie}=    Get Cookie Value    spam
    Should Be Equal    ${cookie}      eggs

App Sees Cookie Set By Selenium
    Add Cookie    setbyselenium    true
    Click Link    Check cookie
    Element Text Should Be    output    Cookie found with value 'true'!

Add Cookie When Secure Is Default
    [Documentation]    Setting secure to True is tested in unit tests
    ...   because chrome raises WebDriverException when http is used with
    ...   secure. Currently our test server supports only http
    Add Cookie    Cookie1    value1
    ${cookie} =    Get Cookie    Cookie1
    Should Be Equal    ${cookie.secure}       ${False}

Add Cookie When Secure Is False
    Add Cookie    Cookie1    value1    secure=False
    ${cookie} =    Get Cookie    Cookie1
    Should Be Equal    ${cookie.secure}       ${False}

Add Cookie When Expiry Is Epoch
    Add Cookie    Cookie1    value1    expiry=1822137695
    ${cookie} =    Get Cookie    Cookie1
    ${expiry} =    Convert Date    ${1822137695}    exclude_millis=True
    Should Be Equal As Strings    ${cookie.expiry}    ${expiry}

Add Cookie When Expiry Is Human Readable Data&Time
    Add Cookie    Cookie12    value12    expiry=2027-09-28 16:21:35
    ${cookie} =    Get Cookie    Cookie12
    Should Be Equal As Strings    ${cookie.expiry}    2027-09-28 16:21:35

Delete Cookie
    [Tags]    Known Issue Safari
    Delete Cookie    test
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    another=value

Non-existent Cookie
    Run Keyword And Expect Error
    ...    Cookie with name 'missing' not found.
    ...    Get Cookie    missing

Get Cookies When There Are None
    [Tags]    Known Issue Safari
    Delete All Cookies
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    ${EMPTY}

Test Get Cookie Object Expiry
    ${cookie} =    Get Cookie      another
    Should Be Equal As Integers    ${cookie.expiry.year}           2027
    Should Be Equal As Integers    ${cookie.expiry.month}          09
    Should Be Equal As Integers    ${cookie.expiry.day}            28
    Should Be Equal As Integers    ${cookie.expiry.hour}           16
    Should Be Equal As Integers    ${cookie.expiry.minute}         21
    Should Be Equal As Integers    ${cookie.expiry.second}         35
    Should Be Equal As Integers    ${cookie.expiry.microsecond}    0

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

Test Get Cookie Keyword Logging
    [Documentation]
    ...    LOG 2:4 ${cookie} = name=another
    ...    value=value
    ...    path=/
    ...    domain=localhost
    ...    secure=False
    ...    httpOnly=False
    ...    expiry=2027-09-28 16:21:35
    ${cookie} =    Get Cookie     another

*** Keyword ***
Add Cookies
    Delete All Cookies
    Add Cookie    test       seleniumlibrary
    Add Cookie    another    value   expiry=2027-09-28 16:21:35
