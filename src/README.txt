SeleniumLibrary source
======================

The source is organized under one module 'SeleniumLibrary'.
It has three files::

__init__.py
	This files contains the actual SeleniumLibrary code
selenium.py 
	Is the selenium-client driver python implementation.
xpath_converter.py
	Contains a functions that converts an attribute dictionary
	to an xpath expression. This attribute dictionary was
	used in an earlier Robot Framework web testing library
	based on PamIE, and is here for backwards compatibility.

'lib' directory contains the selenium-server.jar. 
Currently used version is 1.0-beta.

