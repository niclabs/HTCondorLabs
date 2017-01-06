@echo off

:: PyInstaller 3.0 is required

rem pyinstaller.exe --onefile --icon=icon_Condor_GUI.ico condor_gui.py
pyinstaller.exe --onefile ^
                --windowed ^
                --icon=icon_condor_gui.ico ^
                --distpath=./bin_win ^
                condor_gui.py

pause

::
rem --onefile is used to package everything into a single executable. If you do not specify this option, the libraries, etc. will be distributed as separate files alongside the main executable.
rem --windowed prevents a console window from being displayed when the application is run. If you�re releasing a non-graphical application (i.e. a console application), you do not need to use this option.
rem --icon=app.ico app.py
rem --name  alternative executable name

rem --distpath=DIR Where to put the bundled app (default: ./dist)
rem --workpath=WORKPATH
rem --version-file=FILE

