*** Settings ***
Resource          ../resource.robot

*** Test Cases ***
Wait Until Element Is Visible
    [Tags]     Known Issue Internet Explorer
    [Setup]    Go To Page "javascript/delayed_events.html"
    Run Keyword And Expect Error
    ...    Element 'hidden' not visible after 10 milliseconds.
    ...    Wait Until Element Is Visible    hidden    0.01
    Run Keyword And Expect Error
    ...    User error message
    ...    Wait Until Element Is Visible    hidden    0.01    User error message
    Wait Until Element Is Visible    hidden    2 s
    Run Keyword And Expect Error
    ...    Element 'invalid' not visible after 100 milliseconds.
    ...    Wait Until Element Is Visible    invalid    0.1

Wait Until Element Is Visible with locator and error arguments
    [Tags]     Known Issue Internet Explorer
    [Setup]    Go To Page "javascript/delayed_events.html"
    Wait Until Element Is Visible    hidden    error=My error message

Wait Until Element Is Visible with locator only
    [Tags]     Known Issue Internet Explorer
    [Setup]    Go To Page "javascript/delayed_events.html"
    Wait Until Element Is Visible    hidden

Wait Until Element Is Not Visible
    [Setup]    Go To Page "javascript/delayed_events.html"
    Wait Until Element Is Not Visible    id:hide_delay
    Wait Until Element Is Not Visible    id:not_present    timeout=3

Element Should Be Visible
    [Setup]    Go To Page "visibility.html"
    Element Should Be Visible    i_am_visible
    Run Keyword And Expect Error
    ...    The element 'i_am_hidden' should be visible, but it is not.
    ...    Element Should Be Visible    i_am_hidden

Element Should Not Be Visible
    [Setup]    Go To Page "visibility.html"
    Element Should Not Be Visible    i_am_hidden
    Element Should Not Be Visible    not_here
    Run Keyword And Expect Error
    ...    The element 'i_am_visible' should not be visible, but it is.
    ...    Element Should Not Be Visible    i_am_visible

