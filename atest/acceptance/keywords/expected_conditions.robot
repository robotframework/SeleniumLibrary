*** Settings ***
Test Setup        Go To Page "javascript/expected_conditions.html"
Resource          ../resource.robot

*** Test Cases ***
Wait For Expected Conditions One Argument
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition    title_is    Delayed
    Title Should Be    Delayed

Wait For Expected Condition Times out within set timeout
    [Documentation]  FAIL STARTS: TimeoutException: Message: Expected Condition not met within set timeout of 0.3
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition   title_is  Delayed  timeout=0.3

Wait For Expected Conditions using WebElement as locator
    Click Button    Change the button state
    ${dynamic_btn}=  Get WebElement  id:enabledDisabledBtn
    Wait For Expected Condition  element_to_be_clickable  ${dynamic_btn}

Wait For Expected Conditions Where Condition Written With Spaces
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition    title is    Delayed
    Title Should Be    Delayed

Wait For Expected Conditions Where Condition Is Variable
    ${condition}=  Set Variable  title is
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition    ${condition}    Delayed
    Title Should Be    Delayed

Wait For Expected Conditions Where Condition Is Strange Case
    Click Button    Change the button state
    ${dynamic_btn}=  Get WebElement  id:enabledDisabledBtn
    Wait For Expected Condition  EleMENT tO BE cLiCkAbLe  ${dynamic_btn}

Wait For Non Existing Expected Conditions
    Click Button    Change the button state
    ${dynamic_btn}=  Get WebElement  id:enabledDisabledBtn
    Run Keyword And Expect Error   this_is_not_an_expected_con_dition is an unknown expected condition
    ...  Wait For Expected Condition  this_is not an expected con dition  ${dynamic_btn}

Wait For Expected Conditions When Condition Includes Locator
    Title Should Be    Original
    ${byElem}=  Evaluate  ("id","added_btn")
    Click Element    link:delayed add element
    Wait For Expected Condition    Presence Of Element Located    ${byElem}
    Click Element    id:added_btn