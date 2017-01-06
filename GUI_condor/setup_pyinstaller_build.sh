#!/bin/bash

# PyInstaller 3.0 is required

pyinstaller --onefile \
            --windowed \
            condor_gui.py
