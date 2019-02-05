*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithKwArgs.py;kw1=Text1;kw2=Text2

*** Test Cases ***
Testing Plugin With Keyword Arguments
    ${text} =    Return Kw Args As String
    Should Be Equal As Strings    ${text}    start: kw1=Text1, kw2=Text2
