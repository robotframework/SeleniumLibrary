*** Settings ***
Suite Teardown    Close All Browsers
Library           ../resources/testlibs/get_driver_path.py
Resource          resource.robot
# Force Tags        Known Issue Firefox    Known Issue Safari    Known Issue Internet Explorer
Documentation     Creating test which would work on all browser is not possible.
...    These tests are for Chrome only.

*** Test Cases ***
Chrome Browser With Chrome Service As String
    [Documentation]
    ...    LOG 2:3 DEBUG STARTS: Started executable:
    ...    LOG 2:4 DEBUG GLOB:    POST*/session*
    ${driver_path}=  Get Driver Path    Chrome
    Open Browser    ${FRONT PAGE}    Chrome    remote_url=${REMOTE_URL}
    ...    service=executable_path='${driver_path}'
 
Chrome Browser With Chrome Service As String With service_args As List
    Open Browser    ${FRONT PAGE}    Chrome    remote_url=${REMOTE_URL}
    ...    service=service_args=['--append-log', '--readable-timestamp']; log_output='${OUTPUT_DIR}/chromedriverlog.txt'
    File Should Exist    ${OUTPUT_DIR}/chromedriverlog.txt
    # ...    service=service_args=['--append-log', '--readable-timestamp']; log_output='./'
    # ...    service=service_args=['--append-log', '--readable-timestamp']

Firefox Browser With Firefox Service As String
    [Documentation]
    ...    LOG 2:3 DEBUG STARTS: Started executable:
    ...    LOG 2:4 DEBUG GLOB:    POST*/session*
    ${driver_path}=  Get Driver Path    Firefox
    Open Browser    ${FRONT PAGE}    Firefox    remote_url=${REMOTE_URL}
    ...    service=executable_path='${driver_path}'

#Chrome Browser With Selenium Options Invalid Method
#    Run Keyword And Expect Error     AttributeError: 'Options' object has no attribute 'not_here_method'
#    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
#    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=not_here_method("arg1")
#
#
#Chrome Browser With Selenium Options Argument With Semicolon
#    [Documentation]
#    ...    LOG 1:14 DEBUG GLOB: *"goog:chromeOptions"*
#    ...    LOG 1:14 DEBUG GLOB: *["has;semicolon"*
#    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
#    ...    desired_capabilities=${DESIRED_CAPABILITIES}    options=add_argument("has;semicolon")
