*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Find Text In Header
    [Template]    Table Header Should Contain
    tableWithSingleHeader       tableWithSingleHeader_A1
    id:tableWithSingleHeader    tableWithSingleHeader_B1
    css:#tableWithTwoHeaders    tableWithTwoHeaders_A1
    tableWithTwoHeaders         tableWithTwoHeaders_C2
    withHeadAndFoot             withHeadAndFoot_AH1
    withHeadAndFoot             withHeadAndFoot_CH1
    withHeadAndFoot             withHeadAndFoot_AH2
    withHeadAndFoot             withHeadAndFoot_BH2

Should Give Error Message When Content Not Found In Table Header
    Run Keyword And Expect Error
    ...    Table 'withHeadAndFoot' header did not contain text 'withHeadAndFoot_B2'.
    ...    Table Header Should Contain    withHeadAndFoot    withHeadAndFoot_B2
