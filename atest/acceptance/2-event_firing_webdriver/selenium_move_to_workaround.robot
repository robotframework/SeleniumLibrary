*** Settings ***
Documentation    Can be deleted when minimum Selenium version 4.0
Library          SeleniumLibrary     event_firing_webdriver=${CURDIR}/MyListener.py
Resource         resource_event_firing_webdriver.robot
Force Tags       NoGrid
Suite Setup      Open Browser    ${FRONT PAGE}    ${BROWSER}    alias=event_firing_webdriver
...              remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}

*** Test Cases ***
Selenium move_to workaround Click Element At Coordinates
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
    Click Element At Coordinates    id:some_id    4    4

Selenium move_to workaround Scroll Element Into View
    [Documentation]    LOG 1:4 DEBUG  Workaround for Selenium 3 bug.
    Scroll Element Into View    id:some_id

Selenium move_to workaround Mouse Out
    [Documentation]    LOG 1:8 DEBUG  Workaround for Selenium 3 bug.
    Mouse Out    id:some_id

Selenium move_to workaround Mouse Over
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
    Mouse Over    id:some_id

Click Element
    [Documentation]    LOG 2 Clicking element 'singleClickButton'.
    [Setup]    Initialize Page For Click Element
    Click Element    singleClickButton
    Element Text Should Be    output    single clicked

Double Click Element
    [Documentation]    LOG 2 Double clicking element 'doubleClickButton'.
    [Setup]    Initialize Page For Click Element
    [Tags]    Known Issue Safari    Known Issue Firefox
    Double Click Element    doubleClickButton
    Element Text Should Be    output    double clicked

Click Element Action Chain
    [Tags]    NoGrid
    [Documentation]
    ...    LOB 1:1 INFO        Clicking 'singleClickButton' using an action chain.
    ...    LOG 2:5 DEBUG GLOB: *actions {"actions": [{*
    [Setup]    Initialize Page For Click Element
    Click Element    singleClickButton      action_chain=True
    Element Text Should Be    output    single clicked

Mouse Down
    [Tags]    Known Issue Safari
    [Setup]        Go To Page "mouse/index.html"
    Mouse Down    el_for_mousedown
    Textfield Value Should Be    el_for_mousedown    mousedown el_for_mousedown
    Run Keyword And Expect Error
    ...    Element with locator 'not_there' not found.
    ...    Mouse Down    not_there

Mouse Up
    [Tags]    Known Issue Safari    Known Issue Firefox
    [Setup]        Go To Page "mouse/index.html"
    Mouse Up    el_for_mouseup
    Textfield Value Should Be    el_for_mouseup    mouseup el_for_mouseup
    Run Keyword And Expect Error
    ...    Element with locator 'not_there' not found.
    ...    Mouse Up    not_there

Open Context Menu
    [Tags]    Known Issue Safari
    [Setup]    Go To Page "javascript/context_menu.html"
    Open Context Menu    myDiv

Drag and Drop
    [Tags]    Known Issue Internet Explorer    Known Issue Safari
    [Setup]    Go To Page "javascript/drag_and_drop.html"
    Element Text Should Be    id=droppable    Drop here
    Drag and Drop    id=draggable    id=droppable
    Element Text Should Be    id=droppable    Dropped!

Drag and Drop by Offset
    [Tags]    Known Issue Firefox    Known Issue Internet Explorer    Known Issue Safari
    [Setup]    Go To Page "javascript/drag_and_drop.html"
    Element Text Should Be    id=droppable    Drop here
    Drag and Drop by Offset    id=draggable    ${1}    ${1}
    Element Text Should Be    id=droppable    Drop here
    Drag and Drop by Offset    id=draggable    ${100}    ${20}
    Element Text Should Be    id=droppable    Dropped!

Mouse Down On Link
    [Tags]    Known Issue Safari
    [Setup]    Go To Page "javascript/mouse_events.html"
    Mouse Down On Image    image_mousedown
    Text Field Should Contain    textfield    onmousedown
    Mouse Up    image_mousedown
    Input text    textfield    ${EMPTY}
    Mouse Down On Link    link_mousedown
    Text Field Should Contain    textfield    onmousedown
    Mouse Up    link_mousedown

*** Keywords ***
Initialize Page For Click Element
    [Documentation]    Initialize Page
    Go To Page "javascript/click.html"
    Reload Page
    Element Text Should Be    output    initial output
