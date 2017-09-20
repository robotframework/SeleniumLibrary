*** Settings ***
Suite Setup       Go To Page "forms/prefilled_email_form.html"
Suite Teardown    Set Selenium Speed    0
Resource          ../resource.robot

*** Test Cases ***
Settimg selenium speed is possible multiple times
    Set Selenium Speed    10
    ${speed} =    Set Selenium Speed    5
    Should Be Equal     ${speed}    ${10}
    ${speed} =    Set Selenium Speed    1
    Should Be Equal     ${speed}    ${5}

Selenium speed should affect execution
    [Documentation]    Click Element executes two selenium commands and
    ...    therefore total time is 2 seconds
    Set Selenium Speed    1
    ${start} =    Get Time    epoch
    Click Element    xpath=//input[@name="email"]
    ${end} =    Get Time    epoch
    Should Be True     ${end} - ${start} >= ${2}

Selenium speed should affect before browser is opened
    [Documentation]    Click Element executes two selenium commands and
    ...    therefore total time is 2 seconds
    Close All Browsers
    Set Selenium Speed    1
    Open Browser To "forms/prefilled_email_form.html"
    ${start} =    Get Time    epoch
    Click Element    xpath=//input[@name="email"]
    ${end} =    Get Time    epoch
    Should Be True     ${end} - ${start} >= ${2}

Selenium speed should affect all browsers
    [Documentation]    Click Element executes two selenium commands and
    ...    therefore total time is 2 seconds
    Close All Browsers
    Open Browser To "forms/prefilled_email_form.html"
    Open Browser To "forms/prefilled_email_form.html"
    Set Selenium Speed    1
    ${start} =    Get Time    epoch
    Click Element    xpath=//input[@name="email"]
    ${end} =    Get Time    epoch
    Should Be True     ${end} - ${start} >= ${2}
    Switch Browser    ${2}
    ${start} =    Get Time    epoch
    Click Element    xpath=//input[@name="email"]
    ${end} =    Get Time    epoch
    Should Be True     ${end} - ${start} >= ${2}

*** Keywords ***
Open Browser To "forms/prefilled_email_form.html"
    ${index} =    Open Browser    ${FRONT PAGE}    ${BROWSER}
    ...    remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
    Go To    ${ROOT}/forms/prefilled_email_form.html
