#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

from PySide import QtCore, QtGui


class CentralWidget(QtGui.QWidget):

    def __init__(self, parent):
        super(CentralWidget, self).__init__(parent)

        layout_main = QtGui.QVBoxLayout()
        layout_main.setContentsMargins(0, 5, 0, 5)

        layout_upper = QtGui.QVBoxLayout()
        layout_upper.setContentsMargins(5, 5, 5, 5)

        layout_lower = QtGui.QVBoxLayout()
        layout_lower.setContentsMargins(5, 5, 5, 5)

        #self.setWindowIcon(QtGui.QIcon('xxx.ico'))

        # Size
        self.setMinimumHeight(400)
        self.setMinimumWidth(600)
        self.setGeometry(100,100,900,600)

        # Labels
        self.label_res = QtGui.QLabel(self)
        self.label_job = QtGui.QLabel(self)
        self.label_res_cmd = QtGui.QLabel(self)
        self.label_job_id_1 = QtGui.QLabel(self)
        self.label_job_id_2 = QtGui.QLabel(self)
        self.label_job_prio = QtGui.QLabel(self)

        self.label_res.setText('Pool Resources')
        self.label_job.setText('Jobs')
        self.label_res_cmd.setText('Command Line')
        self.label_job_id_1.setText('ID')
        self.label_job_id_2.setText('ID')
        self.label_job_prio.setText('Prio')

        self.label_res.setFixedHeight(20)
        self.label_job.setFixedHeight(20)

        font = QtGui.QFont()
        font.setFamily('Consolas')
        #font.setFamily('Courier')
        font.setPointSize(9)

        # Textbrowser
        self.textbrowser_res = QtGui.QTextBrowser(self)
        self.textbrowser_res.setFont(font)

        self.textbrowser_job = QtGui.QTextBrowser(self)
        self.textbrowser_job.setFont(font)

        # Buttons
        self.pushButton_res_all = QtGui.QPushButton(self)
        self.pushButton_res_job = QtGui.QPushButton(self)
        self.pushButton_res_avail = QtGui.QPushButton(self)
        self.pushButton_res_run = QtGui.QPushButton(self)
        self.pushButton_res_online = QtGui.QPushButton(self)
        self.pushButton_res_offline = QtGui.QPushButton(self)

        self.pushButton_res_all.setText('Show All Resources')
        self.pushButton_res_job.setText('All Job Resources ')
        self.pushButton_res_avail.setText('Available Resources')
        self.pushButton_res_run.setText('Running Resources')
        self.pushButton_res_online.setText('Online Resources')
        self.pushButton_res_offline.setText('Offline Resources')

        # Status tip
        self.pushButton_res_all.setStatusTip('Command: condor_status')
        self.pushButton_res_job.setStatusTip('Command: condor_status -autoformat:h Name OpSysName Cpus Memory Disk LoadAvg State KeyboardIdle Activity ActTime JobId')
        self.pushButton_res_avail.setStatusTip('Command: condor_status -available')
        self.pushButton_res_run.setStatusTip('Command: condor_status -run')
        self.pushButton_res_online.setStatusTip('Command: condor_status -constraint Offline=!=True')
        self.pushButton_res_offline.setStatusTip('Command: condor_status -constraint Offline==True')

        self.pushButton_job_show_que = QtGui.QPushButton(self)
        self.pushButton_job_analyze = QtGui.QPushButton(self)
        self.pushButton_job_show_details = QtGui.QPushButton(self)
        self.pushButton_job_show_all = QtGui.QPushButton(self)
        self.pushButton_job_rm_id = QtGui.QPushButton(self)
        self.pushButton_job_rm_all = QtGui.QPushButton(self)
        self.pushButton_job_edit_prio = QtGui.QPushButton(self)
        self.pushButton_job_start_job = QtGui.QPushButton(self)
        self.pushButton_job_start_dag = QtGui.QPushButton(self)

        self.pushButton_job_show_que.setText('Show Jobs in Queue')
        self.pushButton_job_analyze.setText('Analyze Jobs in Queue')
        self.pushButton_job_show_details.setText('Show Job Commands')
        self.pushButton_job_show_all.setText('Show All Jobs')
        self.pushButton_job_rm_id.setText('Remove Job')
        self.pushButton_job_rm_all.setText('Remove All Jobs')
        self.pushButton_job_edit_prio.setText('Edit Priority')
        self.pushButton_job_start_job.setText('Submit Job')
        self.pushButton_job_start_dag.setText('Submit DAG')

        # status tip
        self.pushButton_job_show_que.setStatusTip('Command: condor_q -dag')
        self.pushButton_job_analyze.setStatusTip('Command: condor_q -better-analyze -global')
        self.pushButton_job_show_details.setStatusTip('Command: condor_q -dag -autoformat ClusterId Owner CMD')
        self.pushButton_job_show_all.setStatusTip('Command: condor_q -dag -global')
        self.pushButton_job_rm_id.setStatusTip('Command: condor_rm <ID>')
        self.pushButton_job_rm_all.setStatusTip('Command: condor_rm -all')
        self.pushButton_job_edit_prio.setStatusTip('Command: condor_prio -p <Prio> <ID>')
        self.pushButton_job_start_job.setStatusTip('Command: condor_submit <Job file>')
        self.pushButton_job_start_dag.setStatusTip('Command: condor_submit_dag -f <DAG file>')

        height = 25
        self.pushButton_res_all.setFixedHeight(height)
        self.pushButton_res_job.setFixedHeight(height)
        self.pushButton_res_avail.setFixedHeight(height)
        self.pushButton_res_run.setFixedHeight(height)
        self.pushButton_res_online.setFixedHeight(height)
        self.pushButton_res_offline.setFixedHeight(height)

        self.pushButton_job_show_all.setFixedHeight(height)
        self.pushButton_job_show_que.setFixedHeight(height)
        self.pushButton_job_show_details.setFixedHeight(height)
        self.pushButton_job_analyze.setFixedHeight(height)

        self.pushButton_job_rm_id.setFixedHeight(height)
        self.pushButton_job_rm_all.setFixedHeight(height)
        self.pushButton_job_edit_prio.setFixedHeight(height)
        self.pushButton_job_start_job.setFixedHeight(height)
        self.pushButton_job_start_dag.setFixedHeight(height)

        # line edits
        self.lineEdit_res_cmd = QtGui.QLineEdit(self)
        self.lineEdit_res_cmd.setFixedHeight(25)

        self.lineEdit_job_id_1 = QtGui.QLineEdit(self)
        #self.lineEdit_job_id_1.setAlignment(QtCore.Qt.AlignRight)
        self.lineEdit_job_id_1.setFixedHeight(25)

        self.lineEdit_job_id_2 = QtGui.QLineEdit(self)
        self.lineEdit_job_id_2.setFixedHeight(25)

        self.lineEdit_job_prio = QtGui.QLineEdit(self)
        self.lineEdit_job_prio.setFixedHeight(25)

        # line
        #self.line_1 = QtGui.QFrame(self)
        #self.line_1.setFrameShape(QtGui.QFrame.HLine)
        #self.line_1.setFrameShadow(QtGui.QFrame.Sunken)

        # Layouts
        layout_buttons_res = QtGui.QGridLayout()
        layout_buttons_res.setContentsMargins(0, 5, 0, 5)
        layout_buttons_res.setHorizontalSpacing(10)

        layout_cmdline_res = QtGui.QHBoxLayout()
        layout_cmdline_res.setContentsMargins(0, 5, 0, 5)
        layout_cmdline_res.setSpacing(5)

        layout_buttons_job = QtGui.QGridLayout()
        layout_buttons_job.setContentsMargins(0, 5, 0, 5)
        layout_buttons_job.setHorizontalSpacing(10)

        sub_layout_job_rm = QtGui.QHBoxLayout()
        sub_layout_job_rm.setSpacing(5)
        sub_layout_job_rm.addWidget(self.label_job_id_1)
        sub_layout_job_rm.addWidget(self.lineEdit_job_id_1)
        sub_layout_job_rm.addWidget(self.pushButton_job_rm_id)

        sub_layout_job_prio = QtGui.QHBoxLayout()
        sub_layout_job_prio.setSpacing(5)
        sub_layout_job_prio.addWidget(self.label_job_id_2)
        sub_layout_job_prio.addWidget(self.lineEdit_job_id_2)
        sub_layout_job_prio.addWidget(self.label_job_prio)
        sub_layout_job_prio.addWidget(self.lineEdit_job_prio)

        # PySide.QtGui.QGridLayout.addLayout(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        #layout_buttons_res.addWidget(self.pushButton_res_all, 1, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        layout_buttons_res.addWidget(self.pushButton_res_all, 0, 0, 1, 1)
        layout_buttons_res.addWidget(self.pushButton_res_job, 0, 1, 1, 1)
        layout_buttons_res.addWidget(self.pushButton_res_avail, 0, 2, 1, 1)
        layout_buttons_res.addWidget(self.pushButton_res_run, 0, 3, 1, 1)
        layout_buttons_res.addWidget(self.pushButton_res_online, 0, 4, 1, 1)
        layout_buttons_res.addWidget(self.pushButton_res_offline, 0, 5, 1, 1)

        layout_cmdline_res.addWidget(self.label_res_cmd)
        layout_cmdline_res.addWidget(self.lineEdit_res_cmd)

        # PySide.QtGui.QGridLayout.addLayout(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        layout_buttons_job.addWidget(self.pushButton_job_show_que, 0, 0, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_show_details, 1, 0, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_analyze, 0, 1, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_show_all, 1, 1, 1, 1)

        layout_buttons_job.addLayout(sub_layout_job_rm, 0, 2, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_rm_all, 1, 2, 1, 1)

        layout_buttons_job.addLayout(sub_layout_job_prio, 0, 3, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_edit_prio, 1, 3, 1, 1)

        layout_buttons_job.addWidget(self.pushButton_job_start_job, 0, 4, 1, 1)
        layout_buttons_job.addWidget(self.pushButton_job_start_dag, 1, 4, 1, 1)

        # necessary for uniform column width
        layout_buttons_job.setColumnMinimumWidth(0, 1)
        layout_buttons_job.setColumnMinimumWidth(1, 1)
        layout_buttons_job.setColumnMinimumWidth(2, 1)
        layout_buttons_job.setColumnMinimumWidth(3, 1)
        layout_buttons_job.setColumnMinimumWidth(4, 1)
        layout_buttons_job.setColumnStretch(0, 1)
        layout_buttons_job.setColumnStretch(1, 1)
        layout_buttons_job.setColumnStretch(2, 1)
        layout_buttons_job.setColumnStretch(3, 1)
        layout_buttons_job.setColumnStretch(4, 1)

        # Combine layouts
        layout_upper.addWidget(self.label_res)
        layout_upper.addWidget(self.textbrowser_res)
        layout_upper.addLayout(layout_buttons_res)
        layout_upper.addLayout(layout_cmdline_res)

        layout_lower.addWidget(self.label_job)
        layout_lower.addWidget(self.textbrowser_job)
        layout_lower.addLayout(layout_buttons_job)

        # Frames
        frame_upper = QtGui.QFrame()
        frame_upper.setLayout(layout_upper)
        frame_upper.setFrameShape(QtGui.QFrame.NoFrame)
        frame_upper.setFrameShadow(QtGui.QFrame.Sunken)

        frame_lower = QtGui.QFrame()
        frame_lower.setLayout(layout_lower)
        frame_lower.setFrameShape(QtGui.QFrame.NoFrame)
        frame_lower.setFrameShadow(QtGui.QFrame.Sunken)

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(frame_upper)
        splitter.addWidget(frame_lower)

        layout_main.addWidget(splitter)
        self.setLayout(layout_main)

        # Short cuts
        #QtGui.QShortcut(QtGui.QKeySequence('Ctrl+R'), self, self.refresh)
        #QtGui.QShortcut(QtGui.QKeySequence('Ctrl+S'), self, self.export_fitness)
        #QtGui.QShortcut(QtGui.QKeySequence('Ctrl+C'), self, self.calculate_fitness)
