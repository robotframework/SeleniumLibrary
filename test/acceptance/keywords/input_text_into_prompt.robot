*Setting*
Variables  variables.py
Resource  ../resource.robot
Test Setup  Go To Page "javascript/alert_prompt.html"


*Test Cases*

Verify Input Text into Prompt
  [Documentation]  Typing name into prompt
  Click Element  css=button
  Input Text Into Prompt  myname
  Get Alert Message
