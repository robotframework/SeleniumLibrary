*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithArgs.py;${ARG1};${ARG2},${CURDIR}/MyPlugin.py

*** Variables ***
${ARG1}    Text1
${ARG2}    Text2

*** Test Cases ***
Testing Plugin With Arguments
    ${text1} =    Return Arg1 Arg2 As String
    Should Be Equal As Strings    ${text1}    Text1 Text2
    ${text2} =    New Keyword
    Should Be Equal As Strings    ${text2}    New Keyword
