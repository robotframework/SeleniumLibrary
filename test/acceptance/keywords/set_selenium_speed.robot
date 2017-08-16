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
    ...    therefore total time is 6 seconds
    Set Selenium Speed    3
    ${start} =    Get Time    epoch
    Click Element    xpath=//input[@name="email"]
    ${end} =    Get Time    epoch
    ${total} =    Evaluate    ${end} - ${start}
    Should Be True     ${total} > ${5}
