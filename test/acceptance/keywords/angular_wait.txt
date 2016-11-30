*** Settings ***
Test Setup      Go To   http://${SERVER}/testapp/#/async
Resource        ../resource.txt

*** Test Cases ***
Waits For Http Calls
    Wait For Angular
    Element Text Should Be  binding=slowHttpStatus  not started

    Click Button  css=[ng-click="slowHttp()"]

    Wait For Angular  timeout=20sec
    Element Text Should Be  binding=slowHttpStatus  done

Waits For Long Javascript Execution
    Wait For Angular
    Element Text Should Be  binding=slowFunctionStatus  not started

    Click Button  css=[ng-click="slowFunction()"]

    Wait For Angular
    Element Text Should Be  binding=slowFunctionStatus  done

DOES NOT wait for timeout
    Wait For Angular
    Element Text Should Be  binding=slowTimeoutStatus  not started

    Click Button  css=[ng-click="slowTimeout()"]

    Wait For Angular
    Element Text Should Be  binding=slowTimeoutStatus  pending...

Waits For $timeout
    Wait For Angular
    Element Text Should Be  binding=slowAngularTimeoutStatus  not started

    Click Button  css=[ng-click="slowAngularTimeout()"]

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowAngularTimeoutStatus  done
    
Waits For $timeout Then A Promise
    Wait For Angular
    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  not started

    Click Button  css=[ng-click="slowAngularTimeoutPromise()"]

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowAngularTimeoutPromiseStatus  done
    
Waits For Long Http Call Then A Promise
    Wait For Angular
    Element Text Should Be  binding=slowHttpPromiseStatus  not started

    Click Button  css=[ng-click="slowHttpPromise()"]

    Wait For Angular  timeout=30sec
    Element Text Should Be  binding=slowHttpPromiseStatus  done

Waits For Slow Routing Changes
    Wait For Angular
    Element Text Should Be  binding=routingChangeStatus  not started

    Click Button  css=[ng-click="routingChange()"]

    Wait For Angular  timeout=30sec
    Page Should Contain  polling mechanism

Waits For Slow Ng-Include Templates To Load
    Wait For Angular
    Element Text Should Be  css=.included  fast template contents

    Click Button  css=[ng-click="changeTemplateUrl()"]

    Wait For Angular  timeout=30sec
    Element Text Should Be  css=.included  slow template contents
