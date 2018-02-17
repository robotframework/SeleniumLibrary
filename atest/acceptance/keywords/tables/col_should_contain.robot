*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Find Text In Specific Column
    [Template]    Table Column Should Contain
    simpleTable              2    simpleTable_B2
    id:simpleTable          -2    simpleTable_B2
    simpleWithNested         2    nestedTable_A1
    css:#nestedTable         3    nestedTable_C1
    nestedTable             -1    nestedTable_C1
    tableWithSingleHeader    1    tableWithSingleHeader_A1
    tableWithSingleHeader    1    tableWithSingleHeader_A3
    tableWithTwoHeaders      2    tableWithTwoHeaders_B2

Mixed th and td
    [Template]    Table Column Should Contain
    mixed-th-td              1    1.1 (th)
    id:mixed-th-td           1    2.1 (td)
    css:#mixed-th-td         2    1.2 (td)
    //*[@id="mixed-th-td"]   2    2.2 (th)
    mixed-th-td              3    2.3 (td)
    mixed-th-td              3    3.3 (th)
    mixed-th-td             -2    1.2 (td)
    mixed-th-td             -2    2.2 (th)
    mixed-th-td             -3    1.1 (th)
    mixed-th-td             -3    2.1 (td)

Should Give Error Message When Content Not Found In Table Column
    Run Keyword And Expect Error
    ...    Table 'id:simpleTable' column 2 did not contain text 'simpleTable_C3'.
    ...    Table Column Should Contain    id:simpleTable    2    simpleTable_C3

Should Give Error Message When Column Number Out Of Bounds
    Run Keyword And Expect Error
    ...    Table '//*[@id="simpleTable"]' column 20 did not contain text 'simpleTable_B3'.
    ...    Table Column Should Contain    //*[@id="simpleTable"]    20    simpleTable_B3

Zero is invalid column index
    Run Keyword And Expect Error
    ...    ValueError: Row and column indexes must be non-zero.
    ...    Table Column Should Contain    simpleTable    0    xxx
