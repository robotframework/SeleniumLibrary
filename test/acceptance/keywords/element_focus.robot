*** Settings ***
Documentation     Tests Focus Verification and Wait for Focus
Suite Setup       Open Browser To Start Page
Test Setup        Go To Page "mouse/index.html"
# Suite Teardown    Close All Browsers
Resource          ../resource.robot

*** Test Cases ***
Should Be Focused
    [Documentation]    Verify that element is Focused
    Click Element    el_for_focus
    Element Should Be Focused    el_for_focus

Should Not Be Focused
    [Documentation]    Verify that element is not Focused
    Click Element    el_for_focus
    Run Keyword And Expect Error    ERROR: Element 'el_for_blur' is not with focus.    Element Should Be Focused    el_for_blur

Unexistent Element Not Focused
    [Documentation]    Missing element returns locator error
    Click Element    el_for_focus
    Run Keyword And Expect Error    ValueError: Element locator 'Unexistent_element' did not match any elements.    Element Should Be Focused    Unexistent_element

Span Element Not Focused
    [Documentation]    Focus on not Focusable Span
    Go To Page "/"
    Click Element    some_id
    Run Keyword And Expect Error    ERROR: Element 'some_id' is not with focus.    Element Should Be Focused    some_id

Table Element Not Focused
    [Documentation]    Focus on not Focusable Table
    Go To Page "tables/tables.html"
    Click Element    simpleTable
    Run Keyword And Expect Error    ERROR: Element 'simpleTable' is not with focus.    Element Should Be Focused    simpleTable

