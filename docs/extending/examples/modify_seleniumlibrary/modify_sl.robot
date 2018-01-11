*** Settings ***
Library           SeleniumLibrary
Library           ./NewKeywords.py

*** Test Cases ***
Use New Keywords From SeleniumLibrary
    SeleniumLibrary.Open Browser     google
    ${capabilities} =    SeleniumLibrary.Get Browser Desired Capabilities
    Log    ${capabilities}
    [Teardown]    Close Browser
