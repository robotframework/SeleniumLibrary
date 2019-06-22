*** Settings ***
Test Setup        Go To Front Page
Default Tags      assertions
Resource          ../resource.robot

*** Test Cases ***
Location Should Be
    [Tags]    NoGrid
    [Documentation]    LOG 2:4 Current location is '${FRONT PAGE}'.
    Location Should Be    ${FRONT PAGE}
    Location Should Be    ${FRONT PAGE}  message=taco
    Location Should Be    ${FRONT PAGE}  message=None
    Run Keyword And Expect Error
    ...    Location should have been 'non existing' but was '${FRONT PAGE}'.
    ...    Location Should Be    non existing
    Run Keyword And Expect Error
    ...    not a url
    ...    Location Should Be    non existing  message=not a url
    Run Keyword And Expect Error
    ...    Location should have been 'non existing' but was 'http://localhost:7000/html/'.
    ...    Location Should Be    non existing  message=None

Location Should Contain
    [Tags]    NoGrid
    [Documentation]    LOG 2:4 Current location contains 'html'.
    Location Should Contain    html
    Location Should Contain    html  message=foobar
    Location Should Contain    html  message=None
    Run Keyword And Expect Error
    ...    Location should have contained 'not a location' but it was '${FRONT PAGE}'.
    ...    Location Should Contain    not a location
    Run Keyword And Expect Error
    ...    did not find it
    ...    Location Should Contain    not a location  message=did not find it
    Run Keyword And Expect Error
    ...    Location should have contained 'not a location' but it was 'http://localhost:7000/html/'.
    ...    Location Should Contain    not a location  message=None

Wait Until Location Contains At The End
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Contains     html

Wait Until Location Contains In The Middle
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Contains     7000

Wait Until Location Contains As Number
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Contains     ${7000}

Wait Until Location Contains Fails
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    Click Element   button
    Run Keyword And Expect Error
    ...     Location did not contain 'not_here' in 2 seconds.
    ...     Wait Until Location Contains     not_here
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Contains Fails With Timeout
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Run Keyword And Expect Error
    ...     my_message
    ...     Wait Until Location Contains     not_here   timeout=0.1     message=my_message

Wait Until Location Is
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Is     http://localhost:7000/html/

Wait Until Location Is Fails
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    Click Element   button
    Run Keyword And Expect Error
    ...     Location did not is 'not_me' in 2 seconds.
    ...     Wait Until Location Is     not_me
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Is Fails With Timeout
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Run Keyword And Expect Error
    ...     my_message
    ...     Wait Until Location Is     not_here   timeout=0.1     message=my_message