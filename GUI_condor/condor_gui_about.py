#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

from PySide import QtCore, QtGui

import condor_gui_version

"""
A QT graphics widget for NOA commands and one for redirecting stdout and stderr in console.
"""

###############################################################################
###############################################################################


class AboutWidget(QtGui.QWidget):
    def __init__(self, parent=None):

        super(AboutWidget, self).__init__(parent)

        # Variables
        self.show_lic = False
        self.show_soft = False
        
        self.setWindowTitle('About Condor GUI')

        # Size and Position
        w = 550
        h = 200  # exact size is determined by content
        x = self.parent().x() + (self.parent().width() - w)/2
        y = self.parent().y() + (self.parent().height() - h)/2 - 100

        #self.setGeometry(x, y, w, h)
        self.move(x, y)
        self.setFixedWidth(w)

        self.layout_main = QtGui.QGridLayout()
        self.layout_main.setContentsMargins(5, 5, 5, 0)

        # Window flags to modify the frame
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint)  # only close Button
        #self.setWindowFlags(QtCore.Qt.Popup)  # no frame
        #self.setWindowFlags(QtCore.Qt.ToolTip)  # doesn't close

        # Labels
        self.label_heading = QtGui.QLabel(self)
        self.label_pic = QtGui.QLabel(self)
        self.label_pic.setAlignment(QtCore.Qt.AlignHCenter)

        self.label_heading.setText(
            'Condor GUI\n'
            'Version ' + condor_gui_version.__version__ + '\n\n'
            'Condor GUI is distributed with the BSD license.\n\n'
            'Copyright © 2016, Condor GUI Developers\n'
            'Bartosz Dziubaczyk, Andreas Wünsch\n'
            'Otto von Guericke University Magdeburg\n'
            'All rights reserved.')

        # Logo
        pixmap = QtGui.QPixmap(':/icon_condor_gui.png')
        self.label_pic.setPixmap(pixmap.scaled(64, 64))

        # Buttons
        self.button_lic = QtGui.QPushButton(self)
        self.button_lic.setText('License')
        self.button_lic.setFixedHeight(25)
        self.button_lic.setFixedWidth(150)

        self.button_software = QtGui.QPushButton(self)
        self.button_software.setText('Included Software')
        self.button_software.setFixedHeight(25)
        self.button_software.setFixedWidth(150)

        self.button_ok = QtGui.QPushButton(self)
        self.button_ok.setText('OK')
        self.button_ok.setFixedHeight(25)
        self.button_ok.setFixedWidth(150)
        self.button_ok.setAutoDefault(False)
        self.button_ok.setFocus()

        self.textedit_lic = QtGui.QTextEdit(self)
        self.textedit_lic.setFrameShape(QtGui.QFrame.NoFrame)
        self.textedit_lic.setReadOnly(True)
        self.textedit_lic.setAutoFormatting(QtGui.QTextEdit.AutoBulletList)
        self.textedit_lic.setText(
            'BSD license.\n\n'
            'Redistribution and use in source and binary forms, with or without modification, are permitted '
            'provided that the following conditions are met:\n\n'
            '- Redistributions of source code must retain the above copyright notice, this list of conditions\n'
            '   and the following disclaimer.\n\n'
            '- Redistributions in binary form must reproduce the above copyright notice, this list of conditions\n'
            '   and the following disclaimer in the documentation and/or other materials provided with the\n'
            '   distribution.\n\n'
            '- Neither the name of the copyright holder nor the names of its contributors may be used to\n'
            '   endorse or promote products derived from this software without specific prior written\n'
            '   permission.\n\n'
            'THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS \'AS IS\' AND ANY EXPRESS OR IMPLIED WARRANTIES,'
            'INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR'
            'PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,'
            'INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF'
            'SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND'
            'ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR'
            'OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF'
            'SUCH DAMAGE.')

        #self.textbrowser_software = QtGui.QTextEdit(self)
        self.textbrowser_software = QtGui.QTextBrowser()
        self.textbrowser_software.setFrameShape(QtGui.QFrame.NoFrame)
        self.textbrowser_software.setReadOnly(True)
        self.textbrowser_software.setOpenExternalLinks(True)
        #self.textbrowser_software.setOpenLinks(True)
        self.textbrowser_software.append(
            'Condor GUI uses the following software and modules:\n\n'
            'PySide bindings for QT 4.8.\n')
        #self.textbrowser_software.setHtml("<a href='http://www.w3schools.com/'>Link!</a>aah\n")
        #self.textbrowser_software.insertHtml("<a href='http://www.w3schools.com/'>Link!</a>aah\n")
        #self.cursor = self.textbrowser_software.textCursor()
        self.textbrowser_software.insertHtml("<a href='http://www.pyside.org/'style='color: rgb(61,142,201)'>www.pyside.org</a>\n")
        self.textbrowser_software.append('License: LGPL\n')

        self.textbrowser_software.append('QDarkStyleSheet\n')
        self.textbrowser_software.insertHtml("<a href='https://github.com/ColinDuquesnoy/QDarkStyleSheet/'style='color: rgb(61,142,201)'>https://github.com/ColinDuquesnoy/QDarkStyleSheet</a>\n")
        self.textbrowser_software.append('Copyright © 2013-2014, Colin Duquesnoy\n\n'
            'License: MIT\n'
            'Permission is hereby granted, free of charge, to any person obtaining a copy '
            'of this software and associated documentation files (the "Software"), to deal '
            'in the Software without restriction, including without limitation the rights '
            'to use, copy, modify, merge, publish, distribute, sublicense, and/or sell '
            'copies of the Software, and to permit persons to whom the Software is '
            'furnished to do so, subject to the following conditions:\n\n'
            'The above copyright notice and this permission notice shall be included in '
            'all copies or substantial portions of the Software.\n\n'
            'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR '
            'IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, '
            'FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE '
            'AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER'
            'LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM , '
            'OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN '
            'THE SOFTWARE.\n')
        # go to start
        self.textbrowser_software.moveCursor(QtGui.QTextCursor.Start)

        # Spacer (w, h)
        self.spacer_1 = QtGui.QSpacerItem(10, 10)
        self.spacer_2 = QtGui.QSpacerItem(10, 10)

        # Hide text edits
        self.textedit_lic.hide()
        self.textbrowser_software.hide()

        # Layouts
        # PySide.QtGui.QGridLayout.addLayout(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        #layout_left.addWidget(self.pushButton_executable, 1, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.layout_main.addItem(self.spacer_1, 0, 0, 1, 1)
        self.layout_main.addWidget(self.label_heading, 0, 1, 2, 3, alignment=QtCore.Qt.AlignTop)

        self.layout_main.addWidget(self.label_pic, 1, 0, 1, 1, alignment=QtCore.Qt.AlignTop)

        self.layout_main.addItem(self.spacer_2, 2, 0, 1, 1)

        self.layout_main.addWidget(self.button_lic, 3, 0, 1, 1)
        self.layout_main.addWidget(self.button_software, 3, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.layout_main.addWidget(self.button_ok, 3, 3, 1, 1)

        self.layout_main.addWidget(self.textedit_lic, 4, 0, 4, 4)
        self.layout_main.addWidget(self.textbrowser_software, 4, 0, 4, 4)

        # necessary for uniform column width
        #layout_text.setRowMinimumHeight(0, 1)
        self.layout_main.setRowMinimumHeight(1, 1)
        #self.layout_main.setRowMinimumHeight(2, 1)
        self.layout_main.setRowMinimumHeight(3, 1)
        self.layout_main.setRowMinimumHeight(4, 1)

        #layout_text.setRowStretch(0, 1)
        self.layout_main.setRowStretch(1, 1)
        #self.layout_main.setRowStretch(2, 1)
        self.layout_main.setRowStretch(3, 1)
        self.layout_main.setRowStretch(4, 5)

        self.setLayout(self.layout_main)

        # Fix height to recommended value
        self.height_folded = self.minimumSizeHint().height()
        self.setFixedHeight(self.height_folded)

        # Signals
        self.button_lic.clicked.connect(self.show_license)
        self.button_software.clicked.connect(self.show_software)
        self.button_ok.clicked.connect(self.ok_button_pressed)

    def show_license(self):
        """
        Show textedit with license information.
        """
        if self.show_lic:
            self.textedit_lic.hide()
            self.show_lic = False
            #self.layout_main.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
            self.setFixedHeight(self.height_folded)
            self.layout_main.setContentsMargins(5, 5, 5, 0)

        else:
            self.textbrowser_software.hide()
            self.show_soft = False
            self.textedit_lic.show()
            self.show_lic = True
            self.setFixedHeight(400)
            self.layout_main.setContentsMargins(5, 5, 5, 5)

    def show_software(self):
        """
        Show textedit with included software information.
        """
        if self.show_soft:
            self.textbrowser_software.hide()
            self.show_soft = False
            #self.layout_main.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
            self.setFixedHeight(self.height_folded)
            self.layout_main.setContentsMargins(5, 5, 5, 0)

        else:
            self.textedit_lic.hide()
            self.show_lic = False
            self.textbrowser_software.show()
            self.show_soft = True
            self.setFixedHeight(400)
            self.layout_main.setContentsMargins(5, 5, 5, 5)

    def ok_button_pressed(self):
        """
        Close the window.
        """
        self.close()

    def keyPressEvent(self, event):
        """
        keypress events for Escape
        """
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            pass
