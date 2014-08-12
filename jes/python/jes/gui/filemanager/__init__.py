# -*- coding: utf-8 -*-
"""
jes.gui.filemanager
===================
This manages creating, opening, saving, and reading files into the editor.

:copyright: (C) 2014 Matthew Frazier and Mark Guzdial
:license:   GNU GPL v2 or later, see jes/help/JESCopyright.txt for details
"""
from __future__ import with_statement
import JESConfig
import os.path
from blinker import NamedSignal
from java.io import File, FileWriter
from javax.swing import JFileChooser, JOptionPane
from jes.gui.components.actions import (methodAction, control, controlShift,
                                        PythonAction)
from jes.gui.components.threading import threadsafe
from .recents import RecentFiles

PROMPT_SAVE_CAPTION = 'Save file?'

PROMPT_NEW_MESSAGE = 'You are about to open a new program area\nWould you like to save the current program first?'
PROMPT_OPEN_MESSAGE = 'You are about to open a file.\nWould you like to save the current program first?'


class FileManager(object):
    def __init__(self, logBuffer):
        self.filename = None

        self.parentWindow = None
        self.editor = None

        self.logBuffer = logBuffer

        self.directory = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH)

        self.onNew = NamedSignal('onNew')
        self.onRead = NamedSignal('onRead')
        self.onWrite = NamedSignal('onWrite')

        self.recentFiles = RecentFiles(self)

    ### Configuration

    def setParentWindow(self, window):
        self.parentWindow = window

    def setEditor(self, editor):
        self.editor = editor


    ### Actions -- can initiate a whole GUI process

    @methodAction(name="New Program", accelerator=control('n'))
    @threadsafe
    def newAction(self):
        if self.continueAfterSaving(PROMPT_NEW_MESSAGE):
            self.newFile()

    @methodAction(name="Open Program...", accelerator=control('o'))
    @threadsafe
    def openAction(self):
        if self.continueAfterSaving(PROMPT_OPEN_MESSAGE):
            chooser = JFileChooser(File(self.directory))
            chooser.setApproveButtonText("Open File")

            returnVal = chooser.showOpenDialog(self.parentWindow)
            if returnVal == 0:
                self.readFile(chooser.getSelectedFile().getPath())

    @methodAction(name="Save Program", accelerator=control('s'))
    @threadsafe
    def saveAction(self):
        if self.filename is not None:
            return self.writeFile(self.filename)
        else:
            return self.saveAsAction()

    @methodAction(name="Save Program As...", accelerator=controlShift('s'))
    @threadsafe
    def saveAsAction(self):
        chooser = JFileChooser(File(self.directory))
        chooser.setApproveButtonText("Save File")

        returnVal = chooser.showSaveDialog(self.parentWindow)
        if returnVal == 0:
            return self.writeFile(chooser.getSelectedFile().getPath())
        else:
            return None

    @threadsafe
    def readAction(self, filename):
        if self.continueAfterSaving(PROMPT_OPEN_MESSAGE):
            self.readFile(filename)


    ### Model methods -- touch the GUI, but carry out their actions instantly

    @threadsafe
    def newFile(self):
        self.editor.setText("")
        self.filename = None

        self.editor.modified = 0

        self.logBuffer.resetBuffer()
        self.onNew.send(self)

    @threadsafe
    def readFile(self, filename):
        filename = os.path.normpath(filename)

        try:
            with open(filename, 'r') as fd:
                self.editor.setText(fd.read().decode('utf8', 'replace'))
        except EnvironmentError, exc:
            self.showErrorMessage(
                "Error opening file", "Could not open the file", filename, exc
            )
        else:
            self.filename = filename
            self.directory = os.path.dirname(filename)

            self.editor.modified = 0

            self.logBuffer.openLogFile(filename)
            self.onRead.send(self, filename=filename)

    @threadsafe
    def writeFile(self, filename):
        sourceText = self.editor.getText().encode('utf8')

        try:
            with open(filename, 'w') as fd:
                fd.write(sourceText)
        except EnvironmentError, exc:
            self.showErrorMessage(
                "Error saving file", "Could not save the file to", filename, exc
            )
        else:
            self.filename = filename
            self.directory = os.path.dirname(filename)

            self.editor.modified = 0

            self.logBuffer.saveLogFile(self.filename)
            self.onWrite.send(self, filename=filename)

            # Now write the backup
            if JESConfig.getInstance().getBooleanProperty(JESConfig.CONFIG_BACKUPSAVE):
                try:
                    backupPath = self.filename + "bak"
                    with open(filename, 'w') as fd:
                        fd.write(sourceText)
                except EnvironmentError, exc:
                    self.showErrorMessage(
                        "Error saving backup",
                        "Could not save the backup file to", backupPath, exc
                    )

            return True


    ### Helpers

    @threadsafe
    def continueAfterSaving(self, prompt):
        if self.editor.modified:
            promptResult = JOptionPane.showConfirmDialog(self.parentWindow,
                prompt, PROMPT_SAVE_CAPTION, JOptionPane.YES_NO_CANCEL_OPTION
            )

            if promptResult == JOptionPane.YES_OPTION:
                isSaved = self.saveAction()
                if isSaved:
                    # The file saved, keep going.
                    return True
                else:
                    # The file _isn't_ saved, bail out.
                    return False
            elif promptResult == JOptionPane.NO_OPTION:
                # The user elected not to save it, so keep going.
                return True
            else:
                # The user decided to cancel, bail out.
                return False
        else:
            return True

    def showErrorMessage(title, prefix, path, exc):
        excMessage = getattr(exc, 'strerror', str(exc))
        message = "%s %s:\n%s" % (prefix, os.path.basename(path), excMessage)
        JOptionPane.showMessageDialog(self.parentWindow, message, title,
                                      JOptionPane.ERROR_MESSAGE)

