*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithArgs.py;Text1;Text2,${CURDIR}/MyPlugin.py

*** Test Cases ***
Testing Plugin With Arguments
    ${text} =    Return Arg1 Arg2 As String
    Should Be Equal As Strings    ${text}    Text1 Text2
