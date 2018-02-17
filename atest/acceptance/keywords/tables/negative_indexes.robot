*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Test negative index for CSS strategy in 'Table Row Should Contain'
    Table Row Should Contain    tableWithSingleHeader
    ...    -1    tableWithSingleHeader_A3 tableWithSingleHeader_B3 tableWithSingleHeader_C3
    Table Row Should Contain    id:tableWithSingleHeader
    ...    -1    tableWithSingleHeader_A3 tableWithSingleHeader_B3 tableWithSingleHeader_C3
    Table Row Should Contain    xpath://*[@id="tableWithSingleHeader"]
    ...    -1    tableWithSingleHeader_A3 tableWithSingleHeader_B3 tableWithSingleHeader_C3

Test negative index for XPath strategy in 'Table Row Should Contain'
    Table Row Should Contain    xpath=//*[@id='tableWithSingleHeader']
    ...    -1    tableWithSingleHeader_A3 tableWithSingleHeader_B3 tableWithSingleHeader_C3

Test negative index for CSS strategy in 'Table Column Should Contain'
    Table Column Should Contain    tableWithSingleHeader
    ...    -1    tableWithSingleHeader_C2

Test negative index for XPath strategy in 'Table Column Should Contain'
    Table Column Should Contain    xpath=//*[@id='tableWithSingleHeader']
    ...    -1    tableWithSingleHeader_C2

Test negative index for XPath strategy in 'Table Cell Should Contain'
    Table Cell Should Contain    simpleTable    -1    -2    simpleTable_B3

Test negative index for CSS strategy in 'Table Cell Should Contain'
    Table Cell Should Contain    xpath=//*[@name='simpleTableName']
    ...    -1    -2    simpleTableName_B3
