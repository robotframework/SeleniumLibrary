*Setting*
Variables  variables.py
Resource  ../resource.robot
Test Setup  Go To Page "javascript/password_prompt.html"


*Test Cases*

Verify Input Text into Prompt
  [Documentation]  Typing name into prompt
  Click Element  id=demo
  Input Text Into Prompt  myname
  Page Should Contain  myname
