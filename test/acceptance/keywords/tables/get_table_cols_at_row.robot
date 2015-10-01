*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Count Table Cols At Row Should Be
    [Template]    Table Cols At Row Should Be Equal With CSS And XPath Locators
    simpleTable    1    3
    simpleWithNested    2    12
    tableWithSingleHeader    1    3
    tableWithSingleHeader    2    3
    tableWithTwoHeaders    1    3
    tableWithTwoHeaders    3    3
    withHeadAndFoot    4    3
    mergedRows    1    4
    mergedRows    2    2
    mergedRows    3    2
    mergedCols    1    2
    mergedCols    2    2
    mergedCols    3    3
    mergedCols    4    1

*** Keywords ***
Table Cols At Row Should Be Equal With CSS And XPath Locators
    [Arguments]    ${tableId}    ${row}    ${cols}
    Run Table Keyword With CSS And XPath Locators    Table Cols At Row Should Be Equal    ${tableId}    ${row}    ${cols}

Table Cols At Row Should Be Equal
    [Arguments]    ${tableId}    ${row}    ${cols}
    ${getcols}=    Get Table Cols At Row    ${tableId}    ${row}
    Should Be Equal As Integers    ${getcols}    ${cols}
