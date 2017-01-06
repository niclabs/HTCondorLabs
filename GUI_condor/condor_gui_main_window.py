#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Condor GUI
# Copyright (c) 2016, Bartosz Dziubaczyk and Andreas Wünsch. All rights reserved.
# BSD license (Condor_GUI.chm or Condor_GUI.pdf for details).
#

import os
import sys
import subprocess  # for os operations on unix like systems

from PySide import QtCore, QtGui

import condor_gui_central_widget
import condor_gui_create_job
import condor_gui_create_dag
import condor_gui_edit_config
import condor_gui_about

import condor_gui_resource_icon
import condor_gui_resource_doc

"""
The main window which contains the central and the main functions.
"""

class MainWindow(QtGui.QMainWindow):

    def __init__(self, cwd, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('Condor GUI')
        #self.setWindowIcon(QtGui.QIcon('icon_condor_gui.png'))

        #self.setWindowIcon(QtGui.QIcon(':/icon_condor_gui.ico'))
        self.setWindowIcon(QtGui.QIcon(':/icon_condor_gui.png'))

        # Size
        self.resize(960, 960)

        # Variables
        self.current_dir = cwd
        self.current_dialog_dir = cwd

        # Central widget
        self.central_widget = condor_gui_central_widget.CentralWidget(self)
        self.setCentralWidget(self.central_widget)

        # Menu Bar
        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(QtGui.QAction('New Job', self, shortcut='Ctrl+J', statusTip='Create new job file', triggered=self.create_job))
        file_menu.addAction(QtGui.QAction('New DAG', self, shortcut='Ctrl+D', statusTip='Create new DAG file', triggered=self.create_dag))
        file_menu.addAction(QtGui.QAction('Quit', self, shortcut='Ctrl+Q', triggered=self.close))

        res_menu = self.menuBar().addMenu('&Resources')
        res_menu.addAction(QtGui.QAction('Show all Attributes', self, statusTip='Command: condor_status -long', triggered=self.res_long))
        res_menu.addAction(QtGui.QAction('Show Limits', self, statusTip='Command: condor_config_val -negotiator -dump LIMIT', triggered=self.res_limits))

        help_menu = self.menuBar().addMenu('&Help')
        help_menu.addAction(QtGui.QAction('Contents', self, shortcut='F1', statusTip='Show help contents (F1)', triggered=self.help_chm))
        help_menu.addAction(QtGui.QAction('PDF', self, statusTip='Show help PDF', triggered=self.help_pdf))
        help_menu.addAction(QtGui.QAction('Condor Manual', self, statusTip='Visit http://research.cs.wisc.edu/htcondor/manual/', triggered=self.condor_manual))
        help_menu.addSeparator()
        help_menu.addAction(QtGui.QAction('About', self, triggered=self.about))

        # Status Bar
        self.statusbar = self.statusBar()

        # Processes
        self.process_res = QtCore.QProcess(self)
        self.process_job = QtCore.QProcess(self)

        if self.current_dialog_dir:
            self.process_res.setWorkingDirectory(self.current_dialog_dir)
            self.process_job.setWorkingDirectory(self.current_dialog_dir)

        # show_mode
        self.show_mode_res = 'all'
        self.show_mode_job = 'queue'

        # for storing last commands
        self.list_commands = []
        self.index_command = 0

        # Signals
        # Buttons
        self.central_widget.pushButton_res_all.clicked.connect(self.res_all)
        self.central_widget.pushButton_res_job.clicked.connect(self.res_job)
        self.central_widget.pushButton_res_avail.clicked.connect(self.res_avail)
        self.central_widget.pushButton_res_run.clicked.connect(self.res_run)
        self.central_widget.pushButton_res_online.clicked.connect(self.res_online)
        self.central_widget.pushButton_res_offline.clicked.connect(self.res_offline)

        self.central_widget.pushButton_job_show_que.clicked.connect(self.job_que)
        self.central_widget.pushButton_job_show_all.clicked.connect(self.job_all)
        self.central_widget.pushButton_job_show_details.clicked.connect(self.job_detailed)
        self.central_widget.pushButton_job_analyze.clicked.connect(self.job_analyze)

        self.central_widget.pushButton_job_rm_id.clicked.connect(self.job_rm_id)
        self.central_widget.pushButton_job_rm_all.clicked.connect(self.job_rm_all)
        self.central_widget.pushButton_job_edit_prio.clicked.connect(self.job_edit_prio)
        self.central_widget.pushButton_job_start_job.clicked.connect(self.job_start_job)
        self.central_widget.pushButton_job_start_dag.clicked.connect(self.job_start_dag)

        # Enter pressed in line edits
        self.central_widget.lineEdit_res_cmd.returnPressed.connect(self.run_commandline)
        self.central_widget.lineEdit_job_id_1.returnPressed.connect(self.job_rm_id)
        self.central_widget.lineEdit_job_id_2.returnPressed.connect(self.job_edit_prio)
        self.central_widget.lineEdit_job_prio.returnPressed.connect(self.job_edit_prio)

        # Make sure new Info gets all output and error
        self.process_res.readyReadStandardOutput.connect(self.out_info_res)
        self.process_res.readyReadStandardError.connect(self.err_info_res)

        self.process_job.readyReadStandardOutput.connect(self.out_info_job)
        self.process_job.readyReadStandardError.connect(self.err_info_job)

        # Timer
        self.timer_res = QtCore.QTimer()
        self.timer_res.timeout.connect(self.show_res)

        self.timer_job = QtCore.QTimer()
        self.timer_job.timeout.connect(self.show_job)

        # show resources and jobs
        self.show_res()
        self.show_job()

    #def get_cwd(self):
    #    """
    #    Returns current working directory.
    #    """
    #    current_dir = os.getcwd()
    #    return current_dir

    def get_install_dir(self):
        """
        Returns current install directory, where the exe is.
        """
        install_dir = os.getcwd()
        return install_dir

    #############################################################################
    # Resources
    #############################################################################
    def show_res(self):
        """
        Show resources by running condor_status
        """
        #print('show_res', time.strftime('%X %x'), self.show_mode_res)

        # kill running processes
        self.process_res.kill()

        # start timer
        if not self.timer_res.isActive():
            self.timer_res.start(5000)

        # run condor_status
        if self.show_mode_res == 'all':
            self.process_res.start('condor_status')

        elif self.show_mode_res == 'job':
            self.process_res.start('condor_status -autoformat:h Name OpSysName Cpus Memory LoadAvg State KeyboardIdle Activity ActTime JobId')

        elif self.show_mode_res == 'avail':
            self.process_res.start('condor_status -available')

        elif self.show_mode_res == 'run':
            self.process_res.start('condor_status -run')

        elif self.show_mode_res == 'online':
            self.process_res.start('condor_status -constraint Offline=!=True')

        elif self.show_mode_res == 'offline':
            self.process_res.start('condor_status -constraint Offline==True')

        else:
            pass

    def res_all(self):
        """
        Set self.show_mode_res = all and start self.show_res.
        """
        self.show_mode_res = 'all'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_job(self):
        """
        Set self.show_mode_res = all and start self.show_res.
        """
        self.show_mode_res = 'job'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_avail(self):
        """
        Set self.show_mode_res = avail and start self.show_res.
        """
        self.show_mode_res = 'avail'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_run(self):
        """
        Set self.show_mode_res = run and start self.show_res.
        """
        self.show_mode_res = 'run'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_online(self):
        """
        Set self.show_mode_res = online and start self.show_res.
        """
        self.show_mode_res = 'online'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_offline(self):
        """
        Set self.show_mode_res = offline and start self.show_res.
        """
        self.show_mode_res = 'offline'
        self.central_widget.textbrowser_res.clear()
        self.show_res()

    def res_long(self):
        """
        Stop timer and run condor_status -long.
        """
        self.process_res.kill()
        self.timer_res.stop()

        # start command
        self.process_res.start('condor_status -long')

    def res_limits(self):
        """
        Stop timer and run condor_config_val -negotiator -dump LIMIT.
        """
        self.process_res.kill()
        self.timer_res.stop()

        # start command
        self.process_res.start('condor_config_val -negotiator -dump LIMIT')

    #############################################################################
    # Run Commands
    #############################################################################
    def run_commandline(self):
        """
        Run commands from commandline input.
        """
        #print('run_commandline')
        command_text = str(self.central_widget.lineEdit_res_cmd.text())

        # Skip empty commands
        if command_text == '':
            return

        # Create command dependent on OS, Windows needs cmd
        op_sys = sys.platform
        if op_sys == 'win32':
            command = 'cmd.exe /c ' + command_text
        else:
            command = command_text

        self.process_res.kill()
        self.timer_res.stop()

        # storing commands
        if command_text not in self.list_commands:
            self.list_commands.insert(0,command_text)
        else:
            # put current command to the first position
            self.list_commands.remove(command_text)
            self.list_commands.insert(0,command_text)
        self.index_command = 0

        # start command
        self.process_res.start(command)

        # clear commandline
        self.central_widget.lineEdit_res_cmd.clear()

    def run_command(self, command):
        """
        Run given command in console.
        """
        command_text = command

        # Skip empty commands
        if command_text == '':
            return

        # Create command dependent on OS, Windows needs cmd
        op_sys = sys.platform
        if op_sys == 'win32':
            command = 'cmd.exe /c ' + command_text
        else:
            command = command_text

        self.process_res.kill()
        self.timer_res.stop()

        # storing commands
        if command_text not in self.list_commands:
            self.list_commands.insert(0,command_text)
        else:
            # put current command to the first position
            self.list_commands.remove(command_text)
            self.list_commands.insert(0,command_text)
        self.index_command = 0

        # start command
        self.process_res.start(command)

        # clear commandline
        self.central_widget.lineEdit_res_cmd.clear()

    def keyPressEvent(self, event):
        """
        keypress events for arrow up, down and Escape
        """
        if event.key() == QtCore.Qt.Key_Up:
            self.count_up()
        elif event.key() == QtCore.Qt.Key_Down:
            self.count_down()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.central_widget.lineEdit_res_cmd.clear()
        else:
            pass

    def count_up(self):
        """
        Walk through the list_commands and set current element to lineEdit_res_cmd
        """
        if self.list_commands:
            if self.index_command < len(self.list_commands):
                self.central_widget.lineEdit_res_cmd.setText(self.list_commands[self.index_command])
                self.index_command += 1

            else:
                return
        else:
            return

    def count_down(self):
        """
        Walk through the list_commands and set current element to lineEdit_res_cmd
        """
        if self.list_commands:

            if self.index_command > 1:
                self.central_widget.lineEdit_res_cmd.setText(self.list_commands[self.index_command-2])
                self.index_command -= 1

            else:
                return
        else:
            return

    def out_info_res(self):
        out_string = self.process_res.readAllStandardOutput()

        # decode, codec IBM 850
        codec = QtCore.QTextCodec.codecForName('IBM 850')
        out_string = codec.toUnicode(out_string)
        out_string = out_string.strip('\r\n')
        #print('out_string',[out_string])
        self.central_widget.textbrowser_res.setText(out_string)

    def err_info_res(self):
        err_string = self.process_res.readAllStandardError()

        # decode, codec IBM 850
        codec = QtCore.QTextCodec.codecForName('IBM 850')
        err_string = codec.toUnicode(err_string)
        err_string = err_string.strip('\r\n')
        #print('err_string',[err_string])
        self.central_widget.textbrowser_res.setText(err_string)

    #############################################################################
    # Jobs
    #############################################################################
    def show_job(self):
        """
        Show jobs by running condor_q
        """
        #print('show_job', time.strftime('%X %x'), self.show_mode_job)

        # kill running processes
        self.process_job.kill()

        # start timer
        if not self.timer_job.isActive():
            self.timer_job.start(5000)

        # run condor_status
        if self.show_mode_job == 'queue':
            self.process_job.start('condor_q -dag')

        elif self.show_mode_job == 'detailed':
            self.process_job.start('condor_q -dag -autoformat ClusterId Owner CMD')
            # -autoformat:h Header doesn't work for and reason

        elif self.show_mode_job == 'all':
            self.process_job.start('condor_q -dag -global')

        else:
            pass

    def job_que(self):
        """
        Set self.show_mode_job = all and start self.show_job.
        """
        self.show_mode_job = 'queue'
        self.central_widget.textbrowser_job.clear()
        self.show_job()

    def job_detailed(self):
        """
        Set self.show_mode_job = all and start self.show_job.
        """
        self.show_mode_job = 'detailed'
        self.central_widget.textbrowser_job.clear()
        self.show_job()

    def job_all(self):
        """
        Set self.show_mode_job = all and start self.show_job.
        """
        self.show_mode_job = 'all'
        self.central_widget.textbrowser_job.clear()
        self.show_job()

    def job_analyze(self):
        """
        Analyze Show jobs by running condor_q -better-analyze -global.
        """
        self.process_job.kill()
        self.timer_job.stop()

        # start command
        self.process_job.start('condor_q -better-analyze -global')

    def job_rm_id(self):
        """
        Remove job by ID.
        """
        self.process_job.kill()
        self.timer_job.stop()

        job_id = self.central_widget.lineEdit_job_id_1.text()

        # skip empty commands
        if job_id == '':
            return

        command = 'condor_rm ' + job_id

        # start command
        self.process_job.start(command)

        # clear line edit
        self.central_widget.lineEdit_job_id_1.clear()

        # restart timer
        self.timer_job.start(5000)

    def job_rm_all(self):
        """
        Remove all jobs.
        """
        self.process_job.kill()
        self.timer_job.stop()

        command = 'condor_rm -all'

        # start command
        self.process_job.start(command)

        # clear line edit
        self.central_widget.lineEdit_job_id_1.clear()

        # restart timer
        self.timer_job.start(5000)

    def job_edit_prio(self):
        """
        Edit priority of job.
        """
        self.process_job.kill()
        self.timer_job.stop()

        job_id = self.central_widget.lineEdit_job_id_2.text()
        job_prio = self.central_widget.lineEdit_job_prio.text()

        # skip empty entries
        if job_id == '' or job_prio == '':
            return

        command = 'condor_prio -p ' + job_prio + ' ' + job_id

        # start command
        self.process_job.start(command)

        # clear line edit
        self.central_widget.lineEdit_job_id_2.clear()
        self.central_widget.lineEdit_job_prio.clear()

        # restart timer
        self.timer_job.start(5000)

    def job_start_job(self):
        """
        Submit job to condor pool
        """
        # Process handling
        self.process_res.kill()
        self.timer_res.stop()
        self.process_job.kill()
        self.timer_job.stop()


        if self.current_dialog_dir:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                dir=self.current_dialog_dir,
                                                                filter='Job files (*.sub *.job *.condor);;All files(*)')

        else:
            jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File',
                                                                filter='Job files (*.sub *.job *.condor);;All files(*)')

        #jobfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open Job File', filter='Job files (*.job *.condor);;All files(*)')

        # check empty file selection
        if jobfile:
            jobfile = os.path.realpath(jobfile)
            self.current_dir = os.path.dirname(jobfile)
            self.current_dialog_dir = os.path.dirname(jobfile)

            command = 'condor_submit ' + jobfile

            # start command
            self.process_job.setWorkingDirectory(self.current_dir)
            self.process_job.start(command)

        else:
            pass

        # restart timer
        self.timer_res.start(5000)
        self.timer_job.start(5000)

    def job_start_dag(self):
        """
        Submit job to condor pool
        """
        # Process handling
        self.process_res.kill()
        self.timer_res.stop()
        self.process_job.kill()
        self.timer_job.stop()

        if self.current_dialog_dir:
            dagfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open DAG File',
                                                                dir=self.current_dialog_dir,
                                                                filter='DAG files (*.dag);;All files(*)')

        else:
            dagfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open DAG File',
                                                                filter='DAG files (*.dag);;All files(*)')

        #dagfile, filter = QtGui.QFileDialog.getOpenFileName(self, caption='Open DAG File', filter='DAG files (*.dag);;All files(*)')

        if dagfile:
            dagfile = os.path.realpath(dagfile)
            self.current_dir = os.path.dirname(dagfile)
            self.current_dialog_dir = os.path.dirname(dagfile)

            command = 'condor_submit_dag -f ' + dagfile

            # start command
            self.process_job.setWorkingDirectory(self.current_dir)
            self.process_job.start(command)

        else:
            pass

        # restart timer
        self.timer_res.start(5000)
        self.timer_job.start(5000)

    def out_info_job(self):
        out_string = self.process_job.readAllStandardOutput()

        # decode, codec IBM 850
        codec = QtCore.QTextCodec.codecForName('IBM 850')
        out_string = codec.toUnicode(out_string)
        out_string = out_string.strip('\r\n')
        #print('out_string',[out_string])
        self.central_widget.textbrowser_job.setText(out_string)

    def err_info_job(self):
        err_string = self.process_job.readAllStandardError()

        # decode, codec IBM 850
        codec = QtCore.QTextCodec.codecForName('IBM 850')
        err_string = codec.toUnicode(err_string)
        err_string = err_string.strip('\r\n')
        #print('err_string',[err_string])
        self.central_widget.textbrowser_job.setText(err_string)

    #############################################################################
    # Files
    #############################################################################
    def create_job(self):
        """
        Opens class CreateJobWindow, an editor window to create and edit a job file.
        """

        self.createJobWindow = condor_gui_create_job.CreateJobWindow(current_dialog_dir=self.current_dialog_dir, parent=self)
        self.createJobWindow.show()

    def create_dag(self):
        """
        Opens class CreateJobWindow, an editor window to create and edit a job file.
        """

        self.createDAGWindow = condor_gui_create_dag.CreateDAGWindow(current_dialog_dir=self.current_dialog_dir, parent=self)
        self.createDAGWindow.show()

    
    #############################################################################
    # Help
    #############################################################################
    def help_chm(self):
        """
        Show help.
        """
        install_dir = self.get_install_dir()
        doc_dir = os.path.join(install_dir, 'doc')

        # doc dir exist
        if os.path.isdir(doc_dir):
            list_dir_content=os.listdir(doc_dir)

            for i in list_dir_content:
                if i.endswith('chm'):
                    self.open_file(os.path.join(doc_dir, i))
                else:
                    pass

        # use helpfile in current dir
        elif os.path.isfile(os.path.join(install_dir,'Condor_GUI.chm')):
            self.open_file(os.path.join(install_dir,'Condor_GUI.chm'))

        # copy chm file from resource to file
        else:
            resourceFile = QtCore.QFile(':/doc/Condor_GUI.chm')
            destFile = QtCore.QFile('Condor_GUI.chm')

            #print('filename', resourceFile.fileName())
            #print('exist', resourceFile.exists())

            if resourceFile.exists():
                if not resourceFile.open(QtCore.QIODevice.ReadOnly):
                    QtGui.QMessageBox.warning(self, 'Help', 'Error while reading resource file.', QtGui.QMessageBox.Ok)
                    return

                if not destFile.open(QtCore.QIODevice.WriteOnly):
                    QtGui.QMessageBox.warning(self, 'Help', 'Error while writing help file.', QtGui.QMessageBox.Ok)
                    return

                # Write resource to destFile
                destFile.write(resourceFile.readAll())

                destFile.waitForBytesWritten(2000)
                destFile.waitForReadyRead(2000)
                destFile.close()

                # open destFile
                self.open_file(destFile.fileName())

            else:
                QtGui.QMessageBox.warning(self, 'Help',
                                        'Couldn\'t find helpfile in QtResource',
                                        QtGui.QMessageBox.Ok)

    def help_pdf(self):
        """
        Show help.
        """
        install_dir = self.get_install_dir()
        doc_dir = os.path.join(install_dir, 'doc')

        # doc dir exist
        if os.path.isdir(doc_dir):
            list_dir_content=os.listdir(doc_dir)

            for i in list_dir_content:
                if i.endswith('pdf'):
                    self.open_file(os.path.join(doc_dir, i))
                else:
                    pass

        # use helpfile in current dir
        elif os.path.isfile(os.path.join(install_dir,'Condor_GUI.pdf')):
            self.open_file(os.path.join(install_dir,'Condor_GUI.pdf'))

        # copy chm file from resource to file
        else:
            resourceFile = QtCore.QFile(':/doc/Condor_GUI.pdf')
            destFile = QtCore.QFile('Condor_GUI.pdf')

            #print('filename', resourceFile.fileName())
            #print('exist', resourceFile.exists())

            if resourceFile.exists():
                if not resourceFile.open(QtCore.QIODevice.ReadOnly):
                    QtGui.QMessageBox.warning(self, 'Help', 'Error while reading resource file.', QtGui.QMessageBox.Ok)
                    return

                if not destFile.open(QtCore.QIODevice.WriteOnly):
                    QtGui.QMessageBox.warning(self, 'Help', 'Error while writing help file.', QtGui.QMessageBox.Ok)
                    return

                # Write resource to destFile
                destFile.write(resourceFile.readAll())

                destFile.waitForBytesWritten(2000)
                destFile.waitForReadyRead(2000)
                destFile.close()

                # open destFile
                self.open_file(destFile.fileName())

            else:
                QtGui.QMessageBox.warning(self, 'Help',
                                        'Couldn\'t find helpfile in QtResource',
                                        QtGui.QMessageBox.Ok)

    def condor_manual(self):
        """
        Show Condor manual.
        """
        #QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://research.cs.wisc.edu/htcondor/manual/', QtCore.QUrl.TolerantMode))
        QtGui.QDesktopServices.openUrl('http://research.cs.wisc.edu/htcondor/manual/')

    def about(self):
        """
        Show about information
        """
        #self.aboutWindow = condor_gui_about_widget.NOAWidget(self)
        self.aboutWindow = condor_gui_about.AboutWidget(self)
        self.aboutWindow.show()

        return

        #QtGui.QMessageBox.about(self, 'About Condor GUI',
        #    'Condor GUI\n'
        #    'Version ' + condor_gui_version.__version__ + '\n\n'
        #    'Copyright (c) 2015, Bartosz Dziubaczyk and Andreas Wünsch.\n'
        #    'All rights reserved.\n\n'
        #    'See \'License Information\' or help for licensing information and included modules.')

    def open_file(self, filename):
        """
        Open files dependent on platform, os.startfile doesn't work on unix.
        """
        # Windows
        if sys.platform == 'win32':
            os.startfile(filename)

        # MacOS
        elif sys.platform == 'darwin':
            opener = 'open'
            subprocess.call([opener, filename])

        # Linux
        elif sys.platform == 'linux':

            opener = 'xdg-open'

            try:
                returncode = subprocess.check_call([opener, filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                #print('returncode ', returncode)

            except subprocess.CalledProcessError as e:
                output = e.output
                returncode = e.returncode

                #print('output ', output)
                #print('returncode ', returncode)

                QtGui.QMessageBox.warning(self, 'Help',
                                          'Error while opening ' + filename
                                          + '\nPlease install software to open file.',
                                          QtGui.QMessageBox.Ok)

        else:
            QtGui.QMessageBox.warning(self, 'Help',
                                      'Platform ist not supported.',
                                      QtGui.QMessageBox.Ok)
