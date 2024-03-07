*** Settings ***
Documentation     Tests cookies
Suite Setup       Go To Page "cookies.html"
Suite Teardown    Delete All Cookies
Test Setup        Add Cookies
Resource          ../resource.robot
Library           DateTime

*** Test Cases ***
Get Cookies
    ${cookies}=    Get Cookies
    Should Match Regexp    ${cookies}
    ...    ^(test=seleniumlibrary; another=value)|(another=value; test=seleniumlibrary)$

Get Cookies As Dict
    ${cookies}=    Get Cookies        as_dict=True
    ${expected_cookies}=    Create Dictionary   test=seleniumlibrary    another=value    far_future=timemachine
    Dictionaries Should Be Equal  ${expected_cookies}   ${cookies}

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
    Add Cookie    Cookie1    value1    expiry=1730205247
    ${cookie} =    Get Cookie    Cookie1
    ${expiry} =    Convert Date    ${1730205247}    exclude_millis=True
    Should Be Equal As Strings    ${cookie.expiry}    ${expiry}

Add Cookie When Expiry Is Human Readable Data&Time
    Add Cookie    Cookie12    value12    expiry=2024-10-29 19:36:51
    ${cookie} =    Get Cookie    Cookie12
    Should Be Equal As Strings    ${cookie.expiry}    2024-10-29 19:36:51

Delete Cookie
    [Tags]    Known Issue Safari
    Delete Cookie    test
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    far_future=timemachine; another=value

Non-existent Cookie
    Run Keyword And Expect Error
    ...    Cookie with name 'missing' not found.
    ...    Get Cookie    missing

Get Cookies When There Are None
    [Tags]    Known Issue Safari
    Delete All Cookies
    ${cookies} =    Get Cookies
    Should Be Equal    ${cookies}    ${EMPTY}

Get Cookies As Dict When There Are None
    [Tags]    Known Issue Safari
    Delete All Cookies
    ${cookies} =    Get Cookies   as_dict=True
    ${expected_cookies}=    Create Dictionary
    Dictionaries Should Be Equal  ${expected_cookies}   ${cookies}

Test Get Cookie Object Expiry
    ${cookie} =    Get Cookie      another
    Should Be Equal As Integers    ${cookie.expiry.year}           ${tomorrow_thistime_datetime.year}
    Should Be Equal As Integers    ${cookie.expiry.month}          ${tomorrow_thistime_datetime.month}
    Should Be Equal As Integers    ${cookie.expiry.day}            ${tomorrow_thistime_datetime.day}
    Should Be Equal As Integers    ${cookie.expiry.hour}           ${tomorrow_thistime_datetime.hour}
    Should Be Equal As Integers    ${cookie.expiry.minute}         ${tomorrow_thistime_datetime.minute}
    Should Be Equal As Integers    ${cookie.expiry.second}         ${tomorrow_thistime_datetime.second}
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
    [Tags]    NoGrid    Known Issue Firefox
    [Documentation]
    ...    LOG 1:5 GLOB: ${cookie} = name=far_future
    ...    value=timemachine
    ...    path=/
    ...    domain=localhost
    ...    secure=False
    ...    httpOnly=False
    ...    expiry=2024-09-15 *:22:33
    ...    extra={'sameSite': 'Lax'}
    ${cookie} =    Get Cookie     far_future

*** Keywords ***
Add Cookies
    Delete All Cookies
    Add Cookie    test       seleniumlibrary
    ${now} =    Get Current Date
    ${tomorrow_thistime} =    Add Time To Date    ${now}    1 day
    ${tomorrow_thistime_datetime} =    Convert Date    ${tomorrow_thistime}    datetime
    Set Suite Variable    ${tomorrow_thistime_datetime}
    Add Cookie    another    value   expiry=${tomorrow_thistime}
    Add Cookie    far_future    timemachine    expiry=1726399353    # 2024-09-15 11:22:33
