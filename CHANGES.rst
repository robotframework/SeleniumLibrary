Release Notes
=============

1.2 (unreleased)
----------------
- Added PhantomJS as a supported browser type.
  [bmannix]

- Fixed 'Get Selected List Label' under IE7 or IE8.
  [ombre42]

- Added support for jQuery and sizzle selectors.
  [Paul Hicks (tenwit)][peritus][j1z0]

- Added new global variable DEFAULT_HOST to demo server for more easier
  way to bind to other address than 'localhost'.
  [IsNoGood]

- Skip closed browsers when setting Selenium timeout. Fixes #93.
  [ombre42]

1.1
----------------
- Increased minimum version requirement for Selenium to 2.12.0 within
  setup.py.  This is required due to the change towards using Selenium's
  Select class which was introduced starting in version 2.12.
  [emanlove]

- Use Selenium's Select class within Selenium2Library's "Select *" keywords.
  Optimization of certain "Select *" keywords to increase performance. 
  [emanlove] [schminitz]

- Replace maximize current browser window from JS to webdriver.
  [jollychang]

- Verify element is found under 'Get Text' and 'Element Should Contain'
  keywords before returning text or verifing element contains specified text.
  [emanlove]

- Fixed capture page screenshot for RemoteWebDriver.
  [korda]

- Fixed issue with select window under IE. Also addresses issue with Firefox
  when using selenum 2.25.0
  (see http://code.google.com/p/selenium/issues/detail?id=4375).
  [adwu73]

- Added iframe support by removing strict filtering for only <frame> elements.
  [emanlove]

- Added the 'get text' keyword to be backwards compatible with the original
  Selenium Library.
  [jouk0]

- Added drag and drop support with two functions `drag and drop  source
  target` and `drag and drop by offset  source  xoffset  yoffset`
  [mamathanag] and [j1z0]

- Added HTMLUnit and HTMLUnitWithJS support.  Just use a line like:
 `Open Browser    [initial page url]    remote_url=[the selenium-server url]    browser=htmlunit`
  [SoCalLongboard]

1.0.1
-----
- Support for Robot Framework 2.7
- Improvements to distribution build script and improved documentation
