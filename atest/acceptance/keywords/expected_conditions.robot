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
    [Documentation]  FAIL REGEXP: TimeoutException: Message: Expected Condition not met within set timeout of 0.5*
    Title Should Be    Original
    Click Element    link=delayed change title
    Wait For Expected Condition   title_is  Delayed  timeout=0.5

Wait For Expected Conditions using WebElement as locator
    Click Button    Change the button state
    ${dynamic_btn}=  Get WebElement  id:enabledDisabledBtn
    Wait For Expected Condition  element_to_be_clickable  ${dynamic_btn}
