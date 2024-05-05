*** Settings ***
Resource    ../variables.robot

*** Keywords ***
Go To Page "${relative url}"
    [Documentation]    Goes to page
    Go To    ${ROOT}/${relative url}
