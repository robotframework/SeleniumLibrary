*** Settings ***
Documentation    Suite description
Suite Setup       Go To Page "non_ascii.html"
Resource          ../resource.robot

*** Test Cases ***
Print Page As PDF Without Print Options
    Print Page As PDF

#Provide Print Options From Module
#    # ${print_options}=  Evaluate  sys.modules['selenium.webdriver'].common.print_page_options()  sys, selenium.webdriver
#    ${print_options}=  Evaluate  selenium.webdriver.common.print_page_options.PrintOptions()
#    # Set To Dictionary    ${print_options}  scale  0.5
#    # Evaluate    ${print_options}.scale=0.5
#    # Set Variable    ${print_options.scale}  0.5
#    # Evaluate    ${print_options.scale}=0.5
#    Evaluate    setattr($print_options, 'scale', 0.5)
#    Print Page As PDF    ${print_options}
