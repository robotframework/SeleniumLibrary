*** Settings ***
Documentation     Simple test for fullpage screenshot
Library           SeleniumLibrary
Library           OperatingSystem

*** Test Cases ***
Test Fullpage Screenshot
    Open Browser    https://www.google.com    firefox
    Maximize Browser Window
    Capture Fullpage Screenshot    test-fullpage.png
    File Should Exist    test-fullpage.png
    Close Browser
