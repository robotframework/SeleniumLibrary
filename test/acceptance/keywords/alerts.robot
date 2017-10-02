*** Settings ***
Force Tags        Known Issue Safari
Test Setup        Go To Page "javascript/alert.html"
Resource          ../resource.robot

*** Test Cases ***
Handle Alert accepts alert by default
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Handle Alert
    Alert Should Not Be Present
    Title Should Be    Original Changed!

Handle Alert can dismiss
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Handle Alert    action=DISMISS
    Alert Should Not Be Present
    Title Should Be    Original

Handle Alert can leave open
    Click Link    Click Me!
    Handle Alert    Leave
    Alert Should Be Present

Handler Alert with invalid action
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
    Title Should Be    Original

Alert Should Be Present
    Run Keyword And Expect Error
    ...    Expected alert not present.
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
    Title Should Be    Original Changed!
    Alert Should Not Be Present

Alert Should Be Present can dismiss
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Alert Should Be Present    Really change the title?    action=DISMISS
    Title Should Be    Original
    Alert Should Not Be Present

Alert Should Be Present can leave alert open
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    Alert Should Be Present    action=LEAVE
    Alert Should Be Present

Get Alert Message
    [Documentation]    DEPRECATED!
    Click Link    Click Me!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    ALERT!
    Click Link    Click Me Too!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    MULTILINE ALERT!
    Run Keyword And Expect Error
    ...    Expected alert not present.
    ...    Get Alert Message

Get Alet Message dismisses by default
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    Really change the title?
    Title Should Be    Original

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
    Title Should Be    Original Changed!

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
    Title Should Be    Original Changed!
    Click Button    Change the title
    ${accepted} =    Dismiss Alert    accept=${FALSE}
    Title Should Be    Original Changed!
    Should Be Equal    ${accepted}    ${FALSE}
    Click Button    Change the title
    Dismiss Alert    true
    Title Should Be    Original Changed! Changed!
