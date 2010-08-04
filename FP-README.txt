Clone necessary dependencies:
git clone http://github.com/admc/flex-pilot.git

Compile:
~/Devel/flex/my$
../sdk3/bin/mxmlc -source-path=. -source-path+=../flex-pilot/src/ Hello.mxml

Start HTTP server:
~/Devel/flex/my$
python -m SimpleHTTPServer

Start Selenium server:
~/Devel/seleniumlibrary/src/SeleniumLibrary/lib$
java -jar selenium-server.jar -userExtensions user-extensions.js

Run tests:
~/Devel/flex/my$
PYTHONPATH=../../seleniumlibrary/src/ pybot RF.txt
