*** Settings ***
Library    SeleniumLibrary    external_modules=${CURDIR}/MyLib.py

*** Test Cases ***
Adding New Keyword From Class
    ${text} =    New Keyword
    Should Be Equal    ${text}    New Keyword

Overwriting Exsisting Keyword
    ${text} =    Open Browser     text is returned
    Should Be Equal    ${text}    text is returned
