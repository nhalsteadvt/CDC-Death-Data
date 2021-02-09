@ECHO OFF
color 0a


:START
cls
cd src

ECHO "1. Run from local file"
ECHO "2. Run from JSON API"
ECHO "3. Quit"

set /P op="Enter your choice: "
::echo %op%
IF %op%==3 GOTO Q
IF %op%==2 GOTO api
IF %op%==1 GOTO local

:local
::echo local
py AnalyzeDataFromFile.py
pause
cd ..
GOTO START

:api
::echo api
py AnalyzeDataFromAPI.py
pause
cd ..
GOTO START

:Q
cd ..
::echo "QUIT"
