*Setting*
Variables  variables.py
Resource  ../resource.robot
Test Setup  Go To Page "forms/login_alert.html"


*Test Cases*

Input Password into AlertPrompt
  [Documentation]  LOG 3 Typing password into alertprompt 'password_field'
  Input Text Into Prompt  password
