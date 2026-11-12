*** Settings ***
Documentation    Tests for the custom Drag And Drop Across Frames keyword
...              in cross-frame drag-and-drop scenarios.
Resource         ../resource.robot
Test Setup       Prepare Drag And Drop Page
Test Teardown    Restore Window Size

*** Test Cases ***
Drag And Drop Across Frames Works From Default Content
    [Tags]    Known Issue Firefox
    [Documentation]    Verifies drag-and-drop from default content to a target inside an iframe.
    Wait Until Page Contains Element    id=defaultSource    10s
    Drag And Drop Across Frames    id=defaultSource    id=target    id=targetFrame
    Select Frame    id=targetFrame
    Element Should Contain    id=target    Dropped Successfully!
    Unselect Frame

Drag And Drop Across Frames Works From Source Frame
    [Tags]    Known Issue Firefox
    [Documentation]    Verifies drag-and-drop from a source iframe to a target iframe.
    Wait Until Page Contains Element    id=sourceFrame    10s
    Select Frame    id=sourceFrame
    Wait Until Page Contains Element    id=frameSource    10s
    Unselect Frame
    Drag And Drop Across Frames    id=frameSource    id=target    id=targetFrame    id=sourceFrame
    Select Frame    id=targetFrame
    Element Should Contain    id=target    Dropped Successfully!
    Unselect Frame

Drag And Drop Across Frames Returns To Default Content
    [Documentation]    Verifies that the keyword returns to default content after execution.
    Wait Until Page Contains Element    id=defaultSource    10s
    Drag And Drop Across Frames    id=defaultSource    id=target    id=targetFrame
    Page Should Not Contain Element    id=target

Drag And Drop Across Frames Hides Default Source Element
    [Tags]    Known Issue Firefox
    [Documentation]    Verifies that the default source element becomes hidden after a successful drop.
    Wait Until Page Contains Element    id=defaultSource    10s
    Drag And Drop Across Frames    id=defaultSource    id=target    id=targetFrame
    Element Should Not Be Visible    id=defaultSource

Drag And Drop Across Frames Hides Frame Source Element
    [Tags]    Known Issue Firefox
    [Documentation]    Verifies that the frame source element becomes hidden after a successful drop.
    Wait Until Page Contains Element    id=sourceFrame    10s
    Drag And Drop Across Frames    id=frameSource    id=target    id=targetFrame    id=sourceFrame
    Select Frame    id=sourceFrame
    Element Should Not Be Visible    id=frameSource
    Unselect Frame

Drag And Drop Across Frames Fails With Invalid Target Frame
    [Documentation]    Verifies that the keyword fails when the target frame locator is invalid.
    Wait Until Page Contains Element    id=defaultSource    10s
    Run Keyword And Expect Error
    ...    Element with locator 'id=missingFrame' not found.
    ...    Drag And Drop Across Frames
    ...    id=defaultSource    id=target    id=missingFrame

Drag And Drop Across Frames Fails With Invalid Target
    [Documentation]    Verifies that the keyword fails when the target element is not found inside the target iframe.
    Wait Until Page Contains Element    id=defaultSource    10s
    Run Keyword And Expect Error
    ...    Element with locator 'id=missingTarget' not found.
    ...    Drag And Drop Across Frames
    ...    id=defaultSource    id=missingTarget    id=targetFrame

Drag And Drop Across Frames Fails With Invalid Source Frame
    [Documentation]    Verifies that the keyword fails when the source frame locator is invalid.
    Wait Until Page Contains Element    id=defaultSource    10s
    Run Keyword And Expect Error
    ...    Element with locator 'id=missingSourceFrame' not found.
    ...    Drag And Drop Across Frames
    ...    id=frameSource    id=target    id=targetFrame    id=missingSourceFrame

Drag And Drop Across Frames Fails With Invalid Source
    [Documentation]    Verifies that the keyword fails when the source element is not found.
    Wait Until Page Contains Element    id=defaultSource    10s
    Run Keyword And Expect Error
    ...    Element with locator 'id=missingSource' not found.
    ...    Drag And Drop Across Frames
    ...    id=missingSource    id=target    id=targetFrame

*** Keywords ***
Prepare Drag And Drop Page
    ${width}    ${height}=    Get Window Size
    Set Test Variable    ${ORIGINAL_WINDOW_WIDTH}    ${width}
    Set Test Variable    ${ORIGINAL_WINDOW_HEIGHT}    ${height}
    Set Window Size    1440    1000
    Go To Page "frames/draganddrop.html"

Restore Window Size
    Set Window Size    ${ORIGINAL_WINDOW_WIDTH}    ${ORIGINAL_WINDOW_HEIGHT}
