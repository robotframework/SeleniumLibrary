*** Settings ***
Resource          table_resource.robot

*** Test Cases ***
Should Find Text In Footer
    [Template]    Table Footer Should Contain
    withHeadAndFoot         withHeadAndFoot_AF1
    id:withHeadAndFoot      withHeadAndFoot_CF1
    css:#withHeadAndFoot    withHeadAndFoot_AF2
    withHeadAndFoot         withHeadAndFoot_CF2

Should Give Error Message When Content Not Found In Table Footer
    Run Keyword And Expect Error
    ...    Table 'withHeadAndFoot' footer did not contain text 'withHeadAndFoot_B2'.
    ...    Table Footer Should Contain    withHeadAndFoot    withHeadAndFoot_B2
