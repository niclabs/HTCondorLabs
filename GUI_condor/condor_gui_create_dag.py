#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

import os

from PySide import QtCore, QtGui

"""
A text editor window which can be used to create and edit a job file.
"""


###############################################################################
###############################################################################
class CreateDAGWindow(QtGui.QMainWindow):
    def __init__(self, current_dialog_dir, parent=None):

        super(CreateDAGWindow, self).__init__(parent)

        self.setWindowTitle('Create DAG File')
        #self.setWindowIcon(QtGui.QIcon('xxx.ico'))

        self.current_dir = None
        self.current_dialog_dir = current_dialog_dir
        self.dagfile = None
        # Variables
        self.undostackIsClean = True

        # Number of shown lines for jobs and dependencies
        self.n_jobline = 3
        self.n_depline = 2

        # Size
        #self.setMinimumWidth(700)
        #self.setMinimumHeight(300)
        #self.setGeometry(100, 100, 860, 500)
        self.resize(860, 500)

        # Position
        parent_pos = self.parent().pos()
        self.move(parent_pos.x() + 50, parent_pos.y() + 50)

        # Central widget
        self.CreateJobWidget = QtGui.QWidget()

        self.setCentralWidget(self.CreateJobWidget)
        layout_main = QtGui.QVBoxLayout(self.CreateJobWidget)
        layout_main.setContentsMargins(0, 5, 0, 5)

        # Labels
        self.label_job_file = QtGui.QLabel(self)
        self.label_job_prio = QtGui.QLabel(self)
        self.label_job_a = QtGui.QLabel(self)
        self.label_job_b = QtGui.QLabel(self)
        self.label_job_c = QtGui.QLabel(self)
        self.label_job_d = QtGui.QLabel(self)
        self.label_job_e = QtGui.QLabel(self)
        self.label_job_f = QtGui.QLabel(self)
        self.label_job_g = QtGui.QLabel(self)
        self.label_job_h = QtGui.QLabel(self)
        self.label_job_i = QtGui.QLabel(self)
        self.label_job_j = QtGui.QLabel(self)

        self.label_syntax = QtGui.QLabel(self)

        self.label_parent_1 = QtGui.QLabel(self)
        self.label_parent_2 = QtGui.QLabel(self)
        self.label_parent_3 = QtGui.QLabel(self)
        self.label_parent_4 = QtGui.QLabel(self)
        self.label_parent_5 = QtGui.QLabel(self)
        self.label_parent_6 = QtGui.QLabel(self)

        self.label_child_1 = QtGui.QLabel(self)
        self.label_child_2 = QtGui.QLabel(self)
        self.label_child_3 = QtGui.QLabel(self)
        self.label_child_4 = QtGui.QLabel(self)
        self.label_child_5 = QtGui.QLabel(self)
        self.label_child_6 = QtGui.QLabel(self)

        self.label_error_handling = QtGui.QLabel(self)
        self.label_error_example = QtGui.QLabel(self)

        self.label_dagfile = QtGui.QLabel(self)
        self.label_preview = QtGui.QLabel(self)

        self.label_job_file.setText('Job Files')
        self.label_job_prio.setText('Priority')
        #self.label_job_prio.setAlignment(QtCore.Qt.AlignHCenter)
        self.label_job_a.setText('Job A')
        self.label_job_b.setText('Job B')
        self.label_job_c.setText('Job C')
        self.label_job_d.setText('Job D')
        self.label_job_e.setText('Job E')
        self.label_job_f.setText('Job F')
        self.label_job_g.setText('Job G')
        self.label_job_h.setText('Job H')
        self.label_job_i.setText('Job I')
        self.label_job_j.setText('Job J')

        self.label_syntax.setText('Syntax: PARENT A CHILD B C (separated by space)')

        self.label_parent_1.setText('PARENT')
        self.label_parent_2.setText('PARENT')
        self.label_parent_3.setText('PARENT')
        self.label_parent_4.setText('PARENT')
        self.label_parent_5.setText('PARENT')
        self.label_parent_6.setText('PARENT')

        self.label_child_1.setText('CHILD')
        self.label_child_2.setText('CHILD')
        self.label_child_3.setText('CHILD')
        self.label_child_4.setText('CHILD')
        self.label_child_5.setText('CHILD')
        self.label_child_6.setText('CHILD')

        self.label_error_handling.setText('Error Handling (implement manually)')
        self.label_error_example.setText('Example')

        self.label_dagfile.setText('DAG File')
        self.label_preview.setText('Preview')

        # Buttons
        self.pushButton_job_a = QtGui.QPushButton(self)
        self.pushButton_job_b = QtGui.QPushButton(self)
        self.pushButton_job_c = QtGui.QPushButton(self)
        self.pushButton_job_d = QtGui.QPushButton(self)
        self.pushButton_job_e = QtGui.QPushButton(self)
        self.pushButton_job_f = QtGui.QPushButton(self)
        self.pushButton_job_g = QtGui.QPushButton(self)
        self.pushButton_job_h = QtGui.QPushButton(self)
        self.pushButton_job_i = QtGui.QPushButton(self)
        self.pushButton_job_j = QtGui.QPushButton(self)

        self.pushButton_show_jobline = QtGui.QPushButton(self)
        self.pushButton_hide_jobline = QtGui.QPushButton(self)

        self.pushButton_show_depline = QtGui.QPushButton(self)
        self.pushButton_hide_depline = QtGui.QPushButton(self)

        self.pushButton_dagfile = QtGui.QPushButton(self)

        self.pushButton_create = QtGui.QPushButton(self)
        self.pushButton_open = QtGui.QPushButton(self)
        self.pushButton_save = QtGui.QPushButton(self)

        self.pushButton_job_a.setText('...')
        self.pushButton_job_b.setText('...')
        self.pushButton_job_c.setText('...')
        self.pushButton_job_d.setText('...')
        self.pushButton_job_e.setText('...')
        self.pushButton_job_f.setText('...')
        self.pushButton_job_g.setText('...')
        self.pushButton_job_h.setText('...')
        self.pushButton_job_i.setText('...')
        self.pushButton_job_j.setText('...')

        self.pushButton_show_jobline.setText('+')
        self.pushButton_hide_jobline.setText('-')
        self.pushButton_show_depline.setText('+')
        self.pushButton_hide_depline.setText('-')

        self.pushButton_dagfile.setText('...')

        self.pushButton_create.setText('Create DAG File')
        self.pushButton_open.setText('Open DAG File')
        self.pushButton_save.setText('Save DAG File')

        # Status and tool tips for buttons
        #self.pushButton_create.setStatusTip('Create DAG file')
        #self.pushButton_open.setStatusTip('Open existing DAG file')
        #self.pushButton_save.setStatusTip('Save DAG file')

        self.pushButton_show_jobline.setToolTip('Add job definition (F5)')
        self.pushButton_hide_jobline.setToolTip('Remove job definition (F6)')
        self.pushButton_show_depline.setToolTip('Add dependency definition (F7)')
        self.pushButton_hide_depline.setToolTip('Remove dependency definition (F8)')

        height = 25
        self.pushButton_job_a.setFixedHeight(height)
        self.pushButton_job_b.setFixedHeight(height)
        self.pushButton_job_c.setFixedHeight(height)
        self.pushButton_job_d.setFixedHeight(height)
        self.pushButton_job_e.setFixedHeight(height)
        self.pushButton_job_f.setFixedHeight(height)
        self.pushButton_job_g.setFixedHeight(height)
        self.pushButton_job_h.setFixedHeight(height)
        self.pushButton_job_i.setFixedHeight(height)
        self.pushButton_job_j.setFixedHeight(height)

        self.pushButton_show_jobline.setFixedHeight(height)
        self.pushButton_hide_jobline.setFixedHeight(height)
        self.pushButton_show_depline.setFixedHeight(height)
        self.pushButton_hide_depline.setFixedHeight(height)

        self.pushButton_dagfile.setFixedHeight(height)

        self.pushButton_create.setFixedHeight(height)
        self.pushButton_open.setFixedHeight(height)
        self.pushButton_save.setFixedHeight(height)

        width = 80
        self.pushButton_job_a.setFixedWidth(width)
        self.pushButton_job_b.setFixedWidth(width)
        self.pushButton_job_c.setFixedWidth(width)
        self.pushButton_job_d.setFixedWidth(width)
        self.pushButton_job_e.setFixedWidth(width)
        self.pushButton_job_f.setFixedWidth(width)
        self.pushButton_job_g.setFixedWidth(width)
        self.pushButton_job_h.setFixedWidth(width)
        self.pushButton_job_i.setFixedWidth(width)
        self.pushButton_job_j.setFixedWidth(width)

        self.pushButton_show_jobline.setFixedWidth(35)
        self.pushButton_hide_jobline.setFixedWidth(35)
        self.pushButton_show_depline.setFixedWidth(35)
        self.pushButton_hide_depline.setFixedWidth(35)

        self.pushButton_dagfile.setFixedWidth(width)

        self.pushButton_create.setFixedWidth(120)
        self.pushButton_open.setFixedWidth(120)
        self.pushButton_save.setFixedWidth(120)

        # line edits
        self.lineEdit_job_a = QtGui.QLineEdit(self)
        self.lineEdit_job_b = QtGui.QLineEdit(self)
        self.lineEdit_job_c = QtGui.QLineEdit(self)
        self.lineEdit_job_d = QtGui.QLineEdit(self)
        self.lineEdit_job_e = QtGui.QLineEdit(self)
        self.lineEdit_job_f = QtGui.QLineEdit(self)
        self.lineEdit_job_g = QtGui.QLineEdit(self)
        self.lineEdit_job_h = QtGui.QLineEdit(self)
        self.lineEdit_job_i = QtGui.QLineEdit(self)
        self.lineEdit_job_j = QtGui.QLineEdit(self)

        self.lineEdit_parent_1 = QtGui.QLineEdit(self)
        self.lineEdit_parent_2 = QtGui.QLineEdit(self)
        self.lineEdit_parent_3 = QtGui.QLineEdit(self)
        self.lineEdit_parent_4 = QtGui.QLineEdit(self)
        self.lineEdit_parent_5 = QtGui.QLineEdit(self)
        self.lineEdit_parent_6 = QtGui.QLineEdit(self)

        self.lineEdit_child_1 = QtGui.QLineEdit(self)
        self.lineEdit_child_2 = QtGui.QLineEdit(self)
        self.lineEdit_child_3 = QtGui.QLineEdit(self)
        self.lineEdit_child_4 = QtGui.QLineEdit(self)
        self.lineEdit_child_5 = QtGui.QLineEdit(self)
        self.lineEdit_child_6 = QtGui.QLineEdit(self)

        self.lineEdit_dagfile = QtGui.QLineEdit(self)

        self.lineEdit_job_a.setFixedHeight(height)
        self.lineEdit_job_b.setFixedHeight(height)
        self.lineEdit_job_c.setFixedHeight(height)
        self.lineEdit_job_d.setFixedHeight(height)
        self.lineEdit_job_e.setFixedHeight(height)
        self.lineEdit_job_f.setFixedHeight(height)
        self.lineEdit_job_g.setFixedHeight(height)
        self.lineEdit_job_h.setFixedHeight(height)
        self.lineEdit_job_i.setFixedHeight(height)
        self.lineEdit_job_j.setFixedHeight(height)

        self.lineEdit_parent_1.setFixedHeight(height)
        self.lineEdit_parent_2.setFixedHeight(height)
        self.lineEdit_parent_3.setFixedHeight(height)
        self.lineEdit_parent_4.setFixedHeight(height)
        self.lineEdit_parent_5.setFixedHeight(height)
        self.lineEdit_parent_6.setFixedHeight(height)

        self.lineEdit_child_1.setFixedHeight(height)
        self.lineEdit_child_2.setFixedHeight(height)
        self.lineEdit_child_3.setFixedHeight(height)
        self.lineEdit_child_4.setFixedHeight(height)
        self.lineEdit_child_5.setFixedHeight(height)
        self.lineEdit_child_6.setFixedHeight(height)

        self.lineEdit_dagfile.setFixedHeight(height)

        # Status tips and tool tips for lineEdits
        self.lineEdit_job_a.setStatusTip('Result: JOB A <JobFile>')
        self.lineEdit_job_b.setStatusTip('Result: JOB B <JobFile>')
        self.lineEdit_job_c.setStatusTip('Result: JOB C <JobFile>')
        self.lineEdit_job_d.setStatusTip('Result: JOB D <JobFile>')
        self.lineEdit_job_e.setStatusTip('Result: JOB E <JobFile>')
        self.lineEdit_job_f.setStatusTip('Result: JOB F <JobFile>')
        self.lineEdit_job_g.setStatusTip('Result: JOB G <JobFile>')
        self.lineEdit_job_h.setStatusTip('Result: JOB H <JobFile>')
        self.lineEdit_job_i.setStatusTip('Result: JOB I <JobFile>')
        self.lineEdit_job_j.setStatusTip('Result: JOB J <JobFile>')

        self.lineEdit_parent_1.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_parent_2.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_parent_3.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_parent_4.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_parent_5.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_parent_6.setStatusTip('Result: PARENT <Job> CHILD <Job>')

        self.lineEdit_child_1.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_child_2.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_child_3.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_child_4.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_child_5.setStatusTip('Result: PARENT <Job> CHILD <Job>')
        self.lineEdit_child_6.setStatusTip('Result: PARENT <Job> CHILD <Job>')

        self.lineEdit_dagfile.setToolTip('DAG description file (absolute path)')

        # Store regular style of lineEdit_job_a
        self.style_lineEdit = self.lineEdit_dagfile.styleSheet()  # original saved

        # line
        #self.line_1 = QtGui.QFrame(self)
        #self.line_1.setFrameShape(QtGui.QFrame.HLine)
        #self.line_1.setFrameShadow(QtGui.QFrame.Sunken)

        # Spin box
        self.spinBox_prio_a = QtGui.QSpinBox(self)
        self.spinBox_prio_b = QtGui.QSpinBox(self)
        self.spinBox_prio_c = QtGui.QSpinBox(self)
        self.spinBox_prio_d = QtGui.QSpinBox(self)
        self.spinBox_prio_e = QtGui.QSpinBox(self)
        self.spinBox_prio_f = QtGui.QSpinBox(self)
        self.spinBox_prio_g = QtGui.QSpinBox(self)
        self.spinBox_prio_h = QtGui.QSpinBox(self)
        self.spinBox_prio_i = QtGui.QSpinBox(self)
        self.spinBox_prio_j = QtGui.QSpinBox(self)

        self.spinBox_prio_a.setRange(-50, 50)
        self.spinBox_prio_b.setRange(-50, 50)
        self.spinBox_prio_c.setRange(-50, 50)
        self.spinBox_prio_d.setRange(-50, 50)
        self.spinBox_prio_e.setRange(-50, 50)
        self.spinBox_prio_f.setRange(-50, 50)
        self.spinBox_prio_g.setRange(-50, 50)
        self.spinBox_prio_h.setRange(-50, 50)
        self.spinBox_prio_i.setRange(-50, 50)
        self.spinBox_prio_j.setRange(-50, 50)

        self.spinBox_prio_a.setValue(0)
        self.spinBox_prio_b.setValue(0)
        self.spinBox_prio_c.setValue(0)
        self.spinBox_prio_d.setValue(0)
        self.spinBox_prio_e.setValue(0)
        self.spinBox_prio_f.setValue(0)
        self.spinBox_prio_g.setValue(0)
        self.spinBox_prio_h.setValue(0)
        self.spinBox_prio_i.setValue(0)
        self.spinBox_prio_j.setValue(0)

        self.spinBox_prio_a.setFixedHeight(height)
        self.spinBox_prio_b.setFixedHeight(height)
        self.spinBox_prio_c.setFixedHeight(height)
        self.spinBox_prio_d.setFixedHeight(height)
        self.spinBox_prio_e.setFixedHeight(height)
        self.spinBox_prio_f.setFixedHeight(height)
        self.spinBox_prio_g.setFixedHeight(height)
        self.spinBox_prio_h.setFixedHeight(height)
        self.spinBox_prio_i.setFixedHeight(height)
        self.spinBox_prio_j.setFixedHeight(height)

        self.spinBox_prio_a.setFixedWidth(width)
        self.spinBox_prio_b.setFixedWidth(width)
        self.spinBox_prio_c.setFixedWidth(width)
        self.spinBox_prio_d.setFixedWidth(width)
        self.spinBox_prio_e.setFixedWidth(width)
        self.spinBox_prio_f.setFixedWidth(width)
        self.spinBox_prio_g.setFixedWidth(width)
        self.spinBox_prio_h.setFixedWidth(width)
        self.spinBox_prio_i.setFixedWidth(width)
        self.spinBox_prio_j.setFixedWidth(width)

        self.spinBox_prio_a.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_b.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_c.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_d.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_e.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_f.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_g.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_h.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_i.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_prio_j.setAlignment(QtCore.Qt.AlignCenter)

        # Spacer (w, h)
        self.spacer_1 = QtGui.QSpacerItem(10, 10)
        self.spacer_2 = QtGui.QSpacerItem(10, 10)
        self.spacer_3 = QtGui.QSpacerItem(10, 10)
        self.spacer_4 = QtGui.QSpacerItem(10, 10)
        self.spacer_5 = QtGui.QSpacerItem(10, 10)
        #self.spacer_6 = QtGui.QSpacerItem(5, 5)

        # Textedit
        self.textedit = QtGui.QTextEdit(self) # for typing in
        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setPointSize(9)
        self.textedit.setFont(font)
        self.textedit.setUndoRedoEnabled(True)

        self.textedit_error_handling = QtGui.QTextEdit(self)
        self.textedit_error_handling.setFrameShape(QtGui.QFrame.NoFrame)
        self.textedit_error_handling.setReadOnly(True)
        self.textedit_error_handling.setFont(font)
        self.textedit_error_handling.setFixedHeight(38)
        self.textedit_error_handling.setText('SCRIPT POST <JobName> <ScriptFile> <Arg>\nRETRY <JobName> <Count>')

        self.textedit_error_example = QtGui.QTextEdit(self)
        self.textedit_error_example.setFrameShape(QtGui.QFrame.NoFrame)
        self.textedit_error_example.setReadOnly(True)
        self.textedit_error_example.setFont(font)
        self.textedit_error_example.setFixedHeight(38)
        self.textedit_error_example.setText('SCRIPT POST A C:\cmd.bat $DAG_STATUS\nRETRY A 3')

        # Layouts
        layout_left = QtGui.QVBoxLayout()
        layout_left.setContentsMargins(5, 5, 5, 5)

        self.layout_upper_left = QtGui.QGridLayout()
        self.layout_upper_left.setContentsMargins(0, 0, 0, 0)
        self.layout_upper_left.setHorizontalSpacing(10)
        #self.layout_upper_left.setAlignment(QtCore.Qt.AlignTop)

        self.layout_mid_left = QtGui.QGridLayout()
        self.layout_mid_left.setContentsMargins(0, 0, 0, 0)
        self.layout_mid_left.setHorizontalSpacing(10)

        layout_lower_left = QtGui.QGridLayout()
        layout_lower_left.setContentsMargins(0, 0, 0, 0)
        layout_lower_left.setHorizontalSpacing(10)

        layout_right = QtGui.QGridLayout()
        layout_right.setContentsMargins(0, 5, 5, 5)

        sub_layout_buttons_depline = QtGui.QHBoxLayout()
        sub_layout_buttons_depline.setSpacing(10)
        sub_layout_buttons_depline.addWidget(self.pushButton_show_depline)
        sub_layout_buttons_depline.addWidget(self.pushButton_hide_depline)

        # PySide.QtGui.QGridLayout.addLayout(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        #layout_left.addWidget(self.pushButton_job_a, 1, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.layout_upper_left.addWidget(self.label_job_file, 0, 0, 1, 1)
        self.layout_upper_left.addWidget(self.label_job_prio, 0, 2, 1, 1)

        self.layout_upper_left.addWidget(self.label_job_a, 1, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_a, 1, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_a, 1, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_a, 1, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_b, 2, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_b, 2, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_b, 2, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_b, 2, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_c, 3, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_c, 3, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_c, 3, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_c, 3, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_d, 4, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_d, 4, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_d, 4, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_d, 4, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_e, 5, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_e, 5, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_e, 5, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_e, 5, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_f, 6, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_f, 6, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_f, 6, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_f, 6, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_g, 7, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_g, 7, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_g, 7, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_g, 7, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_h, 8, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_h, 8, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_h, 8, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_h, 8, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_i, 9, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_i, 9, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_i, 9, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_i, 9, 3, 1, 2)

        self.layout_upper_left.addWidget(self.label_job_j, 10, 0, 1, 1)
        self.layout_upper_left.addWidget(self.lineEdit_job_j, 10, 1, 1, 1)
        self.layout_upper_left.addWidget(self.spinBox_prio_j, 10, 2, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_job_j, 10, 3, 1, 2)

        self.layout_upper_left.addWidget(self.pushButton_show_jobline, 11, 3, 1, 1)
        self.layout_upper_left.addWidget(self.pushButton_hide_jobline, 11, 4, 1, 1)
        
        self.layout_mid_left.addWidget(self.label_syntax, 0, 0, 1, 4)
        self.layout_mid_left.addWidget(self.label_parent_1, 1, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_1, 1, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_1, 1, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_1, 1, 3, 1, 1)

        self.layout_mid_left.addWidget(self.label_parent_2, 2, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_2, 2, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_2, 2, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_2, 2, 3, 1, 1)

        self.layout_mid_left.addWidget(self.label_parent_3, 3, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_3, 3, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_3, 3, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_3, 3, 3, 1, 1)

        self.layout_mid_left.addWidget(self.label_parent_4, 4, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_4, 4, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_4, 4, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_4, 4, 3, 1, 1)

        self.layout_mid_left.addWidget(self.label_parent_5, 5, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_5, 5, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_5, 5, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_5, 5, 3, 1, 1)

        self.layout_mid_left.addWidget(self.label_parent_6, 6, 0, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_parent_6, 6, 1, 1, 1)
        self.layout_mid_left.addWidget(self.label_child_6, 6, 2, 1, 1)
        self.layout_mid_left.addWidget(self.lineEdit_child_6, 6, 3, 1, 1)

        self.layout_mid_left.addLayout(sub_layout_buttons_depline, 7, 3, 1, 1, alignment=QtCore.Qt.AlignRight)

        self.layout_mid_left.addItem(self.spacer_1, 8, 0, 1, 1)

        self.layout_mid_left.addWidget(self.label_error_handling, 9, 0, 1, 4)
        self.layout_mid_left.addWidget(self.textedit_error_handling, 10, 0, 1, 4)
        self.layout_mid_left.addWidget(self.label_error_example, 11, 0, 1, 4)
        self.layout_mid_left.addWidget(self.textedit_error_example, 12, 0, 1, 4)

        layout_lower_left.addWidget(self.label_dagfile, 0, 0, 1, 1)
        layout_lower_left.addWidget(self.lineEdit_dagfile, 0, 1, 1, 1)
        layout_lower_left.addWidget(self.pushButton_dagfile, 0, 2, 1, 1)

        layout_lower_left.addItem(self.spacer_2, 1, 1, 1, 1)
        layout_lower_left.addWidget(self.pushButton_create, 2, 1, 1, 2, alignment=QtCore.Qt.AlignRight)

        # initially hiding joblines and deplines
        self.initial_hide_joblines()
        self.initial_hide_deplines()

        layout_left.addLayout(self.layout_upper_left)
        layout_left.addItem(self.spacer_3)
        layout_left.addLayout(self.layout_mid_left)
        layout_left.addItem(self.spacer_4)
        layout_left.addLayout(layout_lower_left)

        layout_right.addWidget(self.label_preview, 0, 1, 1, 3)
        layout_right.addWidget(self.textedit, 1, 0, 1, 4)
        layout_right.addItem(self.spacer_5, 2, 0, 1, 4)
        layout_right.addWidget(self.pushButton_open, 3, 2, 1, 1)
        layout_right.addWidget(self.pushButton_save, 3, 3, 1, 1)
        #layout_right.addItem(self.spacer_6, 2, 3, 1, 1, alignment=QtCore.Qt.AlignRight)

        #layout_right.setColumnMinimumWidth(0, 1)
        layout_right.setColumnMinimumWidth(1, 1)
        layout_right.setColumnMinimumWidth(2, 1)
        #layout_right.setColumnMinimumWidth(3, 1)

        #layout_right.setColumnStretch(0, 1)
        layout_right.setColumnStretch(1, 1)
        layout_right.setColumnStretch(2, 1)
        #layout_right.setColumnStretch(3, 1)

        # Frames
        frame_left = QtGui.QFrame()
        frame_left.setLayout(layout_left)
        frame_left.setFrameShape(QtGui.QFrame.NoFrame)
        frame_left.setFrameShadow(QtGui.QFrame.Sunken)
        frame_left.setMinimumWidth(380)

        frame_right = QtGui.QFrame()
        frame_right.setLayout(layout_right)
        frame_right.setFrameShape(QtGui.QFrame.NoFrame)
        frame_right.setFrameShadow(QtGui.QFrame.Sunken)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(frame_left)
        splitter.addWidget(frame_right)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)

        # Combine layouts
        layout_main.addWidget(splitter)
        self.setLayout(layout_main)

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
        fileMenu.addAction(QtGui.QAction('&Open...', self, shortcut='Ctrl+O', triggered=self.open))
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

        # Status Bar
        self.statusbar = self.statusBar()

        # Signals
        self.pushButton_job_a.clicked.connect(lambda: self.load_job(1))
        self.pushButton_job_b.clicked.connect(lambda: self.load_job(2))
        self.pushButton_job_c.clicked.connect(lambda: self.load_job(3))
        self.pushButton_job_d.clicked.connect(lambda: self.load_job(4))
        self.pushButton_job_e.clicked.connect(lambda: self.load_job(5))
        self.pushButton_job_f.clicked.connect(lambda: self.load_job(6))
        self.pushButton_job_g.clicked.connect(lambda: self.load_job(7))
        self.pushButton_job_h.clicked.connect(lambda: self.load_job(8))
        self.pushButton_job_i.clicked.connect(lambda: self.load_job(9))
        self.pushButton_job_j.clicked.connect(lambda: self.load_job(10))

        self.pushButton_show_jobline.clicked.connect(self.show_jobline)
        self.pushButton_hide_jobline.clicked.connect(self.hide_jobline)
        self.pushButton_show_depline.clicked.connect(self.show_depline)
        self.pushButton_hide_depline.clicked.connect(self.hide_depline)

        self.pushButton_dagfile.clicked.connect(self.set_dagfile)

        self.pushButton_create.clicked.connect(self.create_dagfile)
        self.pushButton_open.clicked.connect(self.open)
        self.pushButton_save.clicked.connect(self.save)

        self.textedit.textChanged.connect(self.setUndoStack)

        # Short cuts
        QtGui.QShortcut(QtGui.QKeySequence('F5'), self, self.show_jobline)
        QtGui.QShortcut(QtGui.QKeySequence('F6'), self, self.hide_jobline)
        QtGui.QShortcut(QtGui.QKeySequence('F7'), self, self.show_depline)
        QtGui.QShortcut(QtGui.QKeySequence('F8'), self, self.hide_depline)

    #############################################################################
    # DAG file handling
    #############################################################################
    def create_dagfile(self):
        """
        Create dagfile from values
        """
        if not self.check_values():
            #print('error')
            return
        else:
            #print('no error')
            pass

        # dagfile
        self.dagfile = self.lineEdit_dagfile.text()

        # job lines
        list_jobfiles = []
        list_jobprios = []
        show_rows = self.n_jobline

        for row in range(show_rows):

            label = self.layout_upper_left.itemAtPosition(row + 1, 0).widget()
            line_edit = self.layout_upper_left.itemAtPosition(row + 1, 1).widget()
            spin_box = self.layout_upper_left.itemAtPosition(row + 1, 2).widget()

            joblabel = label.text().upper()
            jobfile = line_edit.text()
            jobprio = str(spin_box.value())
            list_jobfiles.append(' '.join([joblabel, jobfile]))
            list_jobprios.append(' '.join(['PRIORITY', joblabel.split()[1], jobprio]))

        # dependency lines
        list_dependencies = []
        show_rows = self.n_depline + 1
        for row in range(1, show_rows):
            label_1 = self.layout_mid_left.itemAtPosition(row, 0).widget()
            line_edit_1 = self.layout_mid_left.itemAtPosition(row, 1).widget()
            label_2 = self.layout_mid_left.itemAtPosition(row, 2).widget()
            line_edit_2 = self.layout_mid_left.itemAtPosition(row, 3).widget()

            parentlabel = label_1.text().upper()
            parent = line_edit_1.text().upper()
            childlabel = label_2.text().upper()
            child = ' '.join(list(line_edit_2.text().upper()))

            list_dependencies.append(' '.join([parentlabel, parent, childlabel, child]))

        # create outstring
        outstring = \
            '####################' + '\n' + \
            '#' + '\n' + \
            '# HTCondor DAG file' + '\n' + \
            '#' + '\n' + \
            '####################' + '\n\n' + \
            '\n'.join(list_jobfiles) + \
            '\n\n' + \
            '\n'.join(list_dependencies) + \
            '\n\n' + \
            '\n'.join(list_jobprios)

        self.textedit.setText(outstring)
        self.setWindowTitle('Create DAG File (' + self.dagfile + '*)')

    def open(self):
        """
        Open condor_config by file dialog.
        """

        if self.current_dialog_dir:
            dagfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open DAG File',
                                                                dir=self.current_dialog_dir,
                                                                filter='DAG files (*.dag);;All files(*)')

        else:
            dagfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open DAG File',
                                                                filter='DAG files (*.dag);;All files(*)')
        if dagfile:
            self.dagfile = os.path.realpath(dagfile)
            self.current_dialog_dir = os.path.dirname(self.dagfile)

            with open(self.dagfile,'r') as file:
                self.textedit.setText(file.read())

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            #print('undostackIsClean',self.undostackIsClean)
            self.setWindowTitle('Create DAG File (' + self.dagfile + ')')
        else:
            pass

    def save(self):
        """
        Save dagfile
        """
        if self.dagfile:
            with open(self.dagfile,'wt') as file:
                file.write(self.textedit.toPlainText())

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            self.setWindowTitle('Create DAG File (' + self.dagfile + ')')

        else:
            self.saveAs()

    def saveAs(self):
        """
        Save dagfile to a different directory pulled out of a file dialog.
        """
        filename_new, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Save DAG File',
                                                                      dir=self.current_dialog_dir,
                                                                      filter='DAG files (*.dag);;All files(*)')
        if filename_new:
            self.dagfile = os.path.realpath(filename_new)
            self.current_dialog_dir = os.path.dirname(self.dagfile)

            with open(self.dagfile,'wt') as file:
                    file.write(self.textedit.toPlainText())

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            self.setWindowTitle('Create DAG File (' + self.dagfile + ')')

        else:
            pass

    def check_values(self):
        """
        Check some necessary values (dagfile, jobfiles and dependencies) on left side and return True if values are ok.
        """
        state_ok = True

        # dagfile
        dagfile = self.lineEdit_dagfile.text()

        if dagfile != '':
            self.lineEdit_dagfile.setStyleSheet(self.style_lineEdit)  # original style
            self.current_dir = os.path.dirname(dagfile)
        else:
            self.lineEdit_dagfile.setStyleSheet('border: 1px solid red;')  # red style
            state_ok = False
            return state_ok

        # job lines
        show_rows = self.n_jobline

        for row in range(show_rows):
            line_edit = self.layout_upper_left.itemAtPosition(row + 1, 1).widget()

            jobfile = line_edit.text()

            if jobfile != '' and os.path.isfile(os.path.join(self.current_dir, jobfile)):
                line_edit.setStyleSheet(self.style_lineEdit)  # original style
            else:
                line_edit.setStyleSheet('border: 1px solid red;')  # red style
                state_ok = False

        # dependency lines
        show_rows = self.n_depline + 1

        for row in range(1, show_rows):
            line_edit_1 = self.layout_mid_left.itemAtPosition(row, 1).widget()
            line_edit_2 = self.layout_mid_left.itemAtPosition(row, 3).widget()

            # parent
            parent = line_edit_1.text()
            if parent != '':
                line_edit_1.setStyleSheet(self.style_lineEdit)  # original style
            else:
                line_edit_1.setStyleSheet('border: 1px solid red;')  # red style
                state_ok = False

            # child
            child = line_edit_2.text()
            if child != '':
                line_edit_2.setStyleSheet(self.style_lineEdit)  # original style
            else:
                line_edit_2.setStyleSheet('border: 1px solid red;')  # red style
                state_ok = False

        return state_ok

    #############################################################################
    # Set Values on left side
    #############################################################################

    def load_job(self, row):
        """
        Dialog to job file of job in given row of self.layout_upper_left.
        """
        # get line edit widget
        lineEdit_job_widget = self.layout_upper_left.itemAtPosition(row, 1).widget()

        if self.current_dialog_dir:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                dir=self.current_dialog_dir,
                                                                filter='Job files (*.job *.condor);;All files(*)')

        else:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                filter='Job files (*.job *.condor);;All files(*)')
        if jobfile:
            jobfile = os.path.realpath(jobfile)
            self.current_dialog_dir = os.path.dirname(jobfile)
            jobfile = os.path.basename(jobfile)
            lineEdit_job_widget.setText(jobfile)
        else:
            pass
    
    def set_dagfile(self):
        """
        Dialog to set dagfile.
        """
        if self.current_dialog_dir:
            dagfile, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Set DAG File',
                                                                dir=self.current_dialog_dir,
                                                                filter='DAG files (*.dag);;All files(*)')

        else:
            dagfile, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Set DAG File',
                                                                filter='DAG files (*.dag);;All files(*)')

        if dagfile:
            dagfile = os.path.realpath(dagfile)
            self.dagfile = dagfile
            self.current_dir = os.path.dirname(dagfile)
            self.current_dialog_dir = os.path.dirname(dagfile)
            self.lineEdit_dagfile.setText(dagfile)
        else:
            pass

    #############################################################################
    # Flexible layout
    #############################################################################
    def initial_hide_joblines(self):
        """
        Initial hiding of widgets self.layout_upper_left depending on self.n_jobline.
        """
        show_rows = self.n_jobline + 1
        rows = self.layout_upper_left.rowCount() - 1

        for row in range(show_rows, rows):
            label = self.layout_upper_left.itemAtPosition(row, 0).widget()
            line_edit = self.layout_upper_left.itemAtPosition(row, 1).widget()
            spin_box = self.layout_upper_left.itemAtPosition(row, 2).widget()
            push_button = self.layout_upper_left.itemAtPosition(row, 3).widget()

            label.hide()
            line_edit.hide()
            spin_box.hide()
            push_button.hide()

        self.resize(self.width(), self.minimumSizeHint().height())

    def show_jobline(self):
        """
        Show widgets in self.n_jobline in self.layout_upper_left.
        """
        row = self.n_jobline + 1
        if row < 10:
            label = self.layout_upper_left.itemAtPosition(row, 0).widget()
            line_edit = self.layout_upper_left.itemAtPosition(row, 1).widget()
            spin_box = self.layout_upper_left.itemAtPosition(row, 2).widget()
            push_button = self.layout_upper_left.itemAtPosition(row, 3).widget()

            label.show()
            line_edit.show()
            spin_box.show()
            push_button.show()

            # restore original style
            line_edit.setStyleSheet(self.style_lineEdit)

            self.n_jobline += 1
            self.resize(self.width(), self.minimumSizeHint().height())
        else:
            pass

    def hide_jobline(self):
        """
        Show widgets in self.n_jobline in self.layout_upper_left.
        """
        row = self.n_jobline

        if row > 2:
            label = self.layout_upper_left.itemAtPosition(row, 0).widget()
            line_edit = self.layout_upper_left.itemAtPosition(row, 1).widget()
            spin_box = self.layout_upper_left.itemAtPosition(row, 2).widget()
            push_button = self.layout_upper_left.itemAtPosition(row, 3).widget()

            label.hide()
            line_edit.hide()
            line_edit.clear()
            spin_box.hide()
            spin_box.setValue(0)
            push_button.hide()

            self.n_jobline -= 1
            self.resize(self.width(), self.minimumSizeHint().height())

        else:
            pass

    def initial_hide_deplines(self):
        """
        Initial hiding of widgets self.layout_mid_left depending on self.n_depline.
        """
        show_rows = self.n_depline + 1
        rows = self.layout_mid_left.rowCount() - 6

        for row in range(show_rows, rows):
            label_1 = self.layout_mid_left.itemAtPosition(row, 0).widget()
            line_edit_1 = self.layout_mid_left.itemAtPosition(row, 1).widget()
            label_2 = self.layout_mid_left.itemAtPosition(row, 2).widget()
            line_edit_2 = self.layout_mid_left.itemAtPosition(row, 3).widget()

            label_1.hide()
            line_edit_1.hide()
            label_2.hide()
            line_edit_2.hide()

        self.resize(self.width(), self.minimumSizeHint().height())

    def show_depline(self):
        """
        Show widgets in self.n_depline in self.layout_mid_left.
        """
        row = self.n_depline + 1
        if row < 7:
            label_1 = self.layout_mid_left.itemAtPosition(row, 0).widget()
            line_edit_1 = self.layout_mid_left.itemAtPosition(row, 1).widget()
            label_2 = self.layout_mid_left.itemAtPosition(row, 2).widget()
            line_edit_2 = self.layout_mid_left.itemAtPosition(row, 3).widget()

            label_1.show()
            line_edit_1.show()
            label_2.show()
            line_edit_2.show()

            # restore original style
            line_edit_1.setStyleSheet(self.style_lineEdit)
            line_edit_2.setStyleSheet(self.style_lineEdit)

            self.n_depline += 1
            self.resize(self.width(), self.minimumSizeHint().height())
        else:
            pass

    def hide_depline(self):
        """
        Show widgets in self.n_depline in self.layout_mid_left.
        """
        row = self.n_depline

        if row > 1:
            label_1 = self.layout_mid_left.itemAtPosition(row, 0).widget()
            line_edit_1 = self.layout_mid_left.itemAtPosition(row, 1).widget()
            label_2 = self.layout_mid_left.itemAtPosition(row, 2).widget()
            line_edit_2 = self.layout_mid_left.itemAtPosition(row, 3).widget()

            label_1.hide()
            line_edit_1.hide()
            label_2.hide()
            line_edit_2.hide()

            self.n_depline -= 1
            self.resize(self.width(), self.minimumSizeHint().height())

        else:
            pass

    #############################################################################
    # General
    #############################################################################
    def setUndoStack(self):
        """
        Selfmade undostack when text in textedit changed.
        """
        self.undostackIsClean = False

        if self.dagfile:
            #print('If',self.filename)
            self.setWindowTitle('Create DAG File (' + self.dagfile + '*)')
        else:
            #print('Else',self.filename)
            self.setWindowTitle('Create DAG File*')

    def closeEvent(self, event):
        """
        Ask "are you sure" if there are unsaved changes.
        """
        if not self.undostackIsClean and self.dagfile:

            reply = QtGui.QMessageBox.question(self, 'Notice', 'File is not saved. Save it before quitting?',
                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                if self.dagfile:
                    self.save()
                else:
                    self.saveAs()

            elif reply == QtGui.QMessageBox.No:
                event.accept()

            elif reply == QtGui.QMessageBox.Cancel:
                event.ignore()

            else:
                event.ignore()