*** Settings ***
Force Tags        Known Issue Safari
Suite Setup       Set Global Timeout    1 second
Test Setup        Go To Page "javascript/alert.html"
Suite Teardown    Restore Global Timeout
Resource          ../resource.robot

*** Test Cases ***
Handle Alert accepts by default
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Handle Alert
    Alert Should Not Be Present
    Wait For Title Change    Original Changed!

Handle Alert can dismiss
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Handle Alert    action=DISMISS
    Alert Should Not Be Present
    Wait For Title Change    Original

Handle Alert can leave open
    Click Link    Click Me!
    Handle Alert    Leave
    Alert Should Be Present

Handle Alert with invalid action
    Click Link    Click Me!
    Run Keyword And Expect Error
    ...    ValueError: Invalid alert action 'INVALID'.
    ...    Handle Alert    INVALID
    Alert Should Be Present

Handle Alert returns message
    Click Link    Click Me!
    ${message} =    Handle Alert
    Should Be Equal    ${message}    ALERT!
    Click Link    Click Me Too!
    ${message} =    Handle Alert    action=LEAVE
    Should Be Equal    ${message}    MULTILINE ALERT!
    Alert Should Be Present

Handle Alert with custom timeout
    Click Button    Slow alert
    Handle Alert    timeout=1s
    Click Button    Slow alert
    Run Keyword And Expect Error
    ...    Alert not found in 1 millisecond.
    ...    Handle Alert    ACCEPT    1 ms
    Handle Alert    timeout=3.14 seconds

Alert Should Not Be Present
    Alert Should Not Be Present
    Click Link    Click Me!
    Run Keyword And Expect Error
    ...    Alert with message 'ALERT!' present.
    ...    Alert Should Not Be Present

Alert Should Not Be Present with custom actions
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Run Keyword And Expect Error
    ...    Alert with message 'Really change the title?' present.
    ...    Alert Should Not Be Present    action=LEAVE
    Run Keyword And Expect Error
    ...    Alert with message 'Really change the title?' present.
    ...    Alert Should Not Be Present    action=DISmiss
    Wait For Title Change    Original

Alert Should Not Be Present with custom timeout
    Alert Should Not Be Present    timeout=0.1s
    Click Button    Slow alert
    Alert Should Not Be Present    DISMISS    ${0.001}
    Run Keyword And Expect Error
    ...    Alert with message 'Alert after 500ms!' present.
    ...    Alert Should Not Be Present    timeout=0.99999

Alert Should Be Present
    Run Keyword And Expect Error
    ...    Alert not found in 1 second.
    ...    Alert Should Be Present
    Click Link    Click Me!
    Alert Should Be Present

Alert Should Be Present with message validation
    Click Link    Click Me!
    Alert Should Be Present    ALERT!
    Click Link    Click Me Too!
    Alert Should Be Present    MULTILINE ALERT!
    Click Link    Click Me!
    Run Keyword And Expect Error
    ...    Alert message should have been 'foo bar' but it was 'ALERT!'.
    ...    Alert Should Be Present    foo bar

Alert Should Be Present accepts by default
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Alert Should Be Present    Really change the title?
    Wait For Title Change    Original Changed!
    Alert Should Not Be Present

Alert Should Be Present can dismiss
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Alert Should Be Present    Really change the title?    action=DISMISS
    Wait For Title Change    Original
    Alert Should Not Be Present

Alert Should Be Present can leave alert open
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Alert Should Be Present    action=LEAVE
    Alert Should Be Present

Alert Should Be Present with custom timeout
    Click Button    Slow alert
    Run Keyword And Expect Error
    ...    Alert not found in 1 millisecond.
    ...    Alert Should Be Present    timeout=1ms
    Alert Should Be Present    Alert after 500ms!    ACCEPT    3s

Get Alert Message
    [Documentation]    DEPRECATED!
    Click Link    Click Me!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    ALERT!
    Click Link    Click Me Too!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    MULTILINE ALERT!
    Run Keyword And Expect Error
    ...    Alert not found in 1 second.
    ...    Get Alert Message

Get Alet Message dismisses by default
    [Documentation]    DEPRECATED!
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    Really change the title?
    Wait For Title Change    Original

Get Alert Message can leave alert open
    [Documentation]    DEPRECATED!
    Click Link    Click Me!
    ${msg} =    Get Alert Message    ${FALSE}
    Should Be Equal    ${msg}    ALERT!
    Alert Should Be Present

Input Text Into Alert
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Alert    Robot
    Alert Should Not Be Present
    Page Should Contain    Hello Robot! How are you today?

Input Text Into Alert can leave alert open
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Alert    Robot    action=LEAVE
    Alert Should Be Present
    Page Should Contain    Hello Robot! How are you today?

Input Text Into Alert can dismiss
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Alert    Robot    action=DISMISS
    Alert Should Not Be Present
    Page Should Not Contain    Robot

Input Text Into Alert with custom timeout
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Run Keyword And Expect Error
    ...    Alert not found in 7 milliseconds.
    ...    Input Text Into Alert    This is not found    timeout=007ms

Input Text Into Prompt
    [Documentation]    DEPRECATED! Always leaves the alert open.
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Prompt    Robot
    Alert Should Be Present
    Page Should Contain    Hello Robot! How are you today?

Confirm Action
    [Documentation]    DEPRECATED!
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${msg}=    Confirm Action
    Should Be Equal    ${msg}    Really change the title?
    Wait For Title Change    Original Changed!

Confirm Action multiple times
    [Documentation]    DEPRECATED!
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Alert    Robot    action=LEAVE
    Confirm Action
    Page Should Contain    Hello Robot! How are you today?
    Click Button    css=button
    Input Text Into Alert    Mr. Roboto    action=LEAVE
    Confirm Action
    Page Should Contain    Hello Mr. Roboto! How are you today?

Cancel Action
    [Documentation]    DEPRECATED!
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Choose Cancel On Next Confirmation
    Click Button    css=button
    Input Text Into Alert    Robot    action=LEAVE
    Confirm Action
    Page Should Not Contain    Robot

Dismiss Alert
    [Documentation]    DEPRECATED!
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${accepted} =    Dismiss Alert    # This actually accepts the alert
    Should Be Equal    ${accepted}    ${TRUE}
    Wait For Title Change    Original Changed!
    Click Button    Change the title
    ${accepted} =    Dismiss Alert    accept=${FALSE}
    Wait For Title Change    Original Changed!
    Should Be Equal    ${accepted}    ${FALSE}
    Click Button    Change the title
    Dismiss Alert    true
    Wait For Title Change    Original Changed! Changed!

*** Keywords ***
Wait For Title Change
    [Arguments]    ${expected}
    Wait For Condition    return document.title == '${expected}'
