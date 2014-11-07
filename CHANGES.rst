Release Notes
=============

1.6
---
- Added examples to 'Execute Javascript' and 'Execute Async Javascript'
  keyword documentation.
  [ombre42]

- Added instructions to README.rst on how to manually install Selenium2Library.
  [pekkaklarck]

- Fixed issue where the browser failed to properly register if 'Open Browser'
  did not complete.
  [Mika Batsman][elizaleong][emanlove] 

- Added support for negative indices for rows and columns in table-related
  keywords.
  [eweitz]

- Added strategy for locating elements by partial link text with locator
  prefix 'partial link'.
  [lina1]

- Added new keyword 'Clear Element Text' for clearing the text of text entry 
  elements.
  [emanlove]

- Added new keyword 'Locator Should Match X Times' for validating number of
  times a given locator appears.
  [emanlove]

- Fixed issue where 'Select Window’ with url strategy fails to locate window
  [laulaz]

- Fixed issue where a non-string assigned to window.id caused
  'Select Window' and 'Get Window *' keywords to fail.
  [ombre42]

- Allow using key attributes (default strategy) when the locator contains
  a '=' by using the prefix 'default='. Also make locator prefixes
  space-insensitive.
  [ombre42]

A big thank you to [eweitz] and [HelioGuilherme66] for getting the
continuous integration builds to go green by fixing internal tests.

1.5
---
- Copy Desired Capabilities before modifying to prevent affecting future
  sesions.
  [ombre42]

- Added support for Safari Browser.
  [zmlpjuran]

- Added 'Create Webdriver' to allow greater control of local WebDrivers, such
  as setting a proxy or using Chrome options.
  [ombre42][pekkaklarck][emanlove][j1z0]

- Fixed Mouse Up keyword attempting to click and hold one more time before
  release.
  [myaskevich][emanlove]

- Refixed issue with parsing desired capabilities.
  [cookie314][ymost][emanlove]

- Fixed compatibility with RobotFramework v2.8.1
  [F1ashhimself]

- Modified how internal tests are run and ignore known browser issues.
  [emanlove]

1.4
---
- Added keywords for verifying text entered into textarea elements.
  [stevejefferies][emanlove]

- Fixed bad browser name raising AttributeError.
  [ombre42]

- Raise exception in selecting non-existing item in list. Error handling varies
  between single-select and multi-select lists. See keyword documentation for
  more information.
  [adwu73][emanlove] 

- Added 'Get Window Size' and 'Set Window Size' keywords matching the
  Selenium functionality.
  [emanlove][ombre42]

1.3
---
- Updated expected error messages with async javascript tests.
  [emanlove]

- Beautified README.rst.
  [j1z0][emanlove]
  
- Changed press key test to use Line Feed (\10) instead of
  Carriage Return (\13).
  [emanlove]
 
- Added new keyword 'Click Element At Coordinates'.
  [aaltat][pierreroth64][ombre42][emanlove]

- Added a "Getting Help" section to README.rst.
  [ombre42][emanlove]

- Added keyword 'Wait Until Element Visible'
  [ombre42]

- Perform check on return value when finding elements. Fixes Issue 65.
  [ombre42]

- Support checking enabled/disabled state of option elements.
  [ekantola]

- Allow desired_capabilities= to be a dictionary.
  [peritus]

- Added Android and iPhone browsers.
  [maddabini]

- Added keyword 'Current Frame Should Not Contain'.
  [adwu73]

1.2
---
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
---
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
