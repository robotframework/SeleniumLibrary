*** Setting ***
Library           Selenium2Library    run_on_failure=Nothing    implicit_wait=0
Library           Collections
Library           OperatingSystem

*** Variable ***
${SERVER}=         localhost:7000
${BROWSER}=        firefox
${REMOTE_URL}=     ${NONE}
${DESIRED_CAPABILITIES}=    ${NONE}
${ROOT}=           http://${SERVER}/html
${FRONT_PAGE}=     ${ROOT}/
${SPEED}=          0

*** Keyword ***
Open Browser To Start Page
    [Documentation]    This keyword also tests 'Set Selenium Speed' and 'Set Selenium Timeout'
    ...    against all reason.
    ${default speed}    ${default timeout}=    Open Browser To Start Page Without Testing Default Options
    Should Be Equal    ${default speed}    0 seconds
    Should Be Equal    ${default timeout}    5 seconds

Open Browser To Start Page Without Testing Default Options
    [Documentation]    Open Browser To Start Page Without Testing Default Options
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}
    ${orig speed} =    Set Selenium Speed    ${SPEED}
    ${orig timeout} =    Set Selenium Timeout    10 seconds
    [Return]    ${orig speed}    5 seconds

Open Browser To Start Page And Test Implicit Wait
    [Arguments]    ${implicit_wait}
    [Documentation]    This keyword tests that 'Set Selenium Implicit Wait' and
    ...    'Get Selenium Implicit Wait' work as expected
    Should Not Be Equal    0    ${implicit_wait}
    ...    Please do not pass in a value of 0 for the implicit wait argument for this function
    ${old_wait}=    Set Selenium Implicit Wait    ${implicit_wait}
    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}
    ${default_implicit_wait} =    Get Selenium Implicit Wait
    Should Be Equal    ${implicit_wait} seconds    ${default_implicit_wait}
    #be sure to revert the implicit wait to whatever it was before so as to not effect other tests
    Set Selenium Implicit Wait    ${old_wait}

Cannot Be Executed In IE
    [Documentation]    Cannot Be Executed In IE
    ${runsInIE}=    Set Variable If    "${BROWSER}".replace(' ', '').lower() in ['ie', '*iexplore', 'internetexplorer']    ${TRUE}
    Run Keyword If    ${runsInIE}    Set Tags    ie-incompatible
    Run Keyword If    ${runsInIE}    Fail And Set Non-Critical
    ...    This test does not work in Internet Explorer

Fail And Set Non-Critical
    [Arguments]    ${msg}
    [Documentation]    Fails And Set Non-Critical
    Remove Tags    regression
    Fail    ${msg}

Go to Front Page
    [Documentation]    Goes to front page
    Go To    ${FRONT PAGE}

Go To Page "${relative url}"
    [Documentation]    Goes to page
    Go To    ${ROOT}/${relative url}

Set ${level} Loglevel
    [Documentation]    Sets loglevel
    Set Log Level    ${level}

Verify Location Is "${relative url}"
    [Documentation]    Verifies location
    Location Should Be    ${ROOT}/${relative url}
