*** Setting ***
Documentation     These tests must open own browser because windows opened by
...               earlier tests would otherwise be visible to Get Window XXX keywords
...               even if those windows were closed.
Suite Setup       Open Browser To Start Page Without Testing Default Options
Suite Teardown    Close All Browsers
Test Setup        Go To Page "javascript/popupwindow.html"
Force Tags        windows
Resource          resource.robot

*** Test Cases ***
Popup Windows Created With Javascript
    Cannot Be Executed in IE
    Cannot Be Executed In Chrome
    Open Popup Window, Select It And Verify    myName
    Do Action In Popup Window And Verify
    Select Main Window And Verify

Get Window Titles
  [Tags]  Known Issue - TravisCI
  ${exp_titles}=  Create List  Click link to show a popup window  Original
  Click Link  my popup
  ${titles}=  Get Window Titles
  Should Be Equal  ${titles}  ${exp_titles}

Get Window Names
  ${exp_names}=  Create List  selenium_main_app_window  myName
  Click Link  my popup
  ${names}=  Get Window Names
  Should Be Equal  ${names}  ${exp_names}

Get Window Identifiers
  ${exp_ids}=  Create List  undefined  undefined
  Click Link  my popup
  ${ids}=  Get Window Identifiers
  Should Be Equal  ${ids}  ${exp_ids}

Get and Set Window Size
  ${win_width}=  Set Variable  ${600}
  ${win_height}=  Set Variable  ${800}
  Set Window Size  ${win_width}  ${win_height}
  ${returned_width}  ${returned_height}=  Get Window Size
  Should Be Equal  ${returned_width}  ${win_width}
  Should Be Equal  ${returned_height}  ${win_height}


Get and Set Window Position
  ${position_x}=  Set Variable  ${100}
  ${position_y}=  Set Variable  ${100}
  Set Window Position  ${position_x}  ${position_y}
  ${returned_x}  ${returned_y}=  Get Window Position
  Should Be Equal  ${position_x}  ${returned_x}
  Should Be Equal  ${position_y}  ${returned_y}


***Keywords***
Open Popup Window, Select It And Verify
  [Arguments]  ${window_id}
  Click Link  my popup
  Select Window  ${window_id}
  Title should Be  Original

Select Main Window And Verify
  Close Window
  Select Window  main
  Title Should Be  Click link to show a popup window

Do Action In Popup Window And Verify
  Click Link  change title
  Title Should Be  Changed
