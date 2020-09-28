*** Setting ***
Documentation     These tests must open own browser because windows opened by
...               earlier tests would otherwise be visible to Get Window XXX keywords
...               even if those windows were closed.
Suite Setup       Open Browser To Start Page Without Testing Default Options
Suite Teardown    Close All Browsers
Test Setup        Go To Page "javascript/popupwindow.html"
Resource          resource.robot

*** Test Cases ***
Popup Windows Created With Javascript
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Do Action In Popup Window And Verify
    Select Main Window And Verify

Get Window Titles
    ${exp_titles}=    Create List    Click link to show a popup window    Original
    Click Link    my popup
    Wait Until New Window Is Open
    ${titles}=    Get Window Titles
    Should Be Equal    ${titles}    ${exp_titles}

Get Window Titles With Non ASCII Title
    ${exp_titles}=    Create List    Click link to show a popup window    äää
    Click Link    my popup
    Wait Until New Window Is Open
    ${parent} =    Switch Window    Original
    Click Element    unicode
    ${titles} =    Get Window Titles
    Should Be Equal    ${titles}    ${exp_titles}
    [Teardown]  Switch Window    ${parent}

Get Title
    ${title} =    Get Title
    Should Be Equal As Strings    ${title}    Click link to show a popup window

Get Location
    ${current_url}=     Get Location
    Should Be Equal  ${current_url}    ${ROOT}/javascript/popupwindow.html

Get Locations
    ${expected_urls}=   Create List     ${ROOT}/javascript/dynamic_content.html     ${ROOT}/javascript/popupwindow.html
    ${urls}=    Get Locations
    Sort List  ${expected_urls}
    Sort List  ${urls}
    Lists Should Be Equal   ${urls}     ${expected_urls}

Get Window Names
    ${exp_names}=    Create List    undefined    myName
    Click Link    my popup
    Wait Until New Window Is Open
    ${names}=    Get Window Names
    Should Be Equal    ${names}    ${exp_names}

Get Window Identifiers
    ${exp_ids}=    Create List    undefined    undefined
    Click Link    my popup
    Wait Until New Window Is Open
    ${ids}=    Get Window Identifiers
    Should Be Equal    ${ids}    ${exp_ids}

Get and Set Window Size
    [Tags]  Known Issue Internet Explorer    Known Issue Safari
    Set Window Size    ${600}    ${800}
    ${width}    ${height}=    Get Window Size
    Should Be Equal    ${width}    ${600}
    Should Be Equal    ${height}    ${800}

Set Window Size using strings
    [Tags]  Known Issue Internet Explorer    Known Issue Safari
    Set Window Size    600    800
    ${width}    ${height}=    Get Window Size
    Should Be Equal    ${width}    ${600}
    Should Be Equal    ${height}    ${800}

Get and Set Inner Window Size
    Set Window Size    ${800}    ${600}    ${True}
    ${width}    ${height}=    Get Window Size    ${True}
    Should Be Equal    ${width}    ${800}
    Should Be Equal    ${height}    ${600}

Set Inner Window Size using strings
    Set Window Size    800    600    ${True}
    ${width}    ${height}=    Get Window Size    ${True}
    Should Be Equal    ${width}    ${800}
    Should Be Equal    ${height}    ${600}

Get and Set Inner Window Size with Frames
    Go To Page "frames/frameset.html"
    Select Frame            left
    Run Keyword And Expect Error
    ...    Keyword failed setting correct window size.
    ...    Set Window Size         ${400}    ${300}    ${True}

Get and Set Window Position
    [Tags]  Known Issue Chrome    Known Issue Safari
    Set Window Position    ${300}    ${200}
    ${x}    ${y}=    Get Window Position
    Should Be Equal    ${x}    ${300}
    Should Be Equal    ${y}    ${200}

Set Window Position using strings
    [Tags]  Known Issue Chrome    Known Issue Safari
    Set Window Position    200    100
    ${x}    ${y}=    Get Window Position
    Should Be Equal    ${x}    ${200}
    Should Be Equal    ${y}    ${100}

Select Window By Title After Close Window
    [Tags]    Known Issue Internet Explorer    Known Issue Safari
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Close Popup Window And Select Main Window By Title

Get Window Titles After Close Window
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Close Window
    ${titles}=    Get Window Titles

Select Window By Handle
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Click Link    my popup
    Wait Until New Window Is Open
    ${parent}=    Switch Window    Original
    Title Should Be    Original
    ${child}=    Switch Window    ${parent}
    Title Should Be    Click link to show a popup window
    Switch Window    ${child}
    Close Window
    ${FromWindow}=    Switch Window    ${parent}
    Title Should Be    Click link to show a popup window
    Should Be True    ${FromWindow} == None

Select Window With Delay By Title
    [Tags]    Known Issue Internet Explorer
    Click Button     id:MyButton
    Switch Window    Original    timeout=5
    Title Should Be    Original
    Close Window
    Switch Window    main
    Title Should Be    Click link to show a popup window

Select Window With Delay By Title And Window Not Found
    [Tags]    Known Issue Internet Explorer
    Click Button     id:MyButton
    Run Keyword And Expect Error
    ...    No window matching handle, name, title or URL 'Original' found.
    ...    Switch Window    Original    timeout=0.2
    [Teardown]    Switch Window    main

Select Popup Window By Excluded List
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    @{excluded_handle_list}=    Get Window Handles
    Click Link    my popup
    ${parent}=    Switch Window    ${excluded_handle_list}    timeout=5
    Title Should Be    Original
    Close Window
    Switch Window    ${parent}
    Title Should Be    Click link to show a popup window

Select Popup Window With Delay By Excluded List
    [Tags]    Known Issue Internet Explorer
    @{excluded_handle_list}=    Get Window Handles
    Click Button     id:MyButton
    Switch Window    ${excluded_handle_list}    timeout=5
    Title Should Be    Original
    Close Window
    Switch Window    main
    Title Should Be    Click link to show a popup window

Select Window By Special Locator
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    ${start}=    Switch Window    current
    Click Link    my popup
    ${parent}=    Switch Window    new    timeout=5
    Title Should Be    Original
    Should Be True    '${start}' == '${parent}'
    Close Window
    Switch Window    main
    Title Should Be    Click link to show a popup window

Select Window With Delay By Special Locator
    [Tags]    Known Issue Internet Explorer
    Click Button     id:MyButton
    Switch Window    new    timeout=5
    Title Should Be    Original
    Close Window
    Switch Window    main
    Title Should Be    Click link to show a popup window

*** Keywords ***
Open Popup Window, Select It And Verify
    [Arguments]    ${window_id}
    Click Link    my popup
    Switch Window    ${window_id}    timeout=5
    Title should Be    Original

Select Main Window And Verify
    Close Window
    Switch Window    main    timeout=5
    Title Should Be    Click link to show a popup window

Do Action In Popup Window And Verify
    Click Link    change title
    Title Should Be    Changed

Close Popup Window And Select Main Window By Title
    Close Window
    Switch Window    title=Click link to show a popup window

Wait Until New Window Is Open
    Wait Until Keyword Succeeds    5    1    New Windows Should Be Open

New Windows Should Be Open
    ${titles} =    Get Window Titles
    Should Be True    len(${titles}) > 1
