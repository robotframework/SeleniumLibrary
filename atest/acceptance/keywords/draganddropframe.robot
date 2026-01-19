*** Settings ***
Documentation     New Keyword for Drag and Drop Frame
Test Setup        Go To Page "frames/draganddrop.html"
Test Teardown     Close Browser
Resource          ../resource.robot
Force Tags        dragandDrop

*** Test Cases ***
Positive Test_Drag And Drop To Frame Local HTML using new Keyword Drag And Drop To Frame
    [Documentation]     Tests new Keyword created.
    Maximize Browser Window
    Wait Until Element Is Visible    id=source    10s
    ${Status}=  Run Keyword And Return Status       Drag And Drop To Frame    id=source    id=target    id=previewFrame
    Capture Page Screenshot
    log         Returned ${Status}: due to new Keyword switched to iframe and dragged and dropped the element from soruce to target succesfully.
    Select Frame    id=previewFrame
    Element Should Contain    id=target    Dropped Successfully!
    Unselect Frame
    Capture Page Screenshot    dropped.png
    [Teardown]

Negative Test_Drag And Drop To Frame Local HTML using existing keyword Drag And Drop
    [Documentation]     Tests existing Keyword keyword.
    Maximize Browser Window
    Wait Until Element Is Visible    id=source    10s
    ${Error Message}=    Run Keyword And Expect Error       *       Drag And Drop                    id=source    id=target
    Capture Page Screenshot
    log         Returned ${Error Message} due to target element is inside iframe
    [Teardown]    Close Browser
