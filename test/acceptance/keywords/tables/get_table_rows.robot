*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Count Table Rows Should Be
    [Template]    Table Rows Should Be Equal With CSS And XPath Locators
    simpleTable    3
    simpleWithNested    3
    tableWithSingleHeader    3
    tableWithTwoHeaders    4
    withHeadAndFoot    7
    mergedRows    3
    mergedCols    4
    formattedTable    2

*** Keywords ***
Table Rows Should Be Equal With CSS And XPath Locators
    [Arguments]    ${tableId}    ${rows}
    Run Table Keyword With CSS And XPath Locators    Table Rows Should Be Equal    ${tableId}    ${rows}

Table Rows Should Be Equal
    [Arguments]    ${tableId}    ${rows}
    ${getrows}=    Get Table Rows    ${tableId}
    Should Be Equal As Integers    ${getrows}    ${rows}
