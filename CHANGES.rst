Release Notes
=============

1.1 (unreleased)
----------------
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
