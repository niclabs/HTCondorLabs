@echo off

C:\Python34\Lib\site-packages\PySide\pyside-rcc.exe resource_icon.qrc -o condor_gui_resource_icon.py

pause

:: qrc file
rem <RCC>
rem   <qresource prefix="/" >
rem     <file>icons/icon_condor_gui.ico</file>
rem     <file>icons/icon_condor_gui.png</file>
rem   </qresource>
rem </RCC>

:: icons.py file !!!Important!!!
rem qt_resource_data = b"...
rem qt_resource_name = b"...
rem qt_resource_struct = b"...