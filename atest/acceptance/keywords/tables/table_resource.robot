*** Settings ***
Resource          ../../resource.robot

*** Keywords ***
Run Table Keyword With CSS And XPath Locators
    [Arguments]    ${keyword}    ${table id}    @{args}
    Run Keyword    ${keyword}    ${table id}    @{args}
    Run Keyword    ${keyword}    //table[@id="${table id}"]    @{args}
