*** Settings ***
Documentation     Tests Focus Verification and Wait for Focus
Suite Setup       Open Browser To Start Page
Resource          ../resource.robot

*** Test Cases ***
Should Be Focused
    [Setup]    Go To Page "mouse/index.html"
    Click Element    el_for_focus
    Element Should Be Focused    el_for_focus

Should Not Be Focused
    [Setup]    Go To Page "mouse/index.html"
    Click Element    el_for_focus
    Run Keyword And Expect Error
    ...    Element 'el_for_blur' does not have focus.
    ...    Element Should Be Focused    el_for_blur
    Element Should Be Focused    el_for_focus

Unexistent Element Not Focused
    [Setup]    Go To Page "mouse/index.html"
    Click Element    el_for_focus
    Run Keyword And Expect Error
    ...    Element with locator 'Unexistent_element' not found.
    ...    Element Should Be Focused    Unexistent_element

Span Element Not Focused
    [Documentation]    Focus on not Focusable Span
    [Setup]    Go To Page "/"
    Click Element    some_id
    Run Keyword And Expect Error
    ...    Element 'some_id' does not have focus.
    ...    Element Should Be Focused    some_id

Table Element Not Focused
    [Documentation]    Focus on not Focusable Table
    [Setup]    Go To Page "tables/tables.html"
    Click Element    simpleTable
    Run Keyword And Expect Error
    ...    Element 'simpleTable' does not have focus.
    ...    Element Should Be Focused    simpleTable

Radio Button Should Be Focused
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    Click Element    xpath=//input[@name='sex' and @value='male']
    Element Should Be Focused    xpath=//input[@name='sex' and @value='male']
    Run Keyword And Expect Error
    ...    Element 'xpath=//input[@name=\'sex\' and @value=\'female\']' does not have focus.
    ...    Element Should Be Focused    xpath=//input[@name='sex' and @value='female']

Checkbox Should Be Focused
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    Click Element    xpath=//input[@name='can_send_sms']
    Element Should Be Focused    xpath=//input[@name='can_send_sms']
    Run Keyword And Expect Error
    ...    Element 'xpath=//input[@name=\'can_send_email\']' does not have focus.
    ...    Element Should Be Focused    xpath=//input[@name='can_send_email']

Select Button Should Be Focused
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    Mouse Down    xpath=//select[@name='preferred_channel']
    Element Should Be Focused    xpath=//select[@name='preferred_channel']
    Run Keyword And Expect Error
    ...    Element 'xpath=//select[@name=\'preferred_channel\']/option[@value=\'phone\']' does not have focus.
    ...    Element Should Be Focused    xpath=//select[@name='preferred_channel']/option[@value='phone']
    Click Element    xpath=//option[@value='email']
    Run Keyword And Expect Error
    ...    Element 'xpath=//option[@value=\'email\']' does not have focus.
    ...    Element Should Be Focused    xpath=//option[@value='email']

Submit Button Should Be Focused
    [Setup]    Go To Page "forms/prefilled_email_form.html"
    Mouse Up    preferred_channel
    Mouse Down    submit
    Sleep    1 second
    Element Should Be Focused    submit
    Mouse Up    submit

Set Focus To Element
    [Setup]    Go To Page "mouse/index.html"
    Set Focus To Element    el_for_focus
    Textfield Value Should Be    el_for_focus    focus el_for_focus
    Element Should Be Focused    el_for_focus

Focus is deprecated
    [Documentation]    "Focus" is deprecated in favor of "Set Focus To Element"
    [Setup]    Go To Page "mouse/index.html"
    Focus    el_for_focus
    Textfield Value Should Be    el_for_focus    focus el_for_focus
    Element Should Be Focused    el_for_focus
