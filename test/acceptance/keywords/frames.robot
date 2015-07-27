*** Setting ***
Test Setup        Go To Page "frames/frameset.html"
Test Teardown     Run Keywords    Set Selenium Speed    0 seconds    AND    UnSelect Frame
Force Tags        frames
Resource          ../resource.robot

*** Test Cases ***
Frame Should Contain
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Frame Should contain    right    You're looking at right.
    Frame Should Contain    left    Links

Frame Should Contain should also work with iframes
    [Setup]    Go To Page "frames/iframes.html"
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Frame Should contain    right    You're looking at right.
    Frame Should Contain    left    Links

Page Should Contain Text Within Frames
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Page Should contain    You're looking at right.
    Page Should Contain    Links

Page Should Contain Text Within Frames should also work with iframes
    [Setup]    Go To Page "frames/iframes.html"
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Page Should contain    You're looking at right.
    Page Should Contain    Links

Select And Unselect Frame
    [Documentation]    LOG 3:1 INFO Selecting frame 'left'.\ LOG 6:1 INFO Selecting frame 'right'.\ LOG 7:3 INFO Current page contains text 'You're looking at foo.'.
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Contains    You're looking at foo.

Select And Unselect Frame should also work with iframes
    [Documentation]    Selecting frame leftiframe
    [Setup]    Go To Page "frames/iframes.html"
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Select Frame    left
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Contains    You're looking at foo.

Select Frame with non-unique name attribute
    [Documentation]    Descerning frame 'left' from link 'left'.
    [Setup]    Go To Page "frames/poorlynamedframe.html"
    Run Keyword If    '${BROWSER}'.lower() == 'ie' or '${BROWSER}'.lower().replace(' ', '') == 'internetexplorer'    Set Selenium Speed    0.2 seconds
    Run Keyword And Expect Error    NoSuchFrameException*    Select Frame    left
    Select Frame    xpath=//frame[@name='left']|//iframe[@name='left']
    Click Link    foo
    Unselect Frame
    Select Frame    right
    Current Frame Contains    You're looking at foo.
