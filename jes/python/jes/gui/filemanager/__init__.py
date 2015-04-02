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
import re
from blinker import NamedSignal
from java.io import File, FileWriter
from javax.swing import JOptionPane
from jes.gui.components.actions import (methodAction, control, controlShift,
                                        PythonAction)
from jes.gui.components.filechooser import FileChooser
from jes.gui.components.threading import threadsafe
from .printing import printFile
from .recents import RecentFiles

MODULE_NAME_RE = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*\.py$')

PROMPT_SAVE_CAPTION = 'Save file?'
PROMPT_SAVE_OR_DISCARD = 'Would you like to save the open program first?'
PROMPT_SAVE_REQUIRED = 'Would you like to save the program and continue?'

PROMPT_NEW_MESSAGE = 'You are about to create a new, blank program.'
PROMPT_OPEN_MESSAGE = 'You are about to open a different program.'
PROMPT_PRINT_MESSAGE = 'You must save the file that you are working\non before printing it.'

class FileManager(object):
    def __init__(self):
        self.filename = None

        self.parentWindow = None
        self.editor = None

        self.createFileChooser()

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
        if self.continueAfterSavingOrDiscarding(PROMPT_NEW_MESSAGE):
            self.newFile()

    @methodAction(name="Open Program...", accelerator=control('o'))
    @threadsafe
    def openAction(self):
        if self.continueAfterSavingOrDiscarding(PROMPT_OPEN_MESSAGE):
            programToOpen = self.selectProgramToOpen()
            if programToOpen is not None:
                self.readFile(programToOpen)

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
        targetFile = self.selectProgramToSave()
        if targetFile is not None:
            self.writeFile(targetFile)

    @threadsafe
    def readAction(self, filename):
        if self.continueAfterSavingOrDiscarding(PROMPT_OPEN_MESSAGE):
            self.readFile(filename)

    @methodAction(name="Print", accelerator=control('p'))
    @threadsafe
    def printAction(self):
        if self.continueAfterSaving(PROMPT_PRINT_MESSAGE):
            try:
                printFile(self.filename)
            except Exception, exc:
                self.showErrorMessage(
                    "Error printing", "Could not print the file",
                    self.filename, exc
                )


    ### Model methods -- touch the GUI, but carry out their actions instantly

    @threadsafe
    def newFile(self):
        self.editor.setText("")
        self.filename = None

        self.editor.modified = 0

        self.onNew.send(self)

    @threadsafe
    def readFile(self, filename):
        filename = os.path.abspath(os.path.normpath(filename))

        try:
            with open(filename, 'r') as fd:
                self.editor.setText(fd.read().encode('ascii','replace')) #decode('utf8', 'replace'))
        except EnvironmentError, exc:
            self.showErrorMessage(
                "Error opening file", "Could not open the file", filename, exc
            )
        else:
            self.filename = filename
            self.lastDirectory = os.path.dirname(filename)

            self.editor.modified = 0

            self.onRead.send(self, filename=filename)

    @threadsafe
    def writeFile(self, filename):
        filename = os.path.abspath(os.path.normpath(filename))
        sourceText = self.editor.getText().encode('utf8')
        sourceText = sourceText.replace("\r\n","\n") # Deal with Windows file endings

        try:
            with open(filename, 'w') as fd:
                fd.write(sourceText)
        except EnvironmentError, exc:
            self.showErrorMessage(
                "Error saving file", "Could not save the file to", filename, exc
            )
        else:
            self.filename = filename
            self.lastDirectory = os.path.dirname(filename)

            self.editor.modified = 0

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


    ### File choosing

    def createFileChooser(self):
        defaultDir = JESConfig.getInstance().getStringProperty(JESConfig.CONFIG_MEDIAPATH)
        chooser = self.fileChooser = FileChooser(defaultDir)
        chooser.addExtensionFilter("py", "Python programs")

    def selectProgramToOpen(self):
        self.fileChooser.dialogTitle = "Open Program"
        self.fileChooser.validator = None

        # Don't leave the current file selected when the dialog box opens.
        self.fileChooser.selectedFile = None

        # But do navigate to the current file's directory.
        # (If it was opened from the command line, the file chooser would
        # still be sitting in the media path.)
        if self.filename is not None:
            self.fileChooser.currentDirectory = File(os.path.dirname(self.filename))

        return self.fileChooser.chooseFileToOpen(self.parentWindow)

    def selectProgramToSave(self):
        self.fileChooser.dialogTitle = "Save Program"
        self.fileChooser.validator = self.validateFileForSave

        # Navigate to the current file's directory. (See above.)
        if self.filename is not None:
            self.fileChooser.selectedFile = File(self.filename)

        return self.fileChooser.chooseFileToSave(self.parentWindow)

    def validateFileForSave(self, filename):
        if os.path.isfile(filename) and filename != self.filename:
            return self.confirmSave(
                "There's already a file named " + os.path.basename(filename) + ".\n"
                "Would you like to replace it?"
            )
        elif not filename.endswith(".py"):
            return self.confirmSave(
                "A file whose name doesn't end in .py won't be recognized\n"
                "as a Python program by JES or other programs.\n"
                "Are you sure you want to save the file with this name?"
            )
        elif MODULE_NAME_RE.match(os.path.basename(filename)) is None:
            return self.confirmSave(
                "Only .py files whose names are made up of letters, numbers,\n"
                "and underscores can be imported as Python modules.\n"
                "(You will still be able to load it in JES regardless.)\n"
                "Are you sure you want to save the file with this name?"
            )
        else:
            return True


    ### Helpers

    @threadsafe
    def continueAfterSavingOrDiscarding(self, prompt):
        if self.editor.modified:
            promptResult = JOptionPane.showConfirmDialog(self.parentWindow,
                prompt + '\n' + PROMPT_SAVE_OR_DISCARD,
                PROMPT_SAVE_CAPTION, JOptionPane.YES_NO_CANCEL_OPTION
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

    @threadsafe
    def continueAfterSaving(self, prompt):
        if self.filename is None or self.editor.modified:
            promptResult = JOptionPane.showConfirmDialog(self.parentWindow,
                prompt + '\n' + PROMPT_SAVE_REQUIRED,
                PROMPT_SAVE_CAPTION, JOptionPane.YES_NO_OPTION
            )

            if promptResult == JOptionPane.YES_OPTION:
                isSaved = self.saveAction()
                if isSaved:
                    # The file saved, keep going.
                    return True
                else:
                    # The file _isn't_ saved, bail out.
                    return False
            else:
                # The user decided to cancel, bail out.
                return False
        else:
            return True

    def showErrorMessage(self, title, prefix, path, exc):
        excMessage = getattr(exc, 'strerror', str(exc))
        message = "%s %s:\n%s" % (prefix, os.path.basename(path), excMessage)
        JOptionPane.showMessageDialog(self.parentWindow, message, title,
                                      JOptionPane.ERROR_MESSAGE)

    def confirmSave(self, message):
        return JOptionPane.showConfirmDialog(
            self.parentWindow, message,
            "Confirm Save", JOptionPane.YES_NO_OPTION
        ) == JOptionPane.YES_OPTION

