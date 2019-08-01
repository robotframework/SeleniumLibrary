*** Settings ***
Test Setup        Go To Page "forms/named_submit_buttons.html"
Resource          ../resource.robot

*** Variables ***
${FORM SUBMITTED}    forms/submit.html

*** Test Cases ***
Submit Form
    [Documentation]    LOG 2 Submitting form 'form_name'.
    Submit Form    form_name
    Verify Location Is "${FORM SUBMITTED}"

Submit Form Without Args
    [Setup]    Go To Page "forms/form_without_name.html"
    Submit Form
    Verify Location Is "target/first.html"

Click Ok Button By Name
    [Documentation]    LOG 2 Clicking button 'ok_button'.
    Click Button    ok_button
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Name
    Click Button    cancel_button
    Value Should Be Cancel

Click Ok Button By Value
    Click Button    Ok
    Verify Location Is "${FORM SUBMITTED}"

Click Cancel Button By Value
    Click Button    Cancel
    Value Should Be Cancel

Click button created with <button> by id
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    button
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by value attribute
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    Get In
    Verify Location Is "${FORM SUBMITTED}"

Click button created with <button> by tag content
    [Documentation]    Click button created with <button> by tag content
    [Setup]    Go To Page "forms/buttons.html"
    Click Button    Sisään
    Verify Location Is "${FORM SUBMITTED}"

Click Image With Submit Type Images
    [Setup]    Go To Page "forms/form_with_image_submit.html"
    Click Image    robot.bmp
    Verify Location Is "${FORM SUBMITTED}"

*** Keywords ***
Value Should Be Cancel
    ${value} =    Get Value    textfield
    Should Be Equal    ${value}    Cancel
