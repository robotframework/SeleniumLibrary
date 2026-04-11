*** Settings ***
Documentation    Tests for the custom Drag And Drop To Frame keyword
...              in cross-frame drag-and-drop scenarios.
Resource         ../resource.robot
Test Setup       Go To Page "frames/draganddrop.html"
Force Tags       draganddrop

*** Test Cases ***
Drag And Drop To Frame Works With Local HTML
    [Documentation]    Verifies successful cross-frame drag-and-drop from default content to a target inside an iframe.
    Wait Until Page Contains Element    id=source    timeout=10s
    Drag And Drop To Frame    id=source    id=target    id=previewFrame
    Select Frame    id=previewFrame
    Element Should Contain    id=target    Dropped Successfully!
    Unselect Frame

Drag And Drop To Frame Returns To Default Content
    [Documentation]    Verifies that the keyword returns to default content after execution.
    Wait Until Page Contains Element    id=source    timeout=10s
    Drag And Drop To Frame    id=source    id=target    id=previewFrame
    Element Should Be Visible    id=previewFrame

Drag And Drop To Frame Hides Source Element
    [Documentation]    Verifies that the source element becomes hidden after a successful drop.
    Wait Until Page Contains Element    id=source    timeout=10s
    Drag And Drop To Frame    id=source    id=target    id=previewFrame
    Element Should Not Be Visible    id=source

Standard Drag And Drop Fails When Target Is Inside Frame
    [Documentation]    Verifies that the standard Drag And Drop keyword cannot complete this cross-frame scenario.
    Wait Until Page Contains Element    id=source    timeout=10s
    Run Keyword And Expect Error    *    Drag And Drop    id=source    id=target
    Select Frame    id=previewFrame
    Element Should Not Contain    id=target    Dropped Successfully!
    Unselect Frame

Drag And Drop To Frame Fails With Invalid Frame
    [Documentation]    Verifies that the keyword fails when the frame locator is invalid.
    Wait Until Page Contains Element    id=source    timeout=10s
    Run Keyword And Expect Error    *    Drag And Drop To Frame
    ...    id=source    id=target    id=missingFrame

Drag And Drop To Frame Fails With Invalid Target
    [Documentation]    Verifies that the keyword fails when the target element is not found inside the iframe.
    Wait Until Page Contains Element    id=source    timeout=10s
    Run Keyword And Expect Error    *    Drag And Drop To Frame
    ...    id=source    id=missingTarget    id=previewFrame