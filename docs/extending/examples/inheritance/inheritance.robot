*** Settings ***
Library           ./InheritSeleniumLibrary.py

*** Test Cases ***
Use InheritSeleniumLibrary Open Browser Keyword
    Open Browser     google
    ${capabilities} =    Get Browser Desired Capabilities
    Log    ${capabilities}
    [Teardown]    Close Browser