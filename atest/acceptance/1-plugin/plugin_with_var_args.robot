*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithVarArgs.py;Text1;Text2;Text3

*** Test Cases ***
Testing Plugin With Variable Number Of Arguments
    ${text} =    Return Var Args As String
    Should Be Equal As Strings    ${text}    start: Text1, Text2, Text3
