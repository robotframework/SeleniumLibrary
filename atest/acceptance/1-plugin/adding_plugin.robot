*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/MyPlugin.py

*** Test Cases ***
Adding New Keyword From Class
    ${text} =    New Keyword
    Should Be Equal    ${text}    New Keyword

Overwriting Exsisting Keyword
    ${text} =    Open Browser     text is returned
    Should Be Equal    ${text}    text is returned

Oerwriting ElementFinder
    ${element} =    Get WebElement    //div
    Should Be Equal    ${element}    Dummy find
