*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Find Text In Table Content
    [Template]    Verify Table Contains With CSS And XPath Locators
    simpleTable    simpleTable_A1
    simpleTable    simpleTable_C3
    simpleWithNested    simpleWithNested_A1
    simpleWithNested    nestedTable_A1
    nestedTable    nestedTable_A1
    nestedTable    nestedTable_C3
    tableWithSingleHeader    tableWithSingleHeader_B1
    tableWithSingleHeader    tableWithSingleHeader_B2
    withHeadAndFoot    withHeadAndFoot_AH1
    withHeadAndFoot    withHeadAndFoot_B2
    withHeadAndFoot    withHeadAndFoot_CF1
    mergedRows    mergedRows_A1
    mergedCols    mergedCols_B2
    formattedTable    formattedTable_A1
    formattedTable    formattedTable_B1
    formattedTable    formattedTable_C1
    formattedTable    formattedTable_A2
    formattedTable    formattedTable_B2
    formattedTable    formattedTable_ÄÖÜäöüß
    formattedTable    äöü€&äöü€&

Should Find Text In Table Content with CSS Specific Mechanics
    Table Should Contain    formattedTable    formattedTable_D1

Should Give Error Message When Content Not Found In Table
    Run Keyword And Expect Error
    ...    Table 'simpleTable' did not contain text 'Not here'.
    ...    Table Should Contain    simpleTable    Not here

*** Keywords ***
Verify Table Contains With CSS And XPath Locators
    [Arguments]    ${table id}    ${expected}
    Run Table Keyword With CSS And XPath Locators
    ...    Table Should Contain    ${table id}    ${expected}
