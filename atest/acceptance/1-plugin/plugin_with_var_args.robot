*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithVarArgs.py;kw1=Text1;kw2=Text2

*** Test Cases ***
Testing Plugin With Arguments
    ${text} =    Return Var Args As String
    Should Be Equal As Strings    ${text}    start: kw1=Text1, kw2=Text2
