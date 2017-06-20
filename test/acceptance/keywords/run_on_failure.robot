*** Settings ***
Documentation     Tests running on failure
Suite Setup       Run Keywords    Go To Front Page    Set Info Loglevel    Prefer Custom Keywords
Test Teardown     Register Keyword to Run On Failure    Nothing
Suite Teardown    Set Debug Loglevel
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Variables ***
${PAGE TITLE}     (root)/index.html
${FAILURE MESSAGE}    Page should not have contained text 'needle'
${old order}      ${EMPTY}

*** Test Cases ***
Run On Failure Keyword Only Called Once
    [Documentation]    Run On Failure Keyword Only Called Once
    Set Test Variable    ${ON FAIL COUNT}    ${0}
    Register Keyword To Run On Failure    On Fail
    Run Keyword And Ignore Error    Custom Selenium Keyword
    Should Be Equal    ${ON FAIL COUNT}    ${1}    On Failure Keyword called ${ON FAIL COUNT} times.

Log Title On Failure
    [Documentation]    LOG 1 Log Title will be run on failure.
    ...    LOG 2:2 NONE LOG 3.1.1:1 ${PAGE TITLE} LOG 3.1:3 NONE
    Register Keyword to Run on Failure    Log Title
    Page Should Contain    needle
    Run Keyword And Expect Error    ${FAILURE MESSAGE}    Page Should Not Contain
    ...    needle    loglevel=None

Disable Run on Failure
    [Documentation]    LOG 1 No keyword will be run on failure. LOG 2.1:2 NONE
    Register Keyword to Run On Failure    Nothing
    Run Keyword And Expect Error    ${FAILURE MESSAGE}    Page Should Not Contain
    ...    needle    loglevel=None

Run on Failure Returns Previous Value
    [Documentation]    Run on Failure Returns Previous Value
    ${old}=    Register Keyword to Run on Failure    Log Title
    Should Be Equal    ${old}    No keyword
    ${old}=    Register Keyword to Run on Failure    Log Source
    Should Be Equal    ${old}    Log Title
    ${old}=    Register Keyword to Run on Failure    ${old}
    Should Be Equal    ${old}    Log Source

Run On Failure also fails
    Register Keyword to Run on Failure    Failure During Run On failure
    Run Keyword And Expect Error    ${FAILURE MESSAGE}    Page Should Not Contain
    ...    needle    loglevel=None

*** Keywords ***
On Fail
    ${count}=    Evaluate    ${ON FAIL COUNT} + 1
    Set Test Variable    ${ON FAIL COUNT}    ${count}

Prefer Custom Keywords
    Import Library    CustomSeleniumKeywords
    Set Library Search Order    CustomSeleniumKeywords

Open Browser To Front Page
    Open Browser    ${FRONT PAGE}

Failure During Run On failure
    Page Should Not Contain    needle
