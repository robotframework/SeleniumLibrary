*** Settings ***
Test Setup      Go To Page "javascript/dynamic_content.html"
Resource        ../resource.robot

*** Test Cases ***
Clicking Elements Should Activate Javascript
    Title Should Be  Original
    Click Element  link=change title
    Title Should Be  Changed

Alert Should Be Present
    [Setup]  Go To Page "javascript/alert.html"
    Click Link  Click Me!
    Alert Should Be Present
    Click Link  Click Me Too!
    Alert Should Be Present  MULTILINE ALERT!
    Click Link  Click Me!
    Run Keyword And Expect Error  Alert text should have been 'foo bar' but was 'ALERT!'  Alert Should Be Present  foo bar

Get Alert Message
    [Setup]  Go To Page "javascript/alert.html"
    Click Link  Click Me!
    ${msg} =  Get Alert Message
    Should Be Equal  ${msg}  ALERT!
    Run Keyword And Expect Error  There were no alerts  Get Alert Message

Read Alert Message
    [Setup]  Go To Page "javascript/alert.html"
    Click Link  Click Me!
    ${msg} =  Get Alert Message  ${FALSE}
    Should Be Equal  ${msg}  ALERT!
    Dismiss Alert
    Run Keyword And Expect Error  There were no alerts  Get Alert Message

Input Text Into Prompt
  [Setup]  Go To Page "javascript/alert_prompt.html"
  Click Element  css=button
  Input Text Into Prompt  myname
  Dismiss Alert
  Page Should Contain  myname

Mouse Down On Link
    [TAGS]  Known Issue - Firefox
    [Setup]  Go To Page "javascript/mouse_events.html"
    Mouse Down On Image  image_mousedown
    Text Field Should Contain  textfield  onmousedown
    Mouse Up  image_mousedown
    Input text  textfield  ${EMPTY}
    Mouse Down On Link  link_mousedown
    Text Field Should Contain  textfield  onmousedown
    Mouse Up  link_mousedown

Confirm Action
    Click Button  Change the title
    ${msg}=  Confirm Action
    Title Should Be  Changed after confirmation
    Should Be Equal  ${msg}  Really change the title?

Cancel Action
    Choose Cancel On Next Confirmation
    Click Button  Change the title
    ${msg}=  Confirm Action
    Title Should Be  Original
    Should Be Equal  ${msg}  Really change the title?

Execute Javascript
    [Documentation]  LOG 2 Executing JavaScript:\n window.add_content('button_target', 'Inserted directly')
    Execute Javascript  window.add_content('button_target', 'Inserted directly')
    Page Should Contain  Inserted directly

Execute Javascript from File
    [Documentation]  LOG 2:1 REGEXP: Reading JavaScript from file .* LOG 2:2 Executing JavaScript:\n window.add_content('button_target', 'Inserted via file')
    Execute Javascript  ${CURDIR}/executed_by_execute_javascript.js
    Page Should Contain  Inserted via file

Open Context Menu
    [TAGS]  Known Issue - Firefox
    Go To Page "javascript/context_menu.html"
    Open Context Menu  myDiv

Drag and Drop
    [Setup]  Go To Page "javascript/drag_and_drop.html"
    Element Text Should Be  id=droppable    Drop here
    Drag and Drop   id=draggable  id=droppable
    Element Text Should Be  id=droppable    Dropped!

Drag and Drop by Offset
    [Setup]  Go To Page "javascript/drag_and_drop.html"
    Element Text Should Be   id=droppable   Drop here
    Drag and Drop by Offset   id=draggable  ${1}  ${1}
    Element Text Should Be   id=droppable   Drop here
    Drag and Drop by Offset  id=draggable   ${100}  ${20}
    Element Text Should Be   id=droppable   Dropped!
