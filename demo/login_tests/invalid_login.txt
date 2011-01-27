*** Settings ***

Documentation   A test suite containing tests related to invalid login. These
...             tests are data-driven by they nature. They use a single
...             keyword, specified with Test Template setting, that is called
...             with different arguments to cover different scenarios.
Suite Setup     Open Browser To Login Page
Test Setup      Go To Login Page
Test Template   Login With Invalid Credentials Should Fail
Suite Teardown  Close Browser
Resource        common_resource.txt


*** Test Cases ***              User Name      Password

Invalid Username                invalid        ${VALID PASSWD}
Invalid Password                ${VALID USER}  invalid
Invalid Username And Password   invalid        whatever
Empty Username                  ${EMPTY}       ${VALID PASSWD}
Empty Password                  ${VALID USER}  ${EMPTY}
Empty Username And Password     ${EMPTY}       ${EMPTY}


*** Keywords ***

Login With Invalid Credentials Should Fail
    [Arguments]  ${username}  ${password}
    Input Username  ${username}
    Input Password  ${password}
    Submit Credentials
    Login Should Have Failed
