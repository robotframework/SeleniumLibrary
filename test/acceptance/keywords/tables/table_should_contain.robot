*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Find Text In Table Content
    [Template]    Table Should Contain
    simpleTable              simpleTable_A1
    id:simpleTable           simpleTable_C3
    css:#simpleWithNested    simpleWithNested_A1
    simpleWithNested         nestedTable_A1
    nestedTable              nestedTable_A1
    nestedTable              nestedTable_C3
    tableWithSingleHeader    tableWithSingleHeader_B1
    tableWithSingleHeader    tableWithSingleHeader_B2
    withHeadAndFoot          withHeadAndFoot_AH1
    withHeadAndFoot          withHeadAndFoot_B2
    withHeadAndFoot          withHeadAndFoot_CF1
    //*[@id="mergedRows"]    mergedRows_A1
    mergedCols               mergedCols_B2
    formattedTable           formattedTable_A1
    formattedTable           formattedTable_B1
    formattedTable           formattedTable_C1
    formattedTable           formattedTable_D1
    formattedTable           formattedTable_A2
    formattedTable           formattedTable_B2
    formattedTable           formattedTable_ÄÖÜäöüß
    formattedTable           äöü€&äöü€&

Should Give Error Message When Content Not Found In Table
    Run Keyword And Expect Error
    ...    Table 'simpleTable' did not contain text 'Not here'.
    ...    Table Should Contain    simpleTable    Not here
