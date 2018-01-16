*** Settings ***
Library           ./Decomposition.py

*** Test Cases ***
Decomposition Example
    Open Browser     google
    ${capabilities} =    Get Browser Desired Capabilities
    Log    ${capabilities}
    [Teardown]    Close Browser
