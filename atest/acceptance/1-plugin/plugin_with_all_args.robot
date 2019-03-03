*** Settings ***
Library    SeleniumLibrary    plugins=${CURDIR}/PluginWithAllArgs.py;argument1;varg1;varg2;kw1=kwarg1;kw2=kwarg2

*** Test Cases ***
Testing Plugin With Many Arguments Types
    ${text} =    Return All Args As String
    Should Be Equal As Strings    ${text}     	start: arg=argument1, varg1, varg2, kw1=kwarg1, kw2=kwarg2
