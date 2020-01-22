*** Settings ***
Suite Teardown    Close All Browsers
Library           ../resources/testlibs/get_selenium_options.py
Resource          resource.robot
Documentation     Creating test which would work on all browser is not possible. When testing with other
...    browser than Chrome it is OK that these test will fail. SeleniumLibrary CI is run with Chrome only
...    and therefore there is tests for Chrome only.
...    Also it is hard to create where chromedriver location would suite in all os and enviroments, therefore
...    there is a test which tests error scenario and other scenarios needed manual or unit level tests

*** Test Cases ***
Chrome Browser With executable_path Argument
    [Tags]    NoGrid
    Run Keyword And Expect Error
    ...    WebDriverException: Message: 'exist' executable needs to be in PATH.*
    ...    Open Browser    ${FRONT PAGE}    ${BROWSER}    remote_url=${REMOTE_URL}
    ...    desired_capabilities=${DESIRED_CAPABILITIES}    executable_path=/does/not/exist
