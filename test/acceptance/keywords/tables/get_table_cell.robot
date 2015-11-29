*** Settings ***
Documentation     Tests cell contents
Resource          table_resource.robot

*** Test Cases ***
Should Retrieve Text From Cell
    [Documentation]    Should Retrieve Text From Cell
    [Template]    Table Cell Should Be Equal With CSS And XPath Locators
    simpleTable    1    1    simpleTable_A1
    tableWithSingleHeader    1    1    tableWithSingleHeader_A1
    tableWithSingleHeader    3    3    tableWithSingleHeader_C3
    withHeadAndFoot    1    2    withHeadAndFoot_BH1
    withHeadAndFoot    4    3    withHeadAndFoot_C2
    withHeadAndFoot    6    1    withHeadAndFoot_AF1
    mergedRows    2    1    mergedRows_B2
    mergedCols    1    2    mergedCols_C1
    formattedTable    1    1    formattedTable_A1
    formattedTable    1    4    formattedTable_D1
    formattedTable    2    2    formattedTable_B2
    formattedTable    2    3    formattedTable_ÄÖÜäöüß
    formattedTable    2    4    äöü€&äöü€&

Should Give Error Message When Content Not Found In Table Cell
    [Documentation]    Should Give Error Message When Content Not Found In Table Cell
    Run Keyword And Expect Error
    ...    Cell in table 'simpleTable' in row #1 and column #2 should have contained text 'simpleTable_B3'.
    ...    Table Cell Should Contain    simpleTable    1    2    simpleTable_B3

Should Give Error Message When Index Out Of Bounds
    [Documentation]    Should Give Error Message When Index Out Of Bounds
    Run Keyword And Expect Error
    ...    Cell in table 'simpleTable' in row #10 and column #20 should have contained text 'simpleTable_B3'.
    ...    Table Cell Should Contain    simpleTable    10    20    simpleTable_B3

*** Keywords ***
Table Cell Should Be Equal With CSS And XPath Locators
    [Documentation]    Should Give Error Message When Index Out Of Bounds
    [Arguments]    ${tableId}    ${row}    ${col}    ${content}
    Run Table Keyword With CSS And XPath Locators
    ...    Table Cell Should Be Equal    ${table id}    ${row}    ${col}    ${content}

Table Cell Should Be Equal
    [Documentation]    Table Cell Should Be Equal
    [Arguments]    ${tableId}    ${row}    ${col}    ${content}
    ${cell}=    Get Table Cell    ${tableId}    ${row}    ${col}
    Should Be Equal    ${cell}    ${content}
