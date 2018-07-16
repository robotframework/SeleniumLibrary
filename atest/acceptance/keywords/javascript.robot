*** Settings ***
Test Setup        Go To Page "javascript/dynamic_content.html"
Resource          ../resource.robot

*** Variables ***
${TEXT}=   You scrolled in div.

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
    Execute Javascript with arguments    window.add_content('button_target', 'Inserted directly')
    Page Should Contain    Inserted directly

Execute Javascript from File
    [Documentation]    LOG 2:1 REGEXP: Reading JavaScript from file .*
    ...    LOG 2:2 Executing JavaScript:
    ...    window.add_content('button_target', 'Inserted via file')
    Execute Javascript with arguments    ${CURDIR}/executed_by_execute_javascript.js
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

Execute single line JavaScript with arguments
    [Documentation]    Scroll to element by executing javascript with target web
    ...    element as argument
    [Setup]    Go To Page "scroll/index.html"
    ${initial_position}=    Get Vertical Position    css:#target
    ${element}=    Get WebElement    css:#target
    ${unused}=    Set Variable    ununsed
    set test variable    ${script}    return arguments[0].scrollIntoView();
    Execute Javascript with arguments    ARGUMENTS    ${element}    ${unused}    JAVASCRIPT    ${script}
    ${position}=    Get Vertical Position    css:#target
    Should Be True    ${initial_position} > ${position}
    Element Should Contain    css:#result    ${TEXT}

Execute multiline JavaScript with arguments first
    ${integer_variable}=    Set Variable    123
    Execute Javascript with arguments
    ...    ARGUMENTS
    ...    ${integer_variable}
    ...    JAVASCRIPT
    ...    console.log('Hello, world!');
    ...    console.log(arguments[0]);

Execute multiline JavaScript with arguments last
    ${integer_variable}=    Set Variable    123
    Execute Javascript with arguments
    ...    JAVASCRIPT
    ...    console.log('Hello, world!');
    ...    console.log(arguments[0]);
    ...    ARGUMENTS
    ...    ${integer_variable}

Execute multiline JavaScript with multiple arguments
    [Setup]    Go To Page "tables/tables.html"
    ${number_variable}=    Set Variable    123
    ${string_variable}=    Set Variable    string
    ${boolean_variable}=    Set Variable    True
    ${null_variable}=    Set Variable    Null
    ${webelement_variable}=    Get WebElement    xpath://*[@id="mergedRows"]
    Execute Javascript with arguments
    ...    JAVASCRIPT
    ...    if (arguments[2]) {
    ...        console.log(arguments[3]);
    ...    } else {
    ...        console.log('This should not happen');
    ...    }
    ...    console.log(arguments[0]);
    ...    return arguments[4].scrollIntoView();
    ...    console.log(arguments[1].localname);
    ...    ARGUMENTS
    ...    ${number_variable}
    ...    ${string_variable}
    ...    ${boolean_variable}
    ...    ${null_variable}
    ...    ${webelement_variable}

Execute multiline JavaScript
    Execute Javascript with arguments
    ...    console.log('Hello, world!');
    ...    console.log('Here I am.');
    ...    console.log('Who else is here?');

Execute multiline JavaScript with marker
    Execute Javascript with arguments
    ...    JAVASCRIPT
    ...    console.log('Hello, world!');
    ...    console.log('Here I am.');
    ...    console.log('Who else is here?');


Execute multiline Javascript without marker with multiple arguments
    [Setup]    Go To Page "tables/tables.html"
    ${number_variable}=    Set Variable    123
    ${string_variable}=    Set Variable    string
    ${boolean_variable}=    Set Variable    True
    ${null_variable}=    Set Variable    Null
    ${webelement_variable}=    Get WebElement    xpath://*[@id="mergedRows"]
    Execute Javascript with arguments
    ...    console.log('Hello, world!');
    ...    console.log('Here I am.');
    ...    console.log('Who else is here?');
    ...    ARGUMENTS
    ...    ${number_variable}
    ...    ${string_variable}
    ...    ${boolean_variable}
    ...    ${null_variable}
    ...    ${webelement_variable}