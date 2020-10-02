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
    ...    None
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
    ...    None
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
    ...     Location did not become 'not_me' in 2 seconds.
    ...     Wait Until Location Is     not_me
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Is Fails With Timeout
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Run Keyword And Expect Error
    ...     my_message
    ...     Wait Until Location Is     not_here   timeout=0.1     message=my_message

Wait Until Location Is Not
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Is Not     http://localhost:7000/html/javascript/wait_location.html

Wait Until Location Is Not Fail
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    Run Keyword And Expect Error
    ...     Location is 'http://localhost:7000/html/javascript/wait_location.html' in 2 seconds.
    ...     Wait Until Location Is Not  http://localhost:7000/html/javascript/wait_location.html
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Is Not Fails With Timeout
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    Click Element   button
    Run Keyword And Expect Error
    ...     Location is 'http://localhost:7000/html/javascript/wait_location.html' in 1 second.
    ...     Wait Until Location Is Not     http://localhost:7000/html/javascript/wait_location.html   timeout=1 s
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Is Not Fails With Message
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    Run Keyword And Expect Error
    ...     my_message
    ...     Wait Until Location Is Not     http://localhost:7000/html/javascript/wait_location.html  message=my_message
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Does Not Contain
    [Setup]    Go To Page "javascript/wait_location.html"
    Click Element   button
    Wait Until Location Does Not Contain     wait_location

Wait Until Location Does Not Contain Fail
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    run keyword and expect error
    ...    Location did contain 'wait_location.html' in 2 seconds.
    ...    Wait Until Location Does Not Contain      wait_location.html
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Does Not Contain Fail In The Middle
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    run keyword and expect error
    ...    Location did contain 'javascript' in 2 seconds.
    ...    Wait Until Location Does Not Contain      javascript
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Does Not Contain Fail As Number
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    run keyword and expect error
    ...    Location did contain '${7000}' in 2 seconds.
    ...    Wait Until Location Does Not Contain   ${7000}
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Does Not Contain Fail At The End
    [Setup]    Go To Page "javascript/wait_location.html"
    ${orig_timeout}=    Set Selenium Timeout    2 s
    run keyword and expect error
    ...    Location did contain '.html' in 2 seconds.
    ...    Wait Until Location Does Not Contain    .html
    Set Selenium Timeout    ${orig_timeout}

Wait Until Location Does Not Contain Fail With Timeout
    [Setup]    Go To Page "javascript/wait_location.html"
    run keyword and expect error
    ...    Location did contain 'wait_location.html' in 1 second.
    ...    Wait Until Location Does Not Contain      wait_location.html   timeout= 1 s

Wait Until Location Does Not Contain Fail With Message
    [Setup]    Go To Page "javascript/wait_location.html"
    run keyword and expect error
    ...    my_message
    ...    Wait Until Location Does Not Contain      wait_location.html  message=my_message