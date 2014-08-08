*** Settings ***
Resource        table_resource.robot

*** Test Cases ***
Should Find Text In Footer
    [Template]  Table Footer Should Contain With CSS And XPath Locators
    withHeadAndFoot  withHeadAndFoot_AF1
    withHeadAndFoot  withHeadAndFoot_CF1
    withHeadAndFoot  withHeadAndFoot_AF2
    withHeadAndFoot  withHeadAndFoot_CF2

Should Give Error Message When Content Not Found In Table Footer
    Run Keyword And Expect Error  Footer in table identified by 'withHeadAndFoot' should have contained text 'withHeadAndFoot_B2'.  Table Footer Should Contain  withHeadAndFoot  withHeadAndFoot_B2

*** Keywords ***
Table Footer Should Contain With CSS And XPath Locators
    [Arguments]  ${tableId}  ${content}
    Run Table Keyword With CSS And XPath Locators  Table Footer Should Contain  ${table id}  ${content}

