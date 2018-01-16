*** Settings ***
Library           SeleniumLibrary
Library           ./GetSeleniumLibraryInstance.py

*** Test Cases ***
Use InheritSeleniumLibrary Open Browser Keyword
    GetSeleniumLibraryInstance.Open Browser     google
    ${capabilities} =    GetSeleniumLibraryInstance.Get Browser Desired Capabilities
    Log    ${capabilities}
    [Teardown]    Close Browser