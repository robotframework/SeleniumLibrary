*** Settings ***
Documentation     Tests mouse
Test Setup        Go To Page "mouse/index.html"
Resource          ../resource.robot
Force Tags        Known Issue Internet Explorer

*** Test Cases ***
Mouse Over
    [Documentation]    Mouse Over
    [Tags]    Known Issue Safari    Known Issue Firefox
    Mouse Over    el_for_mouseover
    Textfield Value Should Be    el_for_mouseover    mouseover el_for_mouseover
    Run Keyword And Expect Error    ERROR: Element not_there not found.    Mouse Over    not_there

Mouse Out
    [Documentation]    Mouse Out
    [Tags]    Known Issue Safari    Known Issue Firefox
    Mouse Out    el_for_mouseout
    Textfield Value Should Be    el_for_mouseout    mouseout el_for_mouseout
    Run Keyword And Expect Error    ERROR: Element not_there not found.    Mouse Out    not_there

Mouse Down
    [Documentation]    Mouse Down
    [Tags]    Known Issue Safari    Known Issue Firefox
    Mouse Down    el_for_mousedown
    Textfield Value Should Be    el_for_mousedown    mousedown el_for_mousedown
    Run Keyword And Expect Error    ERROR: Element not_there not found.    Mouse Down    not_there

Mouse Up
    [Documentation]    Mouse Up
    [Tags]    Known Issue Safari    Known Issue Firefox
    Mouse Up    el_for_mouseup
    Textfield Value Should Be    el_for_mouseup    mouseup el_for_mouseup
    Run Keyword And Expect Error    ERROR: Element not_there not found.    Mouse Up    not_there

Focus
    [Documentation]    Focus
    Focus    el_for_focus
    Textfield Value Should Be    el_for_focus    focus el_for_focus

Simulate
    [Documentation]    Simulate
    Simulate    el_for_blur    blur
    Textfield Value Should Be    el_for_blur    blur el_for_blur
