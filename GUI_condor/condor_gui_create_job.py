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
An editor window to create and edit a job file.
"""


###############################################################################
###############################################################################
class CreateJobWindow(QtGui.QMainWindow):
    def __init__(self, current_dialog_dir, parent=None):

        super(CreateJobWindow, self).__init__(parent)

        self.setWindowTitle('Create Job File')
        #self.setWindowIcon(QtGui.QIcon('xxx.ico'))

        # Variables
        self.current_dir = None
        if current_dialog_dir:
            self.current_dialog_dir = current_dialog_dir
        else:
            self.current_dialog_dir = os.getcwd()

        self.jobfile = None
        self.undostackIsClean = True

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
        self.label_executable = QtGui.QLabel(self)
        self.label_input_files = QtGui.QLabel(self)
        self.label_input_dir = QtGui.QLabel(self)
        self.label_initial_dir = QtGui.QLabel(self)
        self.label_arguments = QtGui.QLabel(self)
        self.label_rank = QtGui.QLabel(self)
        self.label_req_cpu = QtGui.QLabel(self)
        self.label_req_mem = QtGui.QLabel(self)
        self.label_requirements = QtGui.QLabel(self)
        self.label_group = QtGui.QLabel(self)
        self.label_prio = QtGui.QLabel(self)
        self.label_queue = QtGui.QLabel(self)
        self.label_jobfile = QtGui.QLabel(self)
        self.label_preview = QtGui.QLabel(self)

        self.label_executable.setText('Executable')
        self.label_input_files.setText('Input Files')
        self.label_input_dir.setText('Input Directories')
        self.label_initial_dir.setText('Initial Directory')

        self.label_arguments.setText('Arguments')
        self.label_rank.setText('Rank')
        self.label_req_cpu.setText('Requested CPU')
        self.label_req_mem.setText('Requested Memory')
        self.label_requirements.setText('Requirements')
        
        self.label_group.setText('Group')
        self.label_prio.setText('Priority')
        self.label_queue.setText('Queue')

        self.label_jobfile.setText('Job File')
        self.label_preview.setText('Preview')

        # Buttons
        self.pushButton_executable = QtGui.QPushButton(self)
        self.pushButton_input_files = QtGui.QPushButton(self)
        self.pushButton_input_dir = QtGui.QPushButton(self)
        self.pushButton_initial_dir = QtGui.QPushButton(self)

        self.pushButton_jobfile = QtGui.QPushButton(self)

        self.pushButton_create = QtGui.QPushButton(self)
        self.pushButton_open = QtGui.QPushButton(self)
        self.pushButton_save = QtGui.QPushButton(self)

        self.pushButton_executable.setText('...')
        self.pushButton_input_files.setText('...')
        self.pushButton_input_dir.setText('...')
        self.pushButton_initial_dir.setText('...')
        self.pushButton_jobfile.setText('...')

        self.pushButton_create.setText('Create Job File')
        self.pushButton_open.setText('Open Job File')
        self.pushButton_save.setText('Save Job File')

        # Status tips for buttons
        self.pushButton_executable.setStatusTip('Set executable file')
        self.pushButton_input_files.setStatusTip('Set input files')
        self.pushButton_input_dir.setStatusTip('Set input directories')
        self.pushButton_initial_dir.setStatusTip('Set initial directory')
        self.pushButton_jobfile.setStatusTip('Set job file')

        self.pushButton_create.setStatusTip('Create job file')
        self.pushButton_open.setStatusTip('Open existing job file')
        self.pushButton_save.setStatusTip('Save job file')

        height = 25
        self.pushButton_executable.setFixedHeight(height)
        self.pushButton_input_files.setFixedHeight(height)
        self.pushButton_input_dir.setFixedHeight(height)
        self.pushButton_initial_dir.setFixedHeight(height)

        self.pushButton_jobfile.setFixedHeight(height)

        self.pushButton_create.setFixedHeight(height)
        self.pushButton_open.setFixedHeight(height)
        self.pushButton_save.setFixedHeight(height)

        width = 80
        self.pushButton_executable.setFixedWidth(width)
        self.pushButton_input_files.setFixedWidth(width)
        self.pushButton_input_dir.setFixedWidth(width)
        self.pushButton_initial_dir.setFixedWidth(width)

        self.pushButton_jobfile.setFixedWidth(width)

        self.pushButton_create.setFixedWidth(120)
        self.pushButton_open.setFixedWidth(120)
        self.pushButton_save.setFixedWidth(120)

        # Line edits
        self.lineEdit_executable = QtGui.QLineEdit(self)
        self.lineEdit_input_files = QtGui.QLineEdit(self)
        self.lineEdit_input_dir = QtGui.QLineEdit(self)
        self.lineEdit_initial_dir = QtGui.QLineEdit(self)

        self.lineEdit_arguments = QtGui.QLineEdit(self)
        self.lineEdit_rank = QtGui.QLineEdit(self)
        self.lineEdit_req_cpu = QtGui.QLineEdit(self)
        self.lineEdit_req_mem = QtGui.QLineEdit(self)
        self.lineEdit_requirements = QtGui.QLineEdit(self)
        self.lineEdit_group = QtGui.QLineEdit(self)
        self.lineEdit_jobfile = QtGui.QLineEdit(self)

        self.lineEdit_executable.setFixedHeight(height)
        self.lineEdit_input_files.setFixedHeight(height)
        self.lineEdit_input_dir.setFixedHeight(height)
        self.lineEdit_initial_dir.setFixedHeight(height)

        self.lineEdit_arguments.setFixedHeight(height)
        self.lineEdit_rank.setFixedHeight(height)
        self.lineEdit_req_cpu.setFixedHeight(height)
        self.lineEdit_req_mem.setFixedHeight(height)
        self.lineEdit_requirements.setFixedHeight(height)
        self.lineEdit_group.setFixedHeight(height)
        self.lineEdit_jobfile.setFixedHeight(height)

        self.lineEdit_rank.setFixedWidth(width)
        self.lineEdit_req_cpu.setFixedWidth(width)
        self.lineEdit_req_mem.setFixedWidth(width)

        # Status tips
        self.lineEdit_executable.setStatusTip('Result: executable = <value>')
        self.lineEdit_input_files.setStatusTip('Result: transfer_input_files = <value>')
        self.lineEdit_input_dir.setStatusTip('Result: transfer_input_files = <value>')
        self.lineEdit_initial_dir.setStatusTip('Result: initialdir = <value>')

        self.lineEdit_arguments.setStatusTip('Result: arguments = <value>')
        self.lineEdit_rank.setStatusTip('Result: rank = <value1> && <value2> ...')
        self.lineEdit_req_cpu.setStatusTip('Result: request_cpus = <value>')
        self.lineEdit_req_mem.setStatusTip('Result: request_memory = <value>')
        self.lineEdit_requirements.setStatusTip('Result: requirements = (<value1> =?= True) && (<value2> =?= True) ... and concurrency_limits = <value1> && <value2> ...')
        self.lineEdit_group.setStatusTip('Result: +MyGroup = <value>')
        self.lineEdit_jobfile.setStatusTip('Result: output = <value>.out, error = <value>.err, log = <value>.log')

        # Tool tips
        self.lineEdit_executable.setToolTip('Executable file of job')
        self.lineEdit_input_files.setToolTip('Input files seperated by comma')
        self.lineEdit_input_dir.setToolTip('Input directories seperated by comma')
        self.lineEdit_initial_dir.setToolTip('Initial directory on executing node')

        self.lineEdit_rank.setToolTip('Free rank expression input, seperated by comma')
        self.lineEdit_req_cpu.setToolTip('Request CPU')
        self.lineEdit_req_mem.setToolTip('Request Memory')
        self.lineEdit_requirements.setToolTip('Requirements, e.g. Software on executing node')
        self.lineEdit_group.setToolTip('Preferred group of executing nodes')
        self.lineEdit_jobfile.setToolTip('Job description file (absolute path),\nnecessary to name .out, .err and .log files ')

        # Store regular style of lineEdit_executable
        self.style_lineEdit = self.lineEdit_executable.styleSheet()  # original saved

        # Checkbox
        self.cb_rank_kflops = QtGui.QCheckBox('kflops', self)
        self.cb_rank_memory = QtGui.QCheckBox('memory', self)

        self.cb_rank_kflops.setToolTip('Rank resources by kflops')
        self.cb_rank_memory.setToolTip('Rank resources by memory')

        # Drop Down Menu
        #self.dropDown_rank = QtGui.QComboBox(self)
        #self.dropDown_rank.setFixedHeight(height)
        #dropDownItems = ['kflops', 'memory']
        #self.dropDown_rank.addItems(dropDownItems)
        #self.dropDown_rank.setFixedWidth(width)

        # Spin box
        self.spinBox_prio = QtGui.QSpinBox(self)
        self.spinBox_prio.setRange(-50, 50)
        self.spinBox_prio.setValue(0)
        self.spinBox_prio.setFixedHeight(height)
        self.spinBox_prio.setAlignment(QtCore.Qt.AlignCenter)

        self.spinBox_queue = QtGui.QSpinBox(self)
        self.spinBox_queue.setRange(1, 50)
        self.spinBox_queue.setValue(1)
        self.spinBox_queue.setFixedHeight(height)
        self.spinBox_queue.setAlignment(QtCore.Qt.AlignCenter)

        # line
        #self.line_1 = QtGui.QFrame(self)
        #self.line_1.setFrameShape(QtGui.QFrame.HLine)
        #self.line_1.setFrameShadow(QtGui.QFrame.Sunken)

        # Spacer (w, h)
        self.spacer_1 = QtGui.QSpacerItem(10, 10)
        self.spacer_2 = QtGui.QSpacerItem(10, 10)
        self.spacer_3 = QtGui.QSpacerItem(10, 10)
        self.spacer_4 = QtGui.QSpacerItem(10, 10)
        self.spacer_5 = QtGui.QSpacerItem(10, 10)
        self.spacer_6 = QtGui.QSpacerItem(5, 5)

        # Textedit
        self.textedit = QtGui.QTextEdit(self) # for typing in
        font = QtGui.QFont()
        font.setFamily('Consolas')
        font.setPointSize(9)
        self.textedit.setFont(font)
        self.textedit.setUndoRedoEnabled(True)

        # Layouts
        layout_left = QtGui.QGridLayout()
        layout_left.setContentsMargins(5, 5, 5, 5)
        layout_left.setHorizontalSpacing(10)
        #layout_left.setAlignment(QtCore.Qt.AlignTop)

        layout_right = QtGui.QGridLayout()
        layout_right.setContentsMargins(0, 5, 5, 5)
        #layout_right.setAlignment(QtCore.Qt.AlignTop)

        # PySide.QtGui.QGridLayout.addLayout(arg__1, row, column, rowSpan, columnSpan[, alignment=0])
        #layout_left.addWidget(self.pushButton_executable, 1, 1, 1, 1, alignment=QtCore.Qt.AlignTop)
        layout_left.addWidget(self.label_executable, 0, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_executable, 1, 0, 1, 3)
        layout_left.addWidget(self.pushButton_executable, 1, 3, 1, 1)

        layout_left.addWidget(self.label_input_files, 2, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_input_files, 3, 0, 1, 3)
        layout_left.addWidget(self.pushButton_input_files, 3, 3, 1, 1)

        layout_left.addWidget(self.label_input_dir, 4, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_input_dir, 5, 0, 1, 3)
        layout_left.addWidget(self.pushButton_input_dir, 5, 3, 1, 1)

        layout_left.addWidget(self.label_initial_dir, 6, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_initial_dir, 7, 0, 1, 3)
        layout_left.addWidget(self.pushButton_initial_dir, 7, 3, 1, 1)

        layout_left.addItem(self.spacer_1, 8, 0, 1, 4)
        layout_left.addWidget(self.label_arguments, 9, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_arguments, 9, 1, 1, 3)

        layout_left.addWidget(self.label_rank, 10, 0, 1, 1)
        layout_left.addWidget(self.cb_rank_kflops, 10, 1, 1, 1)
        layout_left.addWidget(self.cb_rank_memory, 10, 2, 1, 1)
        layout_left.addWidget(self.lineEdit_rank, 10, 3, 1, 2)

        layout_left.addWidget(self.label_req_cpu, 11, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_req_cpu, 11, 1, 1, 1)

        layout_left.addWidget(self.label_req_mem, 11, 2, 1, 1, alignment=QtCore.Qt.AlignRight)
        layout_left.addWidget(self.lineEdit_req_mem, 11, 3, 1, 1)

        layout_left.addWidget(self.label_requirements, 12, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_requirements, 12, 1, 1, 3)

        layout_left.addWidget(self.label_group, 13, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_group, 13, 1, 1, 3)

        layout_left.addItem(self.spacer_2, 14, 0, 1, 4)
        layout_left.addWidget(self.label_prio, 15, 0, 1, 1)
        layout_left.addWidget(self.spinBox_prio, 15, 1, 1, 1)

        layout_left.addWidget(self.label_queue, 16, 0, 1, 1)
        layout_left.addWidget(self.spinBox_queue, 16, 1, 1, 1)

        layout_left.addItem(self.spacer_3, 17, 1, 1, 1)
        layout_left.addWidget(self.label_jobfile, 18, 0, 1, 1)
        layout_left.addWidget(self.lineEdit_jobfile, 19, 0, 1, 3)
        layout_left.addWidget(self.pushButton_jobfile, 19, 3, 1, 1)

        layout_left.addItem(self.spacer_4, 20, 1, 1, 1)
        layout_left.addWidget(self.pushButton_create, 21, 2, 1, 2, alignment=QtCore.Qt.AlignRight)

        # necessary for uniform column width
        #layout_left.setColumnMinimumWidth(0, 1)
        #layout_left.setColumnMinimumWidth(1, 1)
        layout_left.setColumnMinimumWidth(2, 1)
        layout_left.setColumnMinimumWidth(3, 1)

        #layout_left.setColumnStretch(0, 2)
        #layout_left.setColumnStretch(1, 1)
        layout_left.setColumnStretch(2, 2)
        layout_left.setColumnStretch(3, 1)

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

        frame_right = QtGui.QFrame()
        frame_right.setLayout(layout_right)
        frame_right.setFrameShape(QtGui.QFrame.NoFrame)
        frame_right.setFrameShadow(QtGui.QFrame.Sunken)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(frame_left)
        splitter.addWidget(frame_right)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

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
        self.pushButton_executable.clicked.connect(self.load_executable)
        self.pushButton_input_files.clicked.connect(self.load_input_files)
        self.pushButton_input_dir.clicked.connect(self.load_input_dir)
        self.pushButton_initial_dir.clicked.connect(self.load_initial_dir)
        self.pushButton_jobfile.clicked.connect(self.set_jobfile_dialog)

        #self.dropDown_rank.activated[str].connect(self.set_rank)

        self.pushButton_create.clicked.connect(self.create_jobfile)
        self.pushButton_open.clicked.connect(self.open)
        self.pushButton_save.clicked.connect(self.save)

        self.textedit.textChanged.connect(self.setUndoStack)
        self.lineEdit_jobfile.returnPressed.connect(self.set_jobfile)

    #############################################################################
    # Job file handling
    #############################################################################
    def create_jobfile(self):
        """
        Create Jobfile from values
        """
        if not self.check_values():
            return

        # Jobfile
        jobfile = self.lineEdit_jobfile.text()
        jobfilename = os.path.splitext(os.path.basename(jobfile))[0]

        str_outfile = '\noutput = ' + jobfilename + '.out' + '\n'
        str_errfile = 'error = ' + jobfilename + '.err' + '\n'
        str_logfile = 'log = ' + jobfilename + '.log' + '\n'

        # Executable
        executable = self.lineEdit_executable.text()
        str_exe = 'executable = ' + executable + '\n\n'

        # Input_files
        input_files = self.lineEdit_input_files.text()
        if input_files != '':
            list_input_files = input_files.split(',')
            list_input_files = [x.strip() for x in list_input_files]
        else:
            list_input_files = []

        # Input_dirs
        input_dirs = self.lineEdit_input_dir.text()
        if input_dirs != '':
            list_input_dirs = input_dirs.split(',')
            list_input_dirs = [x.strip() for x in list_input_dirs]
            list_input_files.extend(list_input_dirs)
        else:
           pass

        # Input_files and input_dirs
        if list_input_files != [] and list_input_files != ['']:
            str_input_files = 'transfer_input_files = ' + ', '.join(list_input_files) + '\n'
        else:
            str_input_files = ''

        # Initial_dir
        initial_dir = self.lineEdit_initial_dir.text()
        if initial_dir != '':
            str_initial_dir = 'initialdir = ' + initial_dir + '\n'
        else:
            str_initial_dir = ''

        # Arguments
        arguments = self.lineEdit_arguments.text()
        if arguments != '':
            str_arguments = 'arguments = ' + arguments + '\n'
        else:
            str_arguments = ''

        # Rank
        list_rank = []
        if self.cb_rank_memory.isChecked():
            list_rank.append('memory')

        if self.cb_rank_kflops.isChecked():
            list_rank.append('kflops')
        rank_text = self.lineEdit_rank.text()
        if rank_text != '':
            rank_text = rank_text.split(',')
            rank_text = [x.strip() for x in rank_text]
            list_rank.extend(rank_text)
        if list_rank:
            str_rank = 'rank = ' + ' && '.join(list_rank) + '\n'
        else:
            str_rank = ''

        # Request_cpu
        req_cpu = self.lineEdit_req_cpu.text()
        if req_cpu != '':
            str_req_cpu = 'request_cpus = ' + req_cpu + '\n'
        else:
            str_req_cpu = ''

        # Request_mem
        req_mem = self.lineEdit_req_mem.text()
        if req_mem != '':
            str_req_mem = 'request_memory = ' + req_mem + '\n'
        else:
            str_req_mem = ''

        # Software
        software = self.lineEdit_requirements.text()
        if software != '':
            list_requirements = software.split(',')
            list_requirements = [x.strip() for x in list_requirements]

            list_req_requirements = ['(' + i + ' =?= True)' for i in list_requirements]
            str_req_requirements = 'requirements = ' + ' && '.join(list_req_requirements) + '\n'
            str_con_requirements = 'concurrency_limits = ' + ', '.join(list_requirements) + '\n'

        else:
            str_req_requirements = ''
            str_con_requirements = ''

        # Group
        group = self.lineEdit_group.text()
        if group != '':
            str_group = '+MyGroup = ' + group + '\n'
        else:
            str_group = ''

        # Priority
        prio = self.spinBox_prio.value()
        str_prio= 'priority = ' + str(prio)

        # queue
        queue = self.spinBox_queue.value()
        str_queue= 'queue ' + str(queue)

        # create outstring
        outstring = \
            '####################' + '\n' + \
            '#' + '\n' + \
            '# HTCondor job file' + '\n' + \
            '#' + '\n' + \
            '####################' + '\n\n' + \
            'universe = vanilla' + '\n\n' + \
            str_exe + \
            str_arguments + \
            str_input_files + \
            str_initial_dir + \
            str_outfile + \
            str_errfile + \
            str_logfile + \
            '\n' + \
            'should_transfer_files = if_needed' + '\n' + \
            'when_to_transfer_output = on_exit' + \
            '\n\n' + \
            str_req_requirements + \
            str_con_requirements + \
            str_rank + \
            str_req_cpu + \
            str_req_mem + \
            str_group + \
            '\n' + \
            str_prio + \
            '\n\n' + \
            str_queue

        self.textedit.setText(outstring)

        self.setWindowTitle('Create Job File (' + self.jobfile + '*)')

    def open(self):
        """
        Open condor_config by file dialog.
        """
        if self.current_dialog_dir:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                dir=self.current_dialog_dir,
                                                                filter='Job files (*.job *.sub *.condor);;All files(*)')

        else:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                filter='Job files (*.job *.sub *.condor);;All files(*)')
        if jobfile:
            self.jobfile = os.path.realpath(jobfile)
            self.current_dialog_dir = os.path.dirname(self.jobfile)

            with open(self.jobfile,'r') as file:
                file_content = file.read()
                self.textedit.setText(file_content)

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            #print('undostackIsClean',self.undostackIsClean)
            self.setWindowTitle('Create Job File (' + self.jobfile + ')')

            # Set jobfile
            self.lineEdit_jobfile.setText(self.jobfile)

            # Parse file content
            file_content = file_content.split('\n')
            for line in file_content:
                if line.startswith('executable'):
                    executable = line.split('=')[-1].strip()
                    self.lineEdit_executable.setText(executable)

                elif line.startswith('arguments'):
                    arguments = line.split('=')[-1].strip()
                    self.lineEdit_arguments.setText(arguments)

                elif line.startswith('transfer_input_files'):
                    input_files = []
                    input_dirs = []
                    transfer_input_files_str = line.split('=')[-1]
                    transfer_input_files = transfer_input_files_str.split(',')
                    transfer_input_files = [x.strip() for x in transfer_input_files]

                    # Separate files and directories
                    for file in transfer_input_files:
                        if '.' in file:
                            input_files.append(file)
                        else:
                            input_dirs.append(file)

                    self. lineEdit_input_files.setText(', '.join(input_files))
                    self. lineEdit_input_dir.setText(', '.join(input_dirs))

                elif line.startswith('initialdir'):
                    initialdir = line.split('=')[-1].strip()
                    self.lineEdit_initial_dir.setText(initialdir)

                elif line.startswith('requirements'):
                    req_list = []
                    req_items_str = line.split('requirements')[-1]
                    req_items_str = req_items_str.replace('=?=', '<>')
                    req_items_str = req_items_str.replace('==', '<>')
                    req_items_str = req_items_str.replace('=', '')
                    req_items_str = req_items_str.replace('(', '')
                    req_items_str = req_items_str.replace(')', '')
                    req_items_str = req_items_str.replace(' ', '')
                    req_items = req_items_str.split('&&')

                    for req_item in req_items:
                        req_item_list = req_item.split('<>')
                        if req_item_list[-1] == 'True' or req_item_list[-1] == 'true' or req_item_list[-1] == 'TRUE':
                            req_list.append(req_item_list[0])
                    self.lineEdit_requirements.setText(', '.join(req_list))

                elif line.startswith('rank'):
                    rank_items_str = line.split('=')[-1].strip()
                    rank_items = rank_items_str.split('&&')
                    rank_items = [x.strip() for x in rank_items]

                    if 'memory' in rank_items:
                        self.cb_rank_memory.setChecked(True)
                        rank_items = [x for x in rank_items if x != 'memory']
                    if 'kflops' in rank_items:
                        self.cb_rank_kflops.setChecked(True)
                        rank_items = [x for x in rank_items if x != 'kflops']
                    self.lineEdit_rank.setText(', '.join(rank_items))

                elif line.startswith('request_cpus'):
                    request_cpus = line.split('=')[-1].strip()
                    self.lineEdit_req_cpu.setText(request_cpus)

                elif line.startswith('request_memory'):
                    request_memory = line.split('=')[-1].strip()
                    self.lineEdit_req_mem.setText(request_memory)

                elif line.startswith('+MyGroup'):
                    group = line.split('=')[-1].strip()
                    self.lineEdit_group.setText(group)

                elif line.startswith('priority'):
                    priority = line.split('=')[-1].strip()
                    self.spinBox_prio.setValue(int(priority))

                elif line.startswith('queue'):
                    queue = line.split(' ')[-1].strip()
                    self.spinBox_queue.setValue(int(queue))
        else:
            pass

    def save(self):
        """
        Save jobfile
        """
        if self.jobfile:
            with open(self.jobfile,'wt') as file:
                file.write(self.textedit.toPlainText())

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            self.setWindowTitle('Create Job File (' + self.jobfile + ')')

        else:
            self.saveAs()

    def saveAs(self):
        """
        Save jobfile to a different directory pulled out of a file dialog.
        """
        self.filename_new, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Save Job File',
                                                                      dir=self.current_dialog_dir,
                                                                      filter='Job files (*.job *.sub *.condor);;All files(*)')
        if self.filename_new:
            self.jobfile = os.path.realpath(self.filename_new)
            self.current_dialog_dir = os.path.dirname(self.jobfile)

            with open(self.jobfile,'wt') as file:
                    file.write(self.textedit.toPlainText())

            # Cleaning undostack and windowtitle
            self.undostackIsClean = True
            self.setWindowTitle('Create Job File (' + self.jobfile + ')')

        else:
            pass

    def check_values(self):
        """
        Check some necessary values (jobfile and executable) on left side and return True if values are ok.
        """
        state_ok = True

        # Jobfile
        jobfile = self.lineEdit_jobfile.text()
        self.set_jobfile()

        #if jobfile != '' and os.path.isfile(jobfile):
        if jobfile != '':

            self.lineEdit_jobfile.setStyleSheet(self.style_lineEdit)  # original style
            self.current_dir = os.path.dirname(jobfile)
        else:
            self.lineEdit_jobfile.setStyleSheet('border: 1px solid red;')  # red style
            state_ok = False
            return state_ok

        # Executable
        exe_file = self.lineEdit_executable.text()

        #if exe_file != '' and os.path.isfile(os.path.join(self.current_dir, exe_file)):
        if exe_file != '':
            self.lineEdit_executable.setStyleSheet(self.style_lineEdit)  # original style
        else:
            self.lineEdit_executable.setStyleSheet('border: 1px solid red;')  # red style
            state_ok = False

        return state_ok

    #############################################################################
    # Set Values on left side
    #############################################################################
    def load_executable(self):
        """
        Dialog to open executable.
        """
        if self.current_dialog_dir:
            exefile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Executable File',
                                                                dir=self.current_dialog_dir,
                                                                filter='All files(*)')

        else:
            exefile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Executable File',
                                                                filter='All files(*)')
        if exefile:
            exefile = os.path.realpath(exefile)
            self.current_dialog_dir = os.path.dirname(exefile)
            exefile = os.path.basename(exefile)
            self.lineEdit_executable.setText(exefile)
        else:
            pass

    def load_input_files(self):
        """
        Dialog to open input_files.
        """
        if self.current_dialog_dir:
            input_files, filter = QtGui.QFileDialog.getOpenFileNames(self, caption='Open Input Files',
                                                                     dir=self.current_dialog_dir,
                                                                     filter='All files(*)')
        else:
            input_files, filter = QtGui.QFileDialog.getOpenFileNames(self, caption='Open Input Files',
                                                                     filter='All files(*)')
        if input_files:
            list_input_files_new = []
            for input_file in input_files:

                input_file = os.path.realpath(input_file)

                # set current dir
                self.current_dialog_dir = os.path.dirname(input_file)

                # get basename
                input_file = os.path.basename(input_file)

                list_input_files_new.append(input_file)

            # handle existing entries in line edit
            list_input_files = self.lineEdit_input_files.text().split(',')
            list_input_files = [x.strip() for x in list_input_files]

            # handle empty list
            if list_input_files == ['']:
                list_input_files = list_input_files_new
            else:
                list_input_files.extend(list_input_files_new)

            # remove duplicates
            list_input_files = list(set(list_input_files))

            # fill line edit
            self.lineEdit_input_files.setText(', '.join(list_input_files))
        else:
            pass

    def load_input_dir(self):
        """
        Dialog to open input_ dirs.
        """
        if self.current_dialog_dir:
            input_dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Open Input Directory',
                                                                     dir=self.current_dialog_dir)
        else:
            input_dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Open Input Directory')

        if input_dir:
            # set current dir
            self.current_dialog_dir = os.path.dirname(input_dir)

            # get basename
            input_dir = os.path.basename(input_dir)

            # handle existing entries in line edit
            list_input_dirs = self.lineEdit_input_dir.text().split(',')
            list_input_dirs = [x.strip() for x in list_input_dirs]

            # handle empty list
            if list_input_dirs == ['']:
                list_input_dirs = [input_dir]
            else:
                list_input_dirs.append(input_dir)

            # remove duplicates
            list_input_dirs = list(set(list_input_dirs))

            # fill line edit
            self.lineEdit_input_dir.setText(', '.join(list_input_dirs))
        else:
            pass

    def load_initial_dir(self):
        """
        Dialog to open initial_dir.
        """
        if self.current_dialog_dir:
            initial_dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Open Input Directory',
                                                                     dir=self.current_dialog_dir)
        else:
            initial_dir = QtGui.QFileDialog.getExistingDirectory(self, caption='Open Input Directory')

        if initial_dir:
            # set current dir
            self.current_dialog_dir = os.path.dirname(initial_dir)

            # get basename
            #initial_dir = os.path.basename(initial_dir)

            # fill line edit
            self.lineEdit_initial_dir.setText(initial_dir)
        else:
            pass

    def set_rank(self, rank):
        """
        Set rank by using drop down menu
        """

        # handle existing entries in line edit
        list_rank = self.lineEdit_rank.text().split(',')
        list_rank = [x.strip() for x in list_rank]

        # handle empty list
        if list_rank == ['']:
            list_rank = [rank]
        else:
            list_rank.append(rank)

        # remove duplicates
        list_rank = list(set(list_rank))

        # fill line edit
        self.lineEdit_rank.setText(', '.join(list_rank))

    def set_jobfile(self):
        """
        Set jobfile by pressing enter in line_edit or creating jobdile
        """
        jobfilename = self.lineEdit_jobfile.text()

        if jobfilename != '':

            # Check file extension and add in necessary
            if not '.' in jobfilename:
                file_ext = 'job'
                jobfile = os.path.join(self.current_dialog_dir, jobfilename + '.' + file_ext)
            else:
                jobfile = os.path.join(self.current_dialog_dir, jobfilename)

            self.jobfile = jobfile
            self.lineEdit_jobfile.setText(jobfile)
        else:
            pass

    def set_jobfile_dialog(self):
        """
        Dialog to set jobfile.
        """
        if self.current_dialog_dir:
            jobfile, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Set Job File',
                                                                dir=self.current_dialog_dir,
                                                                filter='Job files (*.job *.sub *.condor);;All files(*)')

        else:
            jobfile, filter = QtGui.QFileDialog.getSaveFileName(self, caption='Set Job File',
                                                                filter='Job files (*.job *.sub *.condor);;All files(*)')

        if jobfile:
            jobfile = os.path.realpath(jobfile)
            self.jobfile = jobfile
            self.current_dir = os.path.dirname(jobfile)
            self.current_dialog_dir = os.path.dirname(jobfile)
            self.lineEdit_jobfile.setText(jobfile)
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

        if self.jobfile:
            #print('If',self.filename)
            self.setWindowTitle('Create Job File (' + self.jobfile + '*)')
        else:
            #print('Else',self.filename)
            self.setWindowTitle('Create Job File*')

    def closeEvent(self, event):
        """
        Ask "are you sure" if there are unsaved changes.
        """

        if not self.undostackIsClean and self.jobfile:

            reply = QtGui.QMessageBox.question(self, 'Notice', 'File is not saved. Save it before quitting?',
                                               QtGui.QMessageBox.Yes|QtGui.QMessageBox.No|QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Yes:
                if self.jobfile:
                    self.save()
                else:
                    self.saveAs()

            elif reply == QtGui.QMessageBox.No:
                event.accept()

            elif reply == QtGui.QMessageBox.Cancel:
                event.ignore()

            else:
                event.ignore()
