*** Settings ***
Resource        ../../resource.robot

*** Keywords ***
Run Table Keyword With CSS And XPath Locators
    [Arguments]  ${keyword}  ${table id}  @{args}
    Run Keyword  ${keyword}  ${table id}  @{args}
    ${xpath}=  Get Table XPath  ${table id}
    Run Keyword  ${keyword}  ${xpath}  @{args}

Get Table XPath
    [Arguments]  ${table id}
    [Return]  xpath=//table[@id="${table id}"]

