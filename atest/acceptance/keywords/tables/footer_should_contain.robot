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

Should Give Error Message When Content Not Found In Table Footer But Is Other Table
    Run Keyword And Expect Error
    ...    Table 'tableWithSingleHeader' footer did not contain text 'SimpleWithHeadAndFoot_CF1'.
    ...    Table Footer Should Contain    tableWithSingleHeader    SimpleWithHeadAndFoot_CF1

Should Find Text In Footer Header Cell
    Table Footer Should Contain    footer-with-header-cell    Total

Should Find Text In Footer Data Cell
    Table Footer Should Contain    footer-with-header-cell    100 USD

Should Not Find Header Text Outside Footer
    Run Keyword And Expect Error
    ...    Table 'footer-with-header-cell' footer did not contain text 'Amount'.
    ...    Table Footer Should Contain    footer-with-header-cell    Amount

Should Not Find Body Header Text Outside Footer
    Run Keyword And Expect Error
    ...    Table 'footer-with-header-cell' footer did not contain text 'Books'.
    ...    Table Footer Should Contain    footer-with-header-cell    Books

Should Not Find Footer Header Text In Another Table
    Run Keyword And Expect Error
    ...    Table 'withHeadAndFoot' footer did not contain text 'Total'.
    ...    Table Footer Should Contain    withHeadAndFoot    Total