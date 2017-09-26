*** Setting ***
Documentation     Tests frames
Test Setup        Go To Page "frames/frameset.html"
Test Teardown     UnSelect Frame
Resource          ../resource.robot

*** Test Cases ***
Frame Should Contain
    Frame Should contain    right    You're looking at right.
    Frame Should Contain    left    Links

Frame Should Contain should also work with iframes
    [Setup]    Go To Page "frames/iframes.html"
    Frame Should contain    right    You're looking at right.
    Frame Should Contain    left    Links

Current Frame Should (Not) Contain
    Select Frame    left
    Current Frame Should Contain    This is LEFT side.
    Current Frame Should Not Contain   RIGHT
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    This is RIGHT side.
    Current Frame Should Not Contain   LEFT

Current Frame Contains is deprecated
    [Documentation]    "Current Frame Contains" is deprecated in favor of "Current Frame Should Contain"
    Select Frame    left
    Current Frame Contains    This is LEFT side.

Page Should Contain Text Within Frames
    Page Should contain    You're looking at right.
    Page Should Contain    Links

Page Should Contain Text Within Frames should also work with iframes
    [Setup]    Go To Page "frames/iframes.html"
    Page Should contain    You're looking at right.
    Page Should Contain    Links

Select And Unselect Frame
    [Documentation]    LOG 2 Selecting frame 'left'.
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    You're looking at foo.

Select And Unselect Frame should also work with iframes
    [Setup]    Go To Page "frames/iframes.html"
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    You're looking at foo.

Select Frame with non-unique name attribute
    [Setup]    Go To Page "frames/poorlynamedframe.html"
    Run Keyword And Expect Error    NoSuchFrameException*    Select Frame    left
    Select Frame    xpath=//frame[@name='left']|//iframe[@name='left']
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Should Contain    You're looking at foo.
