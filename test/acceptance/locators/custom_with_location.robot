*** Settings ***
Documentation     Test custom locators
Suite Setup       Go To Page "index.html"
Resource          ../resource.robot

*** Variables ***
&{dt_page_index}    This is more text=css=body > p:nth-child(2)    This is the haystack=xpath=/html/body/p[1]

*** Test Cases ***
Test Custom Locator With Location
    Add Location Strategy    custom1    Keyword To Get Locator By Location And Criteria    ${dt_page_index}    #keyword + location to get locator from dict or remote database
    Page Should Contain Element    custom1=This is the haystack
    Page Should Contain Element    custom1=This is more text
    Add Location Strategy    custom2    \    ${dt_page_index}    #dict[criteria] as locator
    Page Should Contain Element    custom2=This is the haystack
    Page Should Contain Element    custom2=This is more text
    Add Location Strategy    custom3    location=${dt_page_index}    #alernative dict[criteria] as locator
    Page Should Contain Element    custom3=This is the haystack
    Page Should Contain Element    custom3=This is more text
    Remove Location Strategy    custom1
    Remove Location Strategy    custom2
    Remove Location Strategy    custom3

Test Custom Locator Without Location
    Add Location Strategy    uitext    Keyword To Get Web Element By Criteria
    Page Should Contain Element    uitext=This is the haystack
    Page Should Contain Element    uitext=This is more text
    Remove Location Strategy    uitext

*** Keywords ***
Keyword To Get Web Element By Criteria
    [Arguments]    ${browser}    ${criteria}    ${tag}    ${constraints}
    ${webelement_object}    Get Webelement    &{dt_page_index}[${criteria}]
    [Return]    ${webelement_object}

Keyword To Get Locator By Location And Criteria
    [Arguments]    ${location}    ${criteria}
    ${locator}    Set Variable    &{location}[${criteria}]    #location is dict here. could be db source
    [Return]    ${locator}
