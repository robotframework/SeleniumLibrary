*** Settings ***
Test Setup      Go To Page "forms/prefilled_email_form.html"
Resource        ../resource.robot

*** Test Cases ***
Checkbox Should Be Selected
    [Documentation]  LOG 2 Verifying checkbox 'can_send_email' is selected.
    Checkbox Should Be Selected  can_send_email
    Run Keyword And Expect Error  Checkbox 'can_send_sms' should have been selected but was not  Checkbox Should Be Selected  can_send_sms

Checkbox Should Not Be Selected
    [Documentation]  LOG 2 Verifying checkbox 'can_send_sms' is not selected.
    Checkbox Should Not Be Selected  can_send_sms
    Run Keyword And Expect Error  Checkbox 'can_send_email' should not have been selected  Checkbox Should Not Be Selected  can_send_email

Select Checkbox
    [Documentation]  LOG 2 Selecting checkbox 'can_send_sms'.
    Select Checkbox  can_send_sms
    Checkbox Should Be Selected  can_send_sms
    Select Checkbox  can_send_sms
    Checkbox Should Be Selected  can_send_sms

UnSelect Checkbox
    [Documentation]  LOG 2 Unselecting checkbox 'can_send_email'.
    Unselect Checkbox  can_send_email
    Checkbox Should Not Be Selected  can_send_email
    Unselect Checkbox  can_send_email
    Checkbox Should Not Be Selected  can_send_email

Radio Button Should Be Set To
    [Documentation]  LOG 2 Verifying radio button 'sex' has selection 'female'.
    Radio Button Should Be Set To  sex  female
    Run Keyword And Expect Error  Selection of radio button 'sex' should have been 'male' but was 'female'  Radio Button Should Be Set To  sex  male

Select Radio Button
    [Documentation]  LOG 2 Selecting 'male' from radio button 'sex'.
    Select Radio Button  sex  male
    Radio Button Should Be Set To  sex  male
    Select Radio Button  sex  female
    Radio Button Should Be Set To  sex  female

Radio Button Should Not Be Selected
    [Documentation]  LOG 2 Verifying radio button 'referrer' has no selection.
    Radio Button Should Not Be Selected  referrer
    Run Keyword And Expect Error  Radio button group 'sex' should not have had selection, but 'female' was selected  Radio Button Should Not Be Selected  sex

Clicking Radio Button Should Trigger Onclick Event
    [Setup]  Go To Page "javascript/dynamic_content.html"
    Select Radio Button  group  title
    Title Should Be  Changed by Button

