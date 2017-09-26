*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Identify Table By CSS
    Table Should Contain    css=table#simpleTable    simpleTable
    Table Header Should Contain    css:table#tableWithTwoHeaders    tableWithTwoHeaders_C2
    Table Footer Should Contain    css=table#withHeadAndFoot    withHeadAndFoot_AF1
    Table Row Should Contain    css=table#mergedRows    1    mergedRows_D1
    Table Column Should Contain    css=table#mergedCols    1    mergedCols_D1
    Table Cell Should Contain    css=table#formattedTable    1    1    formattedTable_A1
    Table Cell Should Contain    css=table#formattedTable    2    4    äöü€&äöü€&
    Table Cell Should Contain    css=h2.someClass ~ table:last-child    2    4    äöü€&äöü€&

Should Identify Table By xpath
    Table Should Contain    xpath://table[@id="simpleTable"]    simpleTable

Should Identify Table By id
    Table Should Contain    id:simpleTable    simpleTable

Should Identify Table By name
    Table Should Contain    name:simpleTable    simpleTable

Should Identify Table By default
    Table Should Contain    simpleTable    simpleTable
