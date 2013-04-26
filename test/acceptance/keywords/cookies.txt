*Setting*
Resource  ../resource.txt
Suite Setup  Run Keywords  Add Cookies  Go To Page "index.html"
Suite Teardown  Delete All Cookies


*Test Cases*

Get Cookies
  ${cookies} =  Get Cookies
  Should Be Equal  ${cookies}  test=seleniumlibrary; another=value

Get Cookie Value
  ${value} =  Get Cookie Value  another
  Should Be Equal  ${value}  value

Delete Cookie
  Delete Cookie  test
  ${cookies} =  Get Cookies
  Should Be Equal  ${cookies}  another=value

*Keyword*

Add Cookies
    Delete All Cookies
    Add Cookie  test    seleniumlibrary
    Add Cookie  another     value

