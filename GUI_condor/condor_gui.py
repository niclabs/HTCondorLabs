#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

import sys
import argparse

from PySide import QtCore, QtGui

import condor_gui_main_window
import condor_gui_version

try:
    import qdarkstyle
except ImportError:
    #print('Package qdarkstyle wasn\'t found.')
    #raise ImportError('<any message you want here>')
    pass


###############################################################################
# Main
###############################################################################
if __name__ == '__main__':

    # Argument parser for options
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                    description='GUI to manage and work with one or more Condor pools.')
    parser.add_argument('-cwd',
                        help='Working directory. If no working directory given \n'
                             'abs. path of the executable is used or current working directory.')
    parser.add_argument('-v', action='version', version=condor_gui_version.__version__)
    args = parser.parse_args()

    # Optional working directory
    cwd = args.cwd

    #
    # Create the application
    #
    app = QtGui.QApplication(sys.argv)

    # qdarkstyle, optional stylesheet
    try:
        app.setStyleSheet(qdarkstyle.load_stylesheet())
    except NameError:
        pass

    # Gui: Construct the MainWindow and run it.

    #mainWindow = condor_gui_main_window.MainWindow(startFile=startFile)
    mainWindow = condor_gui_main_window.MainWindow(cwd=cwd)

    mainWindow.show()
    sys.exit(app.exec_())
