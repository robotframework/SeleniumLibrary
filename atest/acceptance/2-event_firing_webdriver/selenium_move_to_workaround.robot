*** Settings ***
Documentation    Can be deleted when minimum Selenium version 4.0
Library          SeleniumLibrary     event_firing_webdriver=${CURDIR}/../../resources/testlibs/MyListener.py
Library           ../../resources/testlibs/ctrl_or_command.py
Resource         resource_event_firing_webdriver.robot
Force Tags       NoGrid
Suite Setup      Open Browser    ${FRONT PAGE}    ${BROWSER}    alias=event_firing_webdriver
...              remote_url=${REMOTE_URL}    desired_capabilities=${DESIRED_CAPABILITIES}
Suite Teardown    Close All Browsers

*** Variables ***
${event_firing_or_none}     ${NONE}
${CTRL_OR_COMMAND}    ${EMPTY}

*** Test Cases ***
Selenium move_to workaround Click Element At Coordinates
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
    Click Element At Coordinates    id:some_id    4    4

Selenium move_to workaround Scroll Element Into View
    [Documentation]    LOG 1:4 DEBUG  Workaround for Selenium 3 bug.
    Scroll Element Into View    id:some_id

Selenium move_to workaround Mouse Out
    [Documentation]    LOG 1:5 DEBUG  Workaround for Selenium 3 bug.
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
    ...    LOG 2:6 DEBUG GLOB: *actions {"actions": [{*
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

Press Keys Normal Keys
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    AAAAA
    Click Button    OK
    Wait Until Page Contains    AAAAA

Press Keys Normal Keys Many Times
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    AAAAA+BBB
    Click Button    OK
    Wait Until Page Contains    AAAAABBB

Press Keys Sends c++
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    c++
    Click Button    OK
    Wait Until Page Contains    c+

Press Keys Normal Keys Many Arguments
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    ccc    DDDD
    Click Button    OK
    Wait Until Page Contains    cccDDDD

Press Keys Normal Keys Many Times With Many Args
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    a+b    C+D
    Click Button    OK
    Wait Until Page Contains    abCD

Press Keys Special Keys SHIFT
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    SHIFT+cc
    Click Button    OK
    Wait Until Page Contains    CC

Press Keys Special Keys SHIFT Many Times
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    SHIFT+cc    SHIFT+dd
    Click Button    OK
    Wait Until Page Contains    CCDD     timeout=3

Press Keys To Multiple Elements
    [Documentation]    The | Press Keys | OK | ENTER | presses OK button two times, because
    ...    Selenium sets the focus to element by clicking the element.
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys      text_field    tidii
    Press Keys      OK            ENTER
    Press Keys      None          ENTER    ENTER
    Wait Until Page Contains    tidii     timeout=3
    Page Should Contain Element     //p[text()="tidii"]    limit=4

Press Keys ASCII Code Send As Is
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    \\108    \\13
    Click Button    OK
    Wait Until Page Contains    \\108\\13     timeout=3

Press Keys With Scandic Letters
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    ÖÄÖÄÖ    ÅÖÄP
    Click Button    OK
    Wait Until Page Contains    ÖÄÖÄÖÅÖÄP     timeout=3

Press Keys With Asian Text
    [Setup]        Go To Page "forms/input_special_keys.html"
    Press Keys    text_field    田中さんにあげ+て下    さい
    Click Button    OK
    Wait Until Page Contains    田中さんにあげて下さい     timeout=3

Press Keys Element Not Found
    [Setup]        Go To Page "forms/input_special_keys.html"
    Run Keyword And Expect Error
    ...    Element with locator 'not_here' not found.
    ...    Press Keys    not_here    YYYY

Press Keys No keys Argument
    [Setup]        Go To Page "forms/input_special_keys.html"
    Run Keyword And Expect Error
    ...    "keys" argument can not be empty.
    ...    Press Keys    text_field

Press Keys Without Element
    [Setup]        Go To Page "forms/input_special_keys.html"
    Click Element    text_field
    Press Keys       None    tidii
    Click Button     OK
    Wait Until Page Contains    tidii     timeout=3

Press Keys Multiple Times Without Element
    [Setup]        Go To Page "forms/input_special_keys.html"
    Click Element    text_field
    Press Keys       None    foo+bar    e+n+d
    Click Button     OK
    Wait Until Page Contains    foobarend     timeout=3

Press Keys Without Element Special Keys
    [Setup]        Go To Page "forms/input_special_keys.html"
    Click Element    text_field
    Press Keys       None    ${CTRL_OR_COMMAND}+A    ${CTRL_OR_COMMAND}+v
    Click Button     OK
    Wait Until Page Contains    Please input text and click the button. Text will appear in the page.     timeout=3

Click Element Modifier CTRL
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    modifier=CTRL
    Element Text Should Be    output    CTRL click

Click Link Modifier CTRL
    [Setup]    Initialize Page For Click Element With Modifier
    Click Link    link text    modifier=CTRL
    Element Text Should Be    output    CTRL click
    [Teardown]    Close Popup Window

Click Button Modifier CTRL
    [Setup]    Initialize Page For Click Element With Modifier
    Click Button    Click me!    modifier=CTRL
    Element Text Should Be    output    CTRL click

Click Image Modifier CTRL
    [Setup]    Initialize Page For Click Element With Modifier
    Click Image    robot    modifier=CTRL
    Element Text Should Be    output    CTRL click

Click Element Modifier ALT
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    alt
    Element Text Should Be    output    ALT click

Click Element Modifier Shift
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    Shift
    Element Text Should Be    output    Shift click

Click Element Modifier CTRL+Shift
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    modifier=CTRL+Shift
    Element Text Should Be    output    CTRL and Shift click

Click Element No Modifier
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    modifier=False
    Element Text Should Be    output    Normal click

Click Element Wrong Modifier
    [Setup]    Initialize Page For Click Element With Modifier
    Run Keyword And Expect Error
    ...    ValueError: 'FOOBAR' modifier does not match to Selenium Keys
    ...    Click Element    Button    Foobar

Click Element Action Chain and modifier
    [Documentation]     LOG 2:1 INFO Clicking element 'Button' with CTRL.
    [Setup]    Initialize Page For Click Element With Modifier
    Click Element    Button    modifier=CTRL    action_chain=True
    Element Text Should Be    output    CTRL click
    
*** Keywords ***
Initialize Page For Click Element
    [Documentation]    Initialize Page
    Go To Page "javascript/click.html"
    Reload Page
    Element Text Should Be    output    initial output

Initialize Page For Click Element With Modifier
    [Documentation]    Initialize Page
    Go To Page "javascript/click_modifier.html"
    Reload Page
    Element Text Should Be    output    initial output

Close Popup Window
    Switch Window    myName    timeout=5s
    Close Window
    Switch Window    MAIN      timeout=5s