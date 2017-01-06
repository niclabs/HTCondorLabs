#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

import os
import sys
import subprocess

from PySide import QtCore, QtGui

import condor_gui_syntax_highlighting

"""
A text editor window which can be used to edit the condor_config.
"""


###############################################################################
###############################################################################
class EditCondorConfigWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):

        super(EditCondorConfigWindow, self).__init__(parent)

        # variables
        self.condor_dir = self.getCondorDir()
        self.filename = None

        if self.condor_dir is not None:
            self.configFile = os.path.join(self.condor_dir, 'condor_config')
            self.setWindowTitle('Edit ' + self.configFile)
        else:
            self.setWindowTitle('Edit condor_config')
            self.configFile = 'condor_config'

        self.setWindowIcon(QtGui.QIcon(':/icon_condor_gui.png'))

        # Size
        self.setMinimumWidth(700)
        self.setMinimumHeight(300)
        self.setGeometry(100,100,700,800)

        self.EditIndatWidget = QtGui.QWidget()
        self.setCentralWidget(self.EditIndatWidget)
        self.mainLayout = QtGui.QVBoxLayout(self.EditIndatWidget)
        self.mainLayout.setContentsMargins(0,0,0,0)

        # Textedit
        self.textedit = QtGui.QTextEdit(self) # for typing in
        self.textedit.setUndoRedoEnabled(True)

        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setPointSize(9)
        self.textedit.setFont(font)

        # Syntax highlighting
        condor_gui_syntax_highlighting.SyntaxHighlighter(self.textedit.document())

        self.mainLayout.addWidget(self.textedit)
        self.setLayout(self.mainLayout)

        # Undo and Redo
        self.undoAction = QtGui.QAction('Undo',self)
        self.undoAction.setShortcut('Ctrl+Z')
        self.undoAction.triggered.connect(self.textedit.undo)

        self.redoAction = QtGui.QAction('Redo',self)
        self.redoAction.setShortcut('Ctrl+Y')
        self.redoAction.triggered.connect(self.textedit.redo)

        self.cutAction = QtGui.QAction('Cut',self)
        self.cutAction.setShortcut('Ctrl+X')
        self.cutAction.triggered.connect(self.textedit.cut)

        self.copyAction = QtGui.QAction('Copy',self)
        self.copyAction.setShortcut('Ctrl+C')
        self.copyAction.triggered.connect(self.textedit.copy)

        self.pasteAction = QtGui.QAction('Paste',self)
        self.pasteAction.setShortcut('Ctrl+V')
        self.pasteAction.triggered.connect(self.textedit.paste)

        # Create menu bar
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(QtGui.QAction('&Open...', self, shortcut='Ctrl+O', triggered=self.open), toolTip='Hilfe', StatusTip='NOA Hilfe')
        fileMenu.addAction(QtGui.QAction('&Save', self, shortcut='Ctrl+S', triggered= self.save))
        fileMenu.addAction(QtGui.QAction('Save As...', self, triggered=self.saveAs))
        fileMenu.addAction(QtGui.QAction('&Quit...', self, shortcut='Ctrl+Q', triggered=self.close))

        # Menu Edit
        editMenu = self.menuBar().addMenu('&Edit')
        editMenu.addAction(self.undoAction)
        editMenu.addAction(self.redoAction)
        editMenu.addAction(self.cutAction)
        editMenu.addAction(self.copyAction)
        editMenu.addAction(self.pasteAction)

        # Condor Edit
        condorMenu = self.menuBar().addMenu('&Condor')
        condorMenu.addAction(QtGui.QAction('Reconfig', self, triggered=self.condorReconfig))
        condorMenu.addAction(QtGui.QAction('Restart', self, triggered=self.condorRestart))

        # open condor_config automatically
        self.openFileAutomatically()

        # Signals
        self.textedit.textChanged.connect(self.setUndoStack)

    def getCondorDir(self):
        """
        Return path of condor, windows extracted from Path variable, linux= etc/condor
        """

        # Windows
        if sys.platform == 'win32':

            # get Path variable
            path = os.environ.get('Path')
            condor_dir = None

            # no Path variable
            if path is None:
                return None
            else:
                path = path.split(';')
                # print(path)

                list_condor_dir = []
                for i in path:
                    if 'condor' in i:
                        list_condor_dir.append(i)
                # print(list_condor_dir)

                for i in list_condor_dir:
                    if 'condor\\bin' in i:
                        condor_dir = i[:-4]
                    else:
                        pass

                #print(condor_dir)
                return condor_dir

        # Linux
        elif sys.platform == 'linux':
            #print('linux')
            condor_dir = os.path.join('/etc', 'condor')
            return condor_dir

        else:
            QtGui.QMessageBox.warning(self, 'Help',
                                      'Platform ist not supported.',
                                      QtGui.QMessageBox.Ok)

    def openFileAutomatically(self):
        """
        Opens condor_config automatically.
        """
        #print(self.configFile)
        self.undostackIsClean = True

        if os.path.isfile(self.configFile):
            self.filename = self.configFile
            #print(self.filename)

            with open(self.configFile,'r') as file:
                self.textedit.setText(file.read())

        else:
            self.textedit.setText('Couldn\'t find condor_config. Please open manually.')
            self.filename = None
            self.setWindowTitle('Edit')

    def setUndoStack(self):
        """
        Selfmade undostack when text in textedit changed.
        """
        #print('setUndoStack')
        self.undostackIsClean = False
        #print('undostackIsClean',self.undostackIsClean)
        #self.setWindowTitle('Edit indat.txt*')

        if self.filename:
            #print('If',self.filename)
            self.setWindowTitle('Edit ' + self.filename + '*')

        else:
            #print('Else',self.filename)
            self.setWindowTitle('Edit*')

    def open(self):
        """
        Opens condor_config by file dialog.
        """
        self.filename, throwaway = QtGui.QFileDialog.getOpenFileName(self, caption='Open Condor Config', filter='condor_config', dir='C:\\')

        if self.filename:
            self.indatFile = self.filename
            with open(self.filename,'r') as file:
                self.textedit.setText(file.read())

        # Cleaning undostack and windowtitle
        self.undostackIsClean = True
        #print('undostackIsClean',self.undostackIsClean)
        self.setWindowTitle('Edit ' + self.filename)

    def save(self):
        """
        Save indat.txt.
        """
        if self.filename:

            # Windows
            if sys.platform == 'win32':

                # Save file
                with open(self.filename, 'wt') as file:
                    file.write(self.textedit.toPlainText())

            # Linux
            elif sys.platform == 'linux':
                tmp_file = '/tmp/condor_config_tmp'

                # Save file temporarily
                with open(tmp_file, 'wt') as file:
                    file.write(self.textedit.toPlainText())

                # Check package gksu for graphical password request
                devnull = open(os.devnull, 'w')
                retval = subprocess.call(['dpkg', '-s', 'gksu'], stdout=devnull, stderr=subprocess.STDOUT)
                devnull.close()

                if retval == 0:
                    # Move temp file to right location
                    os.system('gksu mv ' + tmp_file + ' ' + os.path.join(self.condor_dir, 'condor_config'))

                else:
                    QtGui.QMessageBox.warning(self, 'Edit Config File',
                                              'Package \'gksu\' isn\'t installed.\n' +
                                              'This package is needed to provide root permissions.\n' +
                                              'Please install the package or move the file\n' +
                                              tmp_file + ' manually to\n' +
                                              os.path.join(self.condor_dir, 'condor_config'),
                                              QtGui.QMessageBox.Ok)
                    return

            else:
                QtGui.QMessageBox.warning(self, 'Help',
                                          'Platform ist not supported.',
                                          QtGui.QMessageBox.Ok)
                return

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            #print('undostackIsClean',self.undostackIsClean)
            self.setWindowTitle('Edit ' + self.filename)

        else:
            self.saveAs()
            pass

    def saveAs(self):
        """
        Saves indat.txt to a different directory pulled out of a file dialog.
        """
        # keep old filename
        self.filename_old = self.filename

        self.filename, throwaway = QtGui.QFileDialog.getSaveFileName(self, caption='Save Condor Config As', filter='condor_config', dir=self.condor_dir)

        if not self.filename:
            self.filename = self.filename_old
            return

        # Windows
        if sys.platform == 'win32':

            # Save file
            with open(self.filename, 'wt') as file:
                file.write(self.textedit.toPlainText())

        # Linux
        elif sys.platform == 'linux':
            tmp_file = '/tmp/condor_config_tmp'

            # Save file temporarily
            with open(tmp_file, 'wt') as file:
                file.write(self.textedit.toPlainText())

            # Check package gksu for graphical password request
            devnull = open(os.devnull, 'w')
            retval = subprocess.call(['dpkg', '-s', 'gksu'], stdout=devnull, stderr=subprocess.STDOUT)
            devnull.close()

            if retval == 0:
                # Move temp file to right location
                os.system('gksu mv ' + tmp_file + ' ' + self.filename)

            else:
                QtGui.QMessageBox.warning(self, 'Edit Config File',
                                          'Package \'gksu\' isn\'t installed.\n' +
                                          'This package is needed to provide root permissions.\n' +
                                          'Please install the package or move the file\n' +
                                          tmp_file + ' manually to\n' +
                                          os.path.join(self.condor_dir, 'condor_config'),
                                          QtGui.QMessageBox.Ok)
                return

        else:
            QtGui.QMessageBox.warning(self, 'Help',
                                      'Platform ist not supported.',
                                      QtGui.QMessageBox.Ok)
            return

        # Cleaning undostack and windowtitle
        self.undostackIsClean = True
        self.setWindowTitle('Edit ' + self.filename)

    def closeEvent(self, event):
        """
        Save program settings and ask "are you sure" if there are unsaved changes.
        """

        if not self.undostackIsClean == True and self.filename:

            reply = QtGui.QMessageBox.question(self, 'Notice', 'File is not saved. Save it before quitting?', QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                #print('Reply Yes')
                if self.filename:
                    self.save()
                else:
                    self.saveAs()

            elif reply == QtGui.QMessageBox.No:
                #print('Reply No')
                pass

            elif reply == QtGui.QMessageBox.Cancel:
                #print('Reply Cancel')
                event.ignore()

            else:
                event.ignore()
                pass

    def condorReconfig(self):
        """
        Reconfig Condor.
        """
        #command = 'start /min condor_reconfig'
        command = 'condor_reconfig'
        #command = 'start condor_reconfig'

        os.system(command)

        QtGui.QMessageBox.information(self, 'Reconfig Condor',
                                     'Sent \'Reconfig\' command to local master.',
                                     QtGui.QMessageBox.Ok)

    def condorRestart(self):
        """
        Restart Condor.
        """
        #command = 'start /min condor_restart'
        command = 'condor_restart'
        #command = 'start condor_restart'

        os.system(command)

        QtGui.QMessageBox.information(self, 'Restart Condor',
                                     'Sent \'Restart\' command to local master.',
                                     QtGui.QMessageBox.Ok)
