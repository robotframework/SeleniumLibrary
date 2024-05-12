*** Settings ***
Documentation    Suite description
Suite Setup       Go To Page "non_ascii.html"
Resource          ../resource.robot

Test Setup    Remove Files    ${OUTPUTDIR}/selenium-page-*.pdf

*** Test Cases ***
Print Page As PDF Without Print Options
    Print Page As PDF

Verify Index Increments With Multiple Prints
    [Setup]    Remove Files    ${OUTPUTDIR}/selenium-page-*.pdf
    ${file_1} =    Print Page As PDF
    Should Be Equal    ${file_1}    ${OUTPUTDIR}${/}selenium-page-1.pdf
    ${file_2} =    Print Page As PDF
    Should Be Equal    ${file_2}    ${OUTPUTDIR}${/}selenium-page-2.pdf
    ${file_3} =    Print Page As PDF
    Should Be Equal    ${file_3}    ${OUTPUTDIR}${/}selenium-page-3.pdf

Print With Full Options
    Print Page As PDF  page_ranges=['1']  background=${False}  shrink_to_fit=${False}  orientation=portrait
    ...  margin_top=${0.5}  margin_left=${1.5}  margin_bottom=${0.5}  margin_right=${1.5}
    ...  page_height=${35.56}  page_width=${21.59}

#Provide Print Options From Module
#    # ${print_options}=  Evaluate  sys.modules['selenium.webdriver'].common.print_page_options()  sys, selenium.webdriver
#    ${print_options}=  Evaluate  selenium.webdriver.common.print_page_options.PrintOptions()
#    # Set To Dictionary    ${print_options}  scale  0.5
#    # Evaluate    ${print_options}.scale=0.5
#    # Set Variable    ${print_options.scale}  0.5
#    # Evaluate    ${print_options.scale}=0.5
#    Evaluate    setattr($print_options, 'scale', 0.5)
#    Print Page As PDF    ${print_options}
