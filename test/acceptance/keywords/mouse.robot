*** Settings ***
Test Setup      Go To Page "mouse/index.html"
Resource        ../resource.robot

*** Test Cases ***
Mouse Over
    [TAGS]  Known Issue - Firefox
    Mouse Over  el_for_mouseover
    Textfield Value Should Be  el_for_mouseover  mouseover el_for_mouseover
    Run Keyword And Expect Error  ERROR: Element not_there not found.  Mouse Over  not_there

Mouse Out
    [TAGS]  Known Issue - Firefox
    Mouse Out  el_for_mouseout
    Textfield Value Should Be  el_for_mouseout  mouseout el_for_mouseout
    Run Keyword And Expect Error  ERROR: Element not_there not found.  Mouse Out  not_there

Mouse Down
    [TAGS]  Known Issue - Firefox
    Mouse Down  el_for_mousedown
    Textfield Value Should Be  el_for_mousedown  mousedown el_for_mousedown
    Run Keyword And Expect Error  ERROR: Element not_there not found.  Mouse Down  not_there

Mouse Up
    [TAGS]  Known Issue - Firefox
    Mouse Up  el_for_mouseup
    Textfield Value Should Be  el_for_mouseup  mouseup el_for_mouseup
    Run Keyword And Expect Error  ERROR: Element not_there not found.  Mouse Up  not_there

Focus
    Focus  el_for_focus
    Textfield Value Should Be  el_for_focus  focus el_for_focus

Simulate
    Simulate  el_for_blur  blur
    Textfield Value Should Be  el_for_blur  blur el_for_blur
