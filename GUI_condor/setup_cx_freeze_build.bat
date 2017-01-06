@echo off

:: build
python setup_cx_freeze.py build > setup_cx_freeze.log

:: binary installer
rem python setup.py bdist_msi

:: for mac
rem python setup.py bdist_dmg

pause