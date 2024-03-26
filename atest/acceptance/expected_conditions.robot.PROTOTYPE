*** Test Cases ***
# Wait Until Element State Is (Not)
# Get Element State
# Element States Should (Not) Be

Check waiting for condition that takes a element
   Fail

Check waiting for condition that takes a title
   Fail

Check waiting for condition that takes a url
   Fail
   Wait Until    url contains   google
   # verify took 2 seconds

Check waiting for condition that takes locator and string
   Wait Until Element State Is     ${condition}    ${locator}   ${string}
   Wait Until Element State Is     ${condition}    ${element}
   Wait Until Condition Is         ${condition}    ${target}
   Wait Until Condition Is         ${condition}    ${whatelse you need for this condition}


   Wait Until State Is         number_of_windows_to_be
   Wait Until Expected Condition Is         number_of_windows_to_be
   Wait Until Condition Is     number of windows to be   5
   Wait Until Condition Is     text to be present in element attribute    //some/xpath/to/an/element  href  http://hello

   Wait Until Condition Is     number of windows to be   5    text to be present in element attribute    //some/xpath/to/an/element  href  http://hello

   Wait Until    number of windows to be   5
   Wait Until    text to be present in element attribute    //some/xpath/to/an/element  href  http://hello   
   Get Condition
   Is       number of windows to be   5