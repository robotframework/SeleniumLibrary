*** Settings ***
Force Tags        Known Issue Safari
Test Setup        Go To Page "javascript/alert.html"
Resource          ../resource.robot

*** Test Cases ***
Alert Should Be Present
    Click Link    Click Me!
    Alert Should Be Present

Alert Should Be Present with message validation
    Click Link    Click Me!
    Alert Should Be Present    ALERT!
    Click Link    Click Me Too!
    Alert Should Be Present    MULTILINE ALERT!
    Click Link    Click Me!
    Run Keyword And Expect Error
    ...    Alert text should have been 'foo bar' but was 'ALERT!'
    ...    Alert Should Be Present    foo bar

Alert Should Be Present when there is none
    Run Keyword And Expect Error
    ...    There were no alerts
    ...    Alert Should Be Present

Get Alert Message
    Click Link    Click Me!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    ALERT!
    Click Link    Click Me Too!
    ${msg} =    Get Alert Message
    Should Be Equal    ${msg}    MULTILINE ALERT!
    Run Keyword And Expect Error
    ...    There were no alerts
    ...    Get Alert Message

Get Alert Message can leave alert open
    Click Link    Click Me!
    ${msg} =    Get Alert Message    ${FALSE}
    Should Be Equal    ${msg}    ALERT!
    Alert Should Be Present

Input Text Into Prompt
    [Documentation]    Always leaves the alert open
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Prompt    Robot
    Alert Should Be Present
    Page Should Contain    Hello Robot! How are you today?

Confirm Action
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${msg}=    Confirm Action
    Should Be Equal    ${msg}    Really change the title?
    Title Should Be    Original Changed!

Confirm Action multiple times
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Click Button    css=button
    Input Text Into Prompt    Robot    # Leaves the alert open
    Confirm Action
    Page Should Contain    Hello Robot! How are you today?
    Click Button    css=button
    Input Text Into Prompt    Mr. Robot
    Confirm Action
    Page Should Contain    Hello Mr. Robot! How are you today?

Cancel Action
    [Setup]    Go To Page "javascript/alert_prompt.html"
    Choose Cancel On Next Confirmation
    Click Button    css=button
    Input Text Into Prompt    Robot    # Leaves the alert open
    Confirm Action
    Page Should Not Contain    Robot

Dismiss Alert
    [Setup]    Go To Page "javascript/dynamic_content.html"
    Click Button    Change the title
    ${accepted} =    Dismiss Alert    # This actually accepts the alert
    Should Be Equal    ${accepted}    ${TRUE}
    Title Should Be    Original Changed!
    Click Button    Change the title
    ${accepted} =    Dismiss Alert    ${FALSE}    # and this dismisses....
    Title Should Be    Original Changed!
    Should Be Equal    ${accepted}    ${FALSE}
    Click Button    Change the title
    Dismiss Alert    true
    Title Should Be    Original Changed! Changed!
