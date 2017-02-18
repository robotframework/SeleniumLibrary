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
    [Documentation]    Popup Windows Created With Javascript
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Do Action In Popup Window And Verify
    Select Main Window And Verify

Get Window Titles
    [Documentation]    Get Window Titles
    ${exp_titles}=    Create List    Click link to show a popup window    Original
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${titles}=    Get Window Titles
    Should Be Equal    ${titles}    ${exp_titles}

Get Title
    ${title} =    Get Title
    Should Be Equal As Strings    ${title}    Click link to show a popup window

Get Location
    [Documentation]  Get current location
    ${current_url}=     Get Location
    Should Be Equal  ${current_url}    ${ROOT}/javascript/popupwindow.html

Get Locations
    [Documentation]  Get all window locations
    ${expected_urls}=   Create List     ${ROOT}/javascript/dynamic_content.html     ${ROOT}/javascript/popupwindow.html
    ${urls}=    Get Locations
    Sort List  ${expected_urls}
    Sort List  ${urls}
    Lists Should Be Equal   ${urls}     ${expected_urls}

Get Window Names
    [Documentation]    Get Window Names
    ${exp_names}=    Create List    selenium_main_app_window    myName
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${names}=    Get Window Names
    Should Be Equal    ${names}    ${exp_names}

Get Window Identifiers
    [Documentation]    Get Window Identifiers
    ${exp_ids}=    Create List    undefined    undefined
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${ids}=    Get Window Identifiers
    Should Be Equal    ${ids}    ${exp_ids}

Get and Set Window Size
    [Documentation]    Get and Set Window Size
    [Tags]  Known Issue Chrome    Known Issue Internet Explorer    Known Issue Safari
    ${win_width}=    Set Variable    ${600}
    ${win_height}=    Set Variable    ${800}
    Set Window Size    ${win_width}    ${win_height}
    ${returned_width}    ${returned_height}=    Get Window Size
    Should Be Equal    ${returned_width}    ${win_width}
    Should Be Equal    ${returned_height}    ${win_height}

Get and Set Window Position
    [Documentation]    Get and Set Window Position
    [Tags]  Known Issue Chrome    Known Issue Safari
    ${position_x}=    Set Variable    ${100}
    ${position_y}=    Set Variable    ${100}
    Set Window Position    ${position_x}    ${position_y}
    ${returned_x}    ${returned_y}=    Get Window Position
    Should Be Equal    ${position_x}    ${returned_x}
    Should Be Equal    ${position_y}    ${returned_y}

Select Window By Title After Close Window
    [Documentation]    Select Window By Title After Close Window
    [Tags]    Known Issue Internet Explorer    Known Issue Safari
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Close Popup Window And Select Main Window By Title

Get Window Titles After Close Window
    [Documentation]    Get Window Titles After Close Window
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Open Popup Window, Select It And Verify    myName
    Close Window
    ${titles}=    Get Window Titles

Select Window By Handle
    [Documentation]    Select Window By Handle
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${parent}=    Select Window    Original
    Title Should Be    Original
    ${child}=    Select Window    ${parent}
    Title Should Be    Click link to show a popup window
    Select Window    ${child}
    Close Window
    ${FromWindow}=    Select Window    ${parent}
    Title Should Be    Click link to show a popup window
    Should Be True    ${FromWindow} == None

Select Popup Window By Excluded List
    [Documentation]    Select Popup Window By Excluded List
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    @{excluded_handle_list}=    List Windows
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${parent}=    Select Window    ${excluded_handle_list}
    Title Should Be    Original
    Close Window
    Select Window    ${parent}
    Title Should Be    Click link to show a popup window

Select Window By Special Locator
    [Documentation]    Select Window By Special Locator
    [Tags]    Known Issue Internet Explorer
    Cannot Be Executed in IE
    ${start}=    Select Window    self
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    ${parent}=    Select Window    new
    Title Should Be    Original
    Should Be True    '${start}' == '${parent}'
    Close Window
    Select Window    main
    Title Should Be    Click link to show a popup window

*** Keywords ***
Open Popup Window, Select It And Verify
    [Arguments]    ${window_id}
    [Documentation]    Open Popup Window, Select It And Verify
    Click Link    my popup
    Wait Until Keyword Succeeds    5    1    Wait Until Window Is Open
    Select Window    ${window_id}
    Title should Be    Original

Select Main Window And Verify
    [Documentation]    Select Main Window And Verify
    Close Window
    Select Window    main
    Title Should Be    Click link to show a popup window

Do Action In Popup Window And Verify
    [Documentation]    Do Action In Popup Window And Verify
    Click Link    change title
    Title Should Be    Changed

Close Popup Window And Select Main Window By Title
    [Documentation]    Close Popup Window And Select Main Window By Title
    Close Window
    Select Window    title=Click link to show a popup window

Wait Until Window Is Open
    ${titles} =    Get Window Titles
    ${status} =    Evaluate    len(${titles}) > 1
    Should Be True    ${status}
