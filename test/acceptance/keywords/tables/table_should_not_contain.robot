*** Settings ***
Documentation     Tests table contents for should not keyowrds
Resource          table_resource.robot
Default Tags  table_not_contain


*** Test Cases ***
Should Give Error Message When Content Found In Table
    [Documentation]    Should Give Error Message When Content Found In Table
    [Template]    Verify Table Does Contain With CSS And XPath Locators
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

Test Table Cell Should Not Contain
    [Documentation]    Test Table Cell Should Not Contain
    ${table}=    set variable    simpleTable
    ${row}=    set variable    1
    ${col}=    set variable    1
    ${expected} =    set variable    simpleTable_A2
    table cell should not contain    ${table}    ${row}    ${col}    ${expected}

Test Table Cell Give Error When It Contains
    [Documentation]    Test Table Cell Give Error When It Contains
    ${table}=    set variable    simpleTable
    ${row}=    set variable    1
    ${col}=    set variable    1
    ${expected} =    set variable    simpleTable_A1
    ${err}=    Set Variable    Cell in table '${table}' in row #${row} and column #${col} should not have contained text '${expected}'.
    Run Keyword And Expect Error    ${err}    table cell should not contain    ${table}    ${row}    ${col}    ${expected}

Test Table Row Should Not Contain
    [Documentation]    Test Table Row Should Not Contain
    ${table}=    set variable    simpleTable
    ${row}=    set variable    1
    ${expected} =    set variable    simpleTable_A2
    table row should not contain    ${table}    ${row}      ${expected}

Test Table Row Should Give Error When It Contains
    [Documentation]    Test Table Row Should Give Error When It Contains
    ${table}=    set variable    tableWithSingleHeader
    ${expected} =    set variable    tableWithSingleHeader_A1
    ${row}=    set variable    1
    ${err}=    Set Variable    Row #${row} in table identified by '${table}' should have contained text '${expected}'.
    run keyword and expect error  ${err}    table row should not contain  ${table}    ${row}    ${expected}

Test Table column Should Not Contain
    [Documentation]    Test Table column Should Not Contain
    ${table}=    set variable    simpleTable
    ${column}=    set variable    1
    ${expected} =    set variable    simpleTable_B2
    table column should not contain    ${table}    ${column}      ${expected}

Test Table column Should Give Error When It Contains
    [Documentation]    Test Table column Should Give Error When It Contains
    ${table}=    set variable    tableWithSingleHeader
    ${column}=    set variable    1
    ${expected} =    set variable    tableWithSingleHeader_A1
    ${err}=    Set Variable    Column #${column} in table identified by '${table}' should not have contained text '${expected}'.
    run keyword and expect error  ${err}    table column should not contain  ${table}    ${column}      ${expected}

Test Table Header Should Not Contain
    [Documentation]    Test Table Header Should Not Contain
    ${table}=    set variable    tableWithSingleHeader
    ${expected} =    set variable    tableWithSingleHeader_A3
    table header should not contain  ${table}    ${expected}

Test Table Header Should Give Error When It Contains
    [Documentation]    Test Table Header Should Give Error When It Contains
    ${table}=    set variable    tableWithSingleHeader
    ${expected} =    set variable    tableWithSingleHeader_A1
    ${err}=    Set Variable    Header in table identified by '${table}' should not have contained text '${expected}'.
    run keyword and expect error  ${err}    table header should not contain  ${table}    ${expected}

Test Table Footer Should Not Contain
    [Documentation]    Test Table Footer Should Not Contain
    ${table}=    set variable    withHeadAndFoot
    ${expected} =    set variable    withHeadAndFoot_A1
    table footer should not contain    ${table}    ${expected}

Test Table Footer Should Give Error When It Contains
    [Documentation]    Test Table Footer Should Give Error When It Contains
    ${table}=    set variable    withHeadAndFoot
    ${expected} =    set variable    withHeadAndFoot_AF1
    ${err}=    Set Variable    Footer in table identified by '${table}' should not have contained text '${expected}'.
    run keyword and expect error  ${err}    table footer should not contain    ${table}    ${expected}


*** Keywords ***
Verify Table Does Contain With CSS And XPath Locators
    [Arguments]    ${locator}    ${expected}
    [Documentation]    Verify Table Contains With CSS And XPath Locators
    ${err}=    Set Variable    Table identified by '${locator}' should not have contained text '${expected}'.
    Run Keyword And Expect Error    ${err}    Table Should Not Contain    ${locator}    ${expected}
