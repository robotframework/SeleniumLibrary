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

Scroll to Element via Javascript
    [Documentation]    Scroll to element by executing javascript with target web
    ...    element as argument
    [Tags]    javascript_with_args
    Go To Page "scroll/index.html"
    ${initial_position}=    Get Vertical Position    css:#target
    ${element}=    Get WebElement    css:#target
    set test variable    ${script}    return arguments[0].scrollIntoView();
    Execute Javascript with arguments    ${script}    ${element}
    ${position}=    Get Vertical Position    css:#target
    Should Be True    ${initial_position} > ${position}
    Element Should Contain    css:#result    ${TEXT}

# test multiline
Execute JavaScript test
#    [Tags]  test_only
    Go To Page "scroll/index.html"
    ${useless_variable}=  Set Variable  123
    Execute Javascript with arguments
    ...  ARGUMENTS
    ...  ${useless_variable}
    ...  JAVASCRIPT
    ...  alert('Hello, world!');
    ...  alert('This is me!');
    ...  alert(arguments[0]);

# python atest/run.py firefox --suite javascript --include test_only
Show WebElement type
    [Tags]  test_only
    Go To Page "tables/tables.html"
    ${element}=  get WebElement  xpath://*[@id="mergedRows"]
    ${useless_variable}=  Set Variable  123
    Execute Javascript with arguments
    ...  ARGUMENTS
    ...  ${element}
    ...  ${useless_variable}
    ...  JAVASCRIPT
#    ...  alert(typeof arguments[0]);
#    ...  element = document.evaluate("//*[@id='mergedRows']", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
#    ...  alert(typeof element);
    ...  return arguments[0].scrollIntoView();
#    ...  element = arguments[0]
#    ...  element.scrollIntoView();

Highlight background
#    [Tags]  test_only
    Go to Page "tables/tables.html"
    ${element}=  get WebElement  xpath://*[@id="mixed-th-td"]
    Execute Javascript with arguments
    ...  ARGUMENTS
    ...  ${element}
    ...  JAVASCRIPT
    ...  element_outside = arguments[0];
    ...  element_inside = document.getElementById('mergedCols');
    ...  console.log(typeof element_outside);
    ...  console.log(typeof element_inside);
    ...  return element_outside.scrollIntoView(behavior="auto");
