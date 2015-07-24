*** Settings ***
Resource        table_resource.robot

*** Test Cases ***
Should Find Text In Specific Row
    [Template]  Table Row Should Contain With CSS And XPath Locators
    simpleTable  1  simpleTable_A1
    simpleTable  3  simpleTable_C3
    simpleWithNested  1  simpleWithNested_A1
    simpleWithNested  1  nestedTable_A1
    nestedTable  1  nestedTable_A1
    nestedTable  3  nestedTable_C3
    tableWithSingleHeader  1  tableWithSingleHeader_B1
    tableWithSingleHeader  2  tableWithSingleHeader_B2
    withHeadAndFoot  2  withHeadAndFoot_B2
    mergedRows  1  mergedRows_A1
    mergedCols  2  mergedCols_B2
    formattedTable  1  formattedTable_A1
    formattedTable  1  formattedTable_B1
    formattedTable  1  formattedTable_C1
    formattedTable  2  formattedTable_A2
    formattedTable  2  formattedTable_B2
    formattedTable  2  formattedTable_ÄÖÜäöüß
    formattedTable  2  äöü€&äöü€&

Should Find Text In Specific Row with CSS Specific Mechnanics
    Table Row Should Contain  formattedTable  1  formattedTable_D1

Should Give Error Message When Content Not Found In Table Row
    Run Keyword And Expect Error  Row #2 in table identified by 'simpleTable' should have contained text 'simpleTable_B3'.  Table Row Should Contain  simpleTable  2  simpleTable_B3

Should Give Error Message When Row Number Out Of Bounds
    Run Keyword And Expect Error  Row #20 in table identified by 'simpleTable' should have contained text 'simpleTable_B3'.  Table Row Should Contain  simpleTable  20  simpleTable_B3

*** Keywords ***
Table Row Should Contain With CSS And XPath Locators
    [Arguments]  ${table id}  ${row}  ${expected}
    Run Table Keyword With CSS And XPath Locators  Table Row Should Contain  ${table id}  ${row}  ${expected}

