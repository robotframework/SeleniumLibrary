*** Settings ***
Resource        table_resource.robot

*** Test Cases ***
Should Find Text In Header
    [Template]  Table Header Should Contain With CSS And XPath Locators
    tableWithSingleHeader  tableWithSingleHeader_A1
    tableWithSingleHeader  tableWithSingleHeader_B1
    tableWithTwoHeaders  tableWithTwoHeaders_A1
    tableWithTwoHeaders  tableWithTwoHeaders_C2
    withHeadAndFoot  withHeadAndFoot_AH1
    withHeadAndFoot  withHeadAndFoot_CH1
    withHeadAndFoot  withHeadAndFoot_AH2
    withHeadAndFoot  withHeadAndFoot_BH2

Should Give Error Message When Content Not Found In Table Header
    Run Keyword And Expect Error  Header in table identified by 'withHeadAndFoot' should have contained text 'withHeadAndFoot_B2'.  Table Header Should Contain  withHeadAndFoot  withHeadAndFoot_B2

*** Keywords ***
Table Header Should Contain With CSS And XPath Locators
    [Arguments]  ${table id}  ${expected}
    Run Table Keyword With CSS And XPath Locators  Table Header Should Contain  ${table id}  ${expected}

