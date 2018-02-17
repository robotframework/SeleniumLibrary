*** Settings ***
Test Setup        Go To Page "javascript/dynamic_content.html"
Resource          ../resource.robot

*** Test Cases ***
Clicking Elements Should Activate Javascript
    Title Should Be    Original
    Click Element    link=change title
    Title Should Be    Changed

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

Execute Javascript
    [Documentation]    LOG 2 Executing JavaScript:
    ...    window.add_content('button_target', 'Inserted directly')
    Execute Javascript    window.add_content('button_target', 'Inserted directly')
    Page Should Contain    Inserted directly

Execute Javascript from File
    [Documentation]    LOG 2:1 REGEXP: Reading JavaScript from file .*
    ...    LOG 2:2 Executing JavaScript:
    ...    window.add_content('button_target', 'Inserted via file')
    Execute Javascript    ${CURDIR}/executed_by_execute_javascript.js
    Page Should Contain    Inserted via file

Open Context Menu
    [Tags]    Known Issue Safari
    Go To Page "javascript/context_menu.html"
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
